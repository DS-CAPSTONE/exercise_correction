   #
   # "source": [
   #  "!pip install flask-ngrok\n",
   #  "!ngrok authtoken '2XOdyPMrFkPtpDYB1uFDfe5U2Gr_6QsDjApXHA3vtnyCxZW6d'\n"
   # ]

# Import necessary libraries
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok
import joblib

# Initialize Flask app
app = Flask(__name__)
  # This will expose the Flask app to the internet via ngrok

# Load the trained model and label encoder
clf = joblib.load('./decision_model/exercise_model.pkl')
le = joblib.load('./decision_model/label_encoder.pkl')

# Define API route for making predictions
@app.route('/predict', methods=['GET'])  # Change to GET method
def predict():
    # Get the input data from the GET request
    # You can change the expected input parameters as needed
    lower_back_pain = request.args.get('lower_back_pain', type=int)  # Expecting 0 or 1
    stretching_exercises = request.args.get('stretching_exercises', type=int)  # Expecting 0 or 1
    reps = request.args.get('reps', type=int)  # Expecting 0 or 1
    sets = request.args.get('sets', type=int)  # Expecting 0 or 1
    # Add more parameters as needed...

    # Prepare the new data for prediction
    new_data = [[lower_back_pain, stretching_exercises, reps, sets]]  # Replace with your actual features

    # Predict the recommended exercise
    predicted_exercise = clf.predict(new_data)
    predicted_exercise_decoded = le.inverse_transform([predicted_exercise[0]])

    # Return the prediction as JSON response
    return jsonify({'Recommended Exercise': predicted_exercise_decoded[0]})

# Start the Flask app
if __name__ == "__main__":
    app.run(port=5006)  # You can keep this line if it works for you
