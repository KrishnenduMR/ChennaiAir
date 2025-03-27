import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message

# Define the path to the CSV file
csv_path = "./static/data/forecast_alandur_daily_aqi.csv"

# Read CSV file into a DataFrame
df = pd.read_csv(csv_path)

def get_aqi_message(value):
    if value < 50:
        return f"{value} (Good) - Air quality is excellent. Enjoy your day!"
    elif value <= 100:
        return f"{value} (Satisfactory) - Air quality is acceptable. No major concerns."
    elif value <= 200:
        return f"{value} (Moderate) - Air quality is fair, but sensitive individuals should take precautions."
    elif value <= 300:
        return f"{value} (Poor) - Air quality may affect people with respiratory issues."
    elif value <= 400:
        return f"{value} (Very Poor) - Unhealthy air quality. Limit outdoor activities."
    else:
        return f"{value} (Severe) - Hazardous air quality! Stay indoors and avoid exposure."

# Process AQI data from DataFrame
aqi_info = ""
for index, row in df.iterrows():  # Now using df instead of csv_data
    aqi_value = row["AQI"]
    date_time = row["Datetime"]
    aqi_message = get_aqi_message(aqi_value)
    aqi_info += f"Date: {date_time}, AQI: {aqi_message}\n"

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'anaghasrikrishna@gmail.com'
app.config['MAIL_PASSWORD'] = 'lpjr vsnd ussz cdiu'  # Use an app password for security
app.config['MAIL_DEFAULT_SENDER'] = 'anaghasrikrishna@gmail.com'

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        recipient_email = data.get("email")

        if not recipient_email:
            return jsonify({"message": "Recipient email is required!"}), 400

        msg = Message(
            "Air Quality Alert",
            recipients=[recipient_email],
            body=f"Dear User,\n\nHere is the forecast AQI data:\n\n{aqi_info}\n\nBest Regards,\nChennai Air Team"
        )    

        # Send the email
        mail.send(msg)
        
        return jsonify({"message": f"Email sent successfully to {recipient_email}!"})
    except Exception as e:
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
