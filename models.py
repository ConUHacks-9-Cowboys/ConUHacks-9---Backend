from typing import Annotated

from pydantic import BaseModel, Field


class NewExercise(BaseModel):
    name: str = Field(description="The name of the exercise")
    index: int = Field(description="The index of the exercise in frontend")
    instructions: str = Field(description="The instruction of the exercise")
