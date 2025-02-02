import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import base64
import cv2
from pathlib import Path
from playsound import playsound
from gtts import gTTS
import os

load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API")
CHROME = os.path.join(
    "C:\\", "Program Files (x86)", "Google", "Chrome", "Application", "chrome.exe"
)
speech_file_path = Path(__file__).parent / "speech.mp3"


client = OpenAI(api_key=OPENAI_KEY)


def send_image(image: cv2.Mat):
    class StressResponse(BaseModel):
        stress_level: int

    _, buffer = cv2.imencode(".png", image)
    base64_string = base64.b64encode(buffer).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_string}"},
                    },
                    {
                        "type": "text",
                        "text": "Looking at this person, tell from a scale of 1 to 10 how stressed do they look like?",
                    },
                ],
            },
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "stress_level",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "level": {
                            "type": "number",
                            "description": "The stress level as an integer value.",
                        }
                    },
                    "required": ["level"],
                    "additionalProperties": False,
                },
            },
        },
    )

    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=
    # )
    return response.choices[0]


def text_to_speech(text: str):
    myobj = gTTS(text=text, lang="en", slow=False)
    myobj.save(speech_file_path)
    playsound(speech_file_path)


class Browser:
    def __init__(self) -> None:
        pass

    def open_url(self, url: str):
        self.pid = os.system(f'start chrome "{url}" --kiosk')

    def close(self):
        os.system("taskkill /im chrome.exe")
