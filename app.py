from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import pickle
import joblib
from typing import List
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="ML Model API")

# Load the model
MODEL_PATH = "decision_tree_model.pkl"
model = joblib.load(MODEL_PATH)

# Define input data model
class PredictionInput(BaseModel):
    features: List[float]

class RetrainInput(BaseModel):
    max_depth: int
    min_samples_split: int
    min_samples_leaf: int

@app.get("/")
def home():
    return {"health_check": "OK", "model_version": "1.0.0"}

@app.post("/predict")
def predict(input_data: PredictionInput):
    try:
        # Convert input features to numpy array
        features = pd.DataFrame([input_data.features])
        # Make prediction
        prediction = model.predict(features)
        return {"prediction": prediction.tolist()[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrain")
def retrain(input_data: RetrainInput):
    try:
        # Load training data
        train_data = pd.read_csv("training_data.csv")
        X_train = train_data.drop('target', axis=1)
        y_train = train_data['target']
        
        # Create and train new model with updated parameters
        from sklearn.tree import DecisionTreeClassifier
        new_model = DecisionTreeClassifier(
            max_depth=input_data.max_depth,
            min_samples_split=input_data.min_samples_split,
            min_samples_leaf=input_data.min_samples_leaf
        )
        new_model.fit(X_train, y_train)
        
        # Save the new model
        joblib.dump(new_model, MODEL_PATH)
        return {"message": "Model retrained successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
