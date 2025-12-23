from flask import Flask, request, jsonify
from pymongo import MongoClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Email Config
SENDER_EMAIL = "bb1.deavanathan.s@gmail.com"
SENDER_PASSWORD = "ipwm okbq ryso xyjc"

@app.route('/send_bill', methods=['POST'])
def send_bill():
    data = request.json
    recipient_email = data.get('to_email')
    bill_content = data.get('bill_content')
    
    if not recipient_email: return jsonify({"message": "No recipient"}), 400

    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = "Your Food Order Bill"

        msg.attach(MIMEText(bill_content, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        print(f"Email error: {e}")
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    print("Notification Service running on port 5007")
    app.run(port=5007, debug=True)
