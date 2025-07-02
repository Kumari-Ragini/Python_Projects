from flask import Flask, render_template, request
import smtplib
import pyttsx3
import geocoder
from googlesearch import search
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pushbullet import Pushbullet

from email.message import EmailMessage
import pythoncom  # Add this import

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send_email', methods=['POST'])
def send_email():
    recipient = request.form['email']
    body = request.form['message']

    try:
        msg = EmailMessage()
        msg['Subject'] = "Message from Flask App"
        msg['From'] = "your_email@gmail.com"
        msg['To'] = recipient
        msg.set_content(body)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("itsrcragini2004@gmail.com", "kfwf ebgv hanv pdha")  # App Password
        server.send_message(msg)
        server.quit()
        
        return "✅ Email Sent Successfully!"
    except Exception as e:
        return f"❌ Error sending email: {str(e)}"

PB_API_KEY = "o.nPe9cWQaz2pgNHQQSPs2lfyKKN6is8Uk"
@app.route('/send_sms_mobile', methods=['POST'])
def send_sms_mobile():
    try:
        number = request.form['phone']
        message = request.form['message']
        pb = Pushbullet(PB_API_KEY)
        pb.push_note(f"SMS to {number}", message)
        return "Message sent to your mobile via Pushbullet"
    except Exception as e:
        return f"Error sending message: {str(e)}"
    
@app.route('/google_search', methods=['POST'])
def google_search():
    query = request.form['query']
    results = list(search(query, num_results=5))
    return '<br>'.join(results)

@app.route('/geo_location')
def geo_location():
    g = geocoder.ip('me')
    return f"Your Location: {g.city}, {g.country}\nCoordinates: {g.latlng}"

@app.route('/text_to_audio', methods=['POST'])
def text_to_audio():
    try:
        pythoncom.CoInitialize()  # 👈 This line solves the COM error
        text = request.form['text']
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "✅ Text-to-speech completed!"
    except Exception as e:
        return f"❌ Error in text-to-speech: {str(e)}"

@app.route('/set_volume', methods=['POST'])
def set_volume():
    try:
        pythoncom.CoInitialize()  # ✅ THIS IS IMPORTANT!
        volume_level = float(request.form['volume'])  # from 0.0 to 1.0
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(volume_level, None)
        return f"Volume set to {int(volume_level * 100)}%"
    except Exception as e:
        return f"Error setting volume: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
