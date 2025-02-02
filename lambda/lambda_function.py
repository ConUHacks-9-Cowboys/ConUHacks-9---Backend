# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from openai import OpenAI
from ask_sdk_model import Response
import requests
import json

client = OpenAI(api_key="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")


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Yeehaw! Welcome to the Cowboy Wellness center! Yo ol' pal cowby is gonna fix you right up! How are you feeling?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
                
        )


class CheckStressIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CheckStressIntent")(handler_input)

    def handle(self, handler_input):
        #setPersistentAttributes({["CurrentStressLevel" : handler_input.intent.slots.number.value]});
        #savePersistentAttributes() : Promise<void>;
        # type: (HandlerInput) -> Response
        
        stress_factor = handler_input.request_envelope.request.intent.slots["number"].value
        #IF 5>THEN
        if int(stress_factor) > 5:
    # api call to gpt with the supplied stress level
            message = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": "You are a the response generator for an AI powered home assistant device. You are going to be given a list of exercises and a stress score on a scale of 1 to 10, and you are going to pick an exercise off the list that you think will help the user relieve stress. Answer with the chosen exercise and the response with instructions to be played for the user in a json format as follows: {'exercise':'', 'instructions':''}\n",
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"The list of exercises sorted by stress level is as follows: Low Stress:\\n 0. Neck Rolls\\n 1. Shoulder Shrugs\\n 2. Arm Extension\\n 3. Deep Breathing\\n 4. Hand and wrist stretch\\n 5. Medium Stress:\\n 6. Deep Breathing\\n 7. Take a walk\\n 8. Seated Spinal Twist\\n 9. Standing Stretches\\n 10. Wall push up\\n 11. High Stress\\n 12. Deep Breathing\\n 13. Jumping Jakes (silent version)\\n 14. Squats\\n 15. Lunges\\n 16. High Knees\\n 17. Desk push up. The stress level of the user is {stress_factor}\n     \n",
                            }
                        ],
                    },

                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "exercise_recommendation",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "exercise": {
                                    "type": "string",
                                    "description": "The chosen exercise that is recommended to help relieve stress.",
                                },
                                "instructions": {
                                    "type": "string",
                                    "description": "Instructions on how to perform the chosen exercise.",
                                },
                                "index": {
                                    "type": "number",
                                    "description": "The index of the exercise on the list provided starting on 0",
                                },
                            },
                            "required": ["exercise", "instructions", "index"],
                            "additionalProperties": False,
                        },
                    },
                },
                temperature=1,
                max_completion_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
    # Returns text to speak with instructions for the exercise
            speak_output = json.loads(message.choices[0].message.content)["instructions"]
            print(speak_output)
            # sends api call with the instruction ID to local api
            requests.post(
                "https://molly-select-beagle.ngrok-free.app/user/exercise/new",
                headers={"Content-Type":"application/json"},
                json={"name": json.loads(message.choices[0].message.content)["exercise"], "index": json.loads(message.choices[0].message.content)["index"]},
            )
        
            return (
                    handler_input.response_builder
                        .speak(speak_output)
                        .ask("Let me know when you're done")
                        .response
                )
        else:
            return (
                handler_input.response_builder
                .speak("Nevermind!")
                .response
        )
        

class CheckCompletionIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CheckCompletionIntent")(handler_input)

    def handle(self, handler_input):
        #setPersistentAttributes({["CurrentStressLevel" : handler_input.intent.slots.number.value]});
        #savePersistentAttributes() : Promise<void>;
        # type: (HandlerInput) -> Response
        
        speak_output = handler_input.request_envelope.request.intent.slots["number"].value

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("What is your stress level?")
                .response
        )


class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "AHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
                
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())

sb.add_request_handler(CheckStressIntentHandler())
sb.add_request_handler(CheckCompletionIntentHandler())

sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()