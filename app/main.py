from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field, field_validator
import pandas as pd
from typing import Optional
from dotenv import load_dotenv

import joblib
import os

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# Load the model once when app starts
model_path = os.path.join(os.path.dirname(__file__), "iris.mdl")
model = joblib.load(model_path)

class IrisFeatures(BaseModel):
    """Model input: 4 numerical values for the Iris classifier."""
    sepal_length: Optional[float] = Field(default=None, alias="sepal_length")
    sepal_width: Optional[float] = Field(default=None, alias="sepal_width")
    petal_length: Optional[float] = Field(default=None, alias="petal_length")
    petal_width: Optional[float] = Field(default=None, alias="petal_width")

    model_config = {
        "populate_by_name": True
    }

    @field_validator("sepal_length", "sepal_width", "petal_length", "petal_width", mode="before")
    def convert_non_float_to_none(cls, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
        
app = FastAPI(
    title="Predict Iris Species",
    description="Predict the species of an Iris flower based on length and width of sepal and petal.",
    version="0.1.0"
)

@app.post("/predict", summary="Predict Iris species", response_description="The predicted species")
async def predict_species(data: IrisFeatures,x_api_token: str = Header(...)):
    """
    Predicts the species of an Iris flower based on four numerical features.

    - **sepal_length**
    - **sepal_width**
    - **petal_length**
    - **petal_width**
    """
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    df = pd.DataFrame([data.model_dump(by_alias=True)])
    prediction = model.predict(df)[0]
    return {"predicted_species": prediction}

class NameRequest(BaseModel):
    name: str

@app.post("/hello")
def hello(data: NameRequest):
    return {"message": f"Hello {data.name}"}
