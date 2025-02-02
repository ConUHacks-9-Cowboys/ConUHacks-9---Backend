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
import numpy as np
import soundfile as sf


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
                        "text": "You will receive a picture of an individual occupied by work. You will have to determine how stressed they are on a scale of 1-10, based on their facial expressions, posture, and vibe. A 1 on the scale indicates a very happy person who is smiling, a 4 indicates a person who has a neutral mouth and seemingly neutral eye brow position. 6 and above are when the mouth is tilted downwards, the eybrows are raised or scrunched, and the mouth may be slightly open. Create numerical values based on these to the best of your ability. Analyze the picture well. ",
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
    data, samplerate = sf.read(speech_file_path)
    amplified_data = data * 3.0  # Increase volume 3x

    # Prevent values from exceeding the valid range (-1.0 to 1.0)
    amplified_data = np.clip(amplified_data, -1.0, 1.0)

    # Save the new louder file
    sf.write(speech_file_path, amplified_data, samplerate)
    playsound(speech_file_path)


class Browser:
    def __init__(self) -> None:
        pass

    def open_url(self, url: str):
        self.pid = os.system(f'start chrome "{url}" --kiosk')

    def close(self):
        os.system("taskkill /im chrome.exe")
