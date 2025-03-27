import numpy as np
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Gmail's SMTP server
app.config['MAIL_PORT'] = 587  # SMTP port for TLS (encrypted connection)
app.config['MAIL_USE_TLS'] = True  # Enables TLS (Transport Layer Security)
app.config['MAIL_USE_SSL'] = False  # SSL is not needed when using TLS
app.config['MAIL_USERNAME'] = 'anaghasrikrishna@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'lpjr vsnd ussz cdiu'  # Use an app password for security
app.config['MAIL_DEFAULT_SENDER'] = 'anaghasrikrishna@gmail.com'  # Sender email

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()  # Get JSON data from request
        recipient_email = data.get("email")  # Extract email from request

        if not recipient_email:
            return jsonify({"message": "Recipient email is required!"}), 400

        msg = Message(
            "Notification Alert",
            recipients=[recipient_email],  # Use the email from the request
            body="This is a test notification from your Flask app!"
        )
        mail.send(msg)
        return jsonify({"message": f"Email sent successfully to {recipient_email}!"})
    except Exception as e:
        return jsonify({"message": f"Failed to send email: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)