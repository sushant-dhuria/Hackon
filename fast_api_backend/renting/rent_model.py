import tensorflow as tf
from sklearn.preprocessing import StandardScaler  # Ensure you have the appropriate pre-processing available

# Load the model architecture from the JSON file
with open("renting/rent_model.json", "r") as json_file:
    loaded_model_json = json_file.read()
loaded_model = tf.keras.models.model_from_json(loaded_model_json)

# Load the model weights from the HDF5 file
loaded_model.load_weights("renting/rent_model.h5")

# You may need to reapply the same preprocessing transformations to your input data
# In this case, we use StandardScaler as an example
def predict_rent(input):
    scaler = StandardScaler()
    scaled_input_data = scaler.fit_transform(input)

    # Make predictions using the loaded model
    predictions = loaded_model.predict(scaled_input_data)
    return float(predictions[0][0])