import joblib

# Load the saved model
model_filename = 'renting/rent_model.pkl'
loaded_model = joblib.load(model_filename)


# You may need to reapply the same preprocessing transformations to your input data
# In this case, we use StandardScaler as an example
def predict_rent(input):

    # Make predictions using the loaded model
    predictions = loaded_model.predict(input)
    return float(predictions[0])