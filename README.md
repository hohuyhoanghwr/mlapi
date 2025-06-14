# Iris Species Prediction API

This project is a FastAPI-based web service that predicts the species of an Iris flower based on four input features: sepal length, sepal width, petal length, and petal width.

The model is trained using the classic Iris dataset and deployed via Docker and CapRover. The API uses a pre-trained pipeline that handles missing or non-float values using median imputation.

---

##  Deployed API

- **POST Endpoint**: [`/predict`](https://iris.captain.dev.huyhoangho.online/predict) -- the app only has post method so can only be inspected via /docs
  - Use this endpoint to send flower measurements in JSON and get the predicted species.
  - Requires a header:  
    `x-api-token: [For professor Roland: please see my submission message in Moodle. For others: contact me]`

- **API Docs**: [`/docs`](https://iris.captain.dev.huyhoangho.online/docs)  
  - Interactive Swagger UI for testing and documentation

---

## 🧪 Example Input

```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
