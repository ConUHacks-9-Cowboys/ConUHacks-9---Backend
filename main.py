from fastapi import FastAPI
import asyncio
from utils import send_image, text_to_speech, Browser
import multiprocessing
from capture import start_capture
from models import NewExercise
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()
browser = Browser()

# Mount the "static" directory at the "/static" URL path
app.mount("/static", StaticFiles(directory="static"), name="static")


async def periodic_capture():
    while True:
        shared_dict["request"] = 1
        while shared_dict["frame"] is None:
            pass

        frame = shared_dict["frame"]
        result = send_image(frame)
        await asyncio.sleep(10)


templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def start_periodic_task():
    # Run the periodic task in the background
    # asyncio.create_task(periodic_capture())
    pass


@app.get("/")
async def root():
    shared_dict["request"] = 1
    while shared_dict["frame"] is None:
        pass

    frame = shared_dict["frame"]
    result = json.loads(send_image(frame).message.content)["level"]
    text_to_speech(f"Alexa! open wellness cowboy")
    await asyncio.sleep(11)
    text_to_speech(f"The stress level is {result}")

    return {"message": "done"}


@app.get("/tts")
async def tts():
    text_to_speech("Alexa! play Let it go")
    return {"message": "done"}


@app.post("/user/exercise/cancel")
async def cancel():
    pass


@app.post("/user/exercise/done")
async def done():
    browser.close()
    return {"message": "done"}


@app.post("/user/stressed")
async def is_stressed():
    pass


@app.post("/user/exercise/new")
async def new(exercise: NewExercise):
    browser.open_url(
        f"http://localhost:8000/exercise/?name={exercise.name}&index={exercise.index}&instructions={exercise.instructions}"
    )

    return {"message": "done"}


@app.get("/exercise/")
async def show_exercise(request: Request, name: str, index: int, instructions: str):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "name": name,
            "index": index,
            "instructions": instructions,
        },
    )


# Run the FastAPI app
if __name__ == "__main__":
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()
    shared_dict["request"] = 0
    shared_dict["frame"] = None

    capture_process = multiprocessing.Process(target=start_capture, args=(shared_dict,))
    capture_process.start()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
    capture_process.join()  # Ensure the process is cleaned up when the server stops
