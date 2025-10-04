from flask import Flask, render_template, request, jsonify, redirect, send_from_directory, url_for, session, flash 
import os, json
from textblob import TextBlob
from dotenv import load_dotenv
import openai
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import uuid
import csv
from sendmail import send_reminder_email  # your email sending function
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from email.message import EmailMessage
import pytesseract
from PIL import Image
from googlesearch import search
from fpdf import FPDF
from duckduckgo_search import DDGS
import re
import pickle
import pytesseract
from serpapi import GoogleSearch
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from werkzeug.security import generate_password_hash, check_password_hash





import cv2





EMAIL_ADDRESS = "hs6202888927@gmail.com"         # ✅ Your Gmail address
EMAIL_PASSWORD = "tkpyofixnkztwjoj" 


app = Flask(__name__)
app.secret_key = 'swasthaAI_secure_2025'  # 🔐 Add this line
app.config['UPLOAD_FOLDER'] = 'static/uploads'
SERPAPI_KEY = "5ebe2f03008186d340e1e851fe89231e9e4b8f2f13fd694854f4843140e78bcc"

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DATA_FILE = 'mood_data.json'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOAD_FOLDER = os.path.join("static", "reports")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'reports')

# Ensure folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)







# File paths for data
DOCTORS_FILE = 'data/doctors.json'
PATIENTS_FILE = 'data/patients.json'
CHATS_FILE = 'data/chats.json'



pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"







@app.route('/')
def home():
    return render_template('index.html')




@app.route('/maternal_health', methods=['GET', 'POST'])
def maternal_health():
    tips = None
    if request.method == 'POST':
        stage = request.form['stage']
        tips_data = {
            'first_trimester': {
                'en': (
                    "• Take folic acid daily to prevent birth defects.\n"
                    "• Avoid alcohol, smoking, and unprescribed medications.\n"
                    "• Eat a balanced diet rich in fruits, vegetables, and whole grains.\n"
                    "• Stay hydrated and get adequate rest.\n"
                    "• Engage in light physical activity like walking or prenatal stretches.\n"
                    "• Schedule your first prenatal visit and begin regular checkups."
                ),
                'hi': (
                    "• जन्म दोषों को रोकने के लिए रोजाना फोलिक एसिड लें।\n"
                    "• शराब, धूम्रपान और बिना डॉक्टर की सलाह की दवाओं से बचें।\n"
                    "• फल, सब्ज़ी और साबुत अनाज से भरपूर संतुलित आहार लें।\n"
                    "• हाइड्रेटेड रहें और भरपूर आराम करें।\n"
                    "• हल्की शारीरिक गतिविधियाँ जैसे चलना या प्रीनेटल स्ट्रेच करें।\n"
                    "• पहली बार प्रसवपूर्व जांच कराएं और नियमित जांच शुरू करें।"
                )
            },
            'second_trimester': {
                'en': (
                    "• Consume calcium, iron, and protein-rich foods to support baby's growth.\n"
                    "• Start sleeping on your side to improve blood flow.\n"
                    "• Monitor fetal movements and attend all checkups.\n"
                    "• Practice gentle prenatal yoga or swimming for relaxation.\n"
                    "• Manage stress through meditation, hobbies, or support groups.\n"
                    "• Consider maternity clothes for comfort and support."
                ),
                'hi': (
                    "• बच्चे की वृद्धि के लिए कैल्शियम, आयरन और प्रोटीन युक्त भोजन लें।\n"
                    "• रक्त प्रवाह के लिए करवट लेकर सोना शुरू करें।\n"
                    "• भ्रूण की गतिविधियों पर ध्यान दें और नियमित जांच कराएं।\n"
                    "• शांति के लिए हल्का प्रीनेटल योग या तैराकी करें।\n"
                    "• ध्यान, शौक या सहायता समूहों के माध्यम से तनाव कम करें।\n"
                    "• आरामदायक कपड़े पहनना शुरू करें।"
                )
            },
            'third_trimester': {
                'en': (
                    "• Finalize your birthing plan and keep your hospital bag ready.\n"
                    "• Increase iron intake and stay active with doctor-approved exercise.\n"
                    "• Practice breathing techniques and attend childbirth classes.\n"
                    "• Ensure you have postnatal support planned (family, caregiver).\n"
                    "• Monitor signs of labor and contact doctor if needed.\n"
                    "• Sleep with extra pillows for support and comfort."
                ),
                'hi': (
                    "• अपनी डिलीवरी योजना को अंतिम रूप दें और अस्पताल का बैग तैयार रखें।\n"
                    "• आयरन की मात्रा बढ़ाएं और डॉक्टर की सलाह अनुसार व्यायाम करें।\n"
                    "• सांस लेने की तकनीकों का अभ्यास करें और प्रसव कक्षा में शामिल हों।\n"
                    "• प्रसवोत्तर सहायता (परिवार, देखभालकर्ता) की योजना बनाएं।\n"
                    "• प्रसव के संकेतों की निगरानी करें और ज़रूरत पर डॉक्टर से संपर्क करें।\n"
                    "• आराम के लिए अतिरिक्त तकियों के साथ सोएं।"
                )
            },
            'post_delivery': {
                'en': (
                    "• Prioritize exclusive breastfeeding for the first 6 months.\n"
                    "• Drink plenty of fluids and eat nutrient-rich meals.\n"
                    "• Maintain hygiene to prevent infections.\n"
                    "• Rest whenever possible to aid recovery.\n"
                    "• Attend postpartum checkups and seek mental health support if needed.\n"
                    "• Do light exercises to regain strength and energy gradually."
                ),
                'hi': (
                    "• पहले 6 महीने तक केवल स्तनपान को प्राथमिकता दें।\n"
                    "• भरपूर पानी पिएं और पौष्टिक भोजन करें।\n"
                    "• संक्रमण से बचने के लिए स्वच्छता बनाए रखें।\n"
                    "• जब भी संभव हो आराम करें ताकि शरीर ठीक हो सके।\n"
                    "• प्रसवोत्तर जांच कराएं और मानसिक स्वास्थ्य में मदद लें यदि ज़रूरत हो।\n"
                    "• धीरे-धीरे हल्की एक्सरसाइज से ताकत और ऊर्जा पाएं।"
                )
            }
        }
        tips = tips_data.get(stage)
    return render_template("maternal_health.html", tips=tips, tips_audio={
    'en': url_for('static', filename='audio/tips_en.mp3'),
    'hi': url_for('static', filename='audio/tips_hi.mp3')
})




@app.route('/scheme_awareness', methods=['GET', 'POST'])
def scheme_awareness():
    schemes = {
        "pregnant_women": [
            "Janani Suraksha Yojana (JSY)",
            "Pradhan Mantri Matru Vandana Yojana (PMMVY)"
        ],
        "children": [
            "Rashtriya Bal Swasthya Karyakram (RBSK)",
            "Mid-Day Meal Scheme"
        ],
        "elderly": [
            "National Programme for Health Care of Elderly (NPHCE)"
        ],
        "general": [
            "Ayushman Bharat - PMJAY",
            "National Health Mission (NHM)"
        ]
    }
    SCHEME_DATA = {
    "pregnant_women": [
        "Janani Suraksha Yojana",
        "Pradhan Mantri Matru Vandana Yojana",
        "Mother and Child Tracking System (MCTS)"
    ],
    "children": [
        "Rashtriya Bal Swasthya Karyakram (RBSK)",
        "Mid Day Meal Scheme",
        "Universal Immunization Programme"
    ],
    "elderly": [
        "National Programme for Health Care of the Elderly (NPHCE)",
        "Indira Gandhi National Old Age Pension Scheme"
    ],
    "general": [
        "Ayushman Bharat - PM-JAY",
        "National Health Insurance Scheme (RSBY)",
        "Health and Wellness Centres (HWC)"
    ]
}

    selected = None
    keyword = ""
    result = []

    if request.method == "POST":
        selected = request.form.get("category")
        keyword = request.form.get("keyword", "").lower()

        # Combine all schemes if no category selected
        if selected:
            schemes = SCHEME_DATA.get(selected, [])
        else:
            # Flatten all schemes
            schemes = [s for schemes_list in SCHEME_DATA.values() for s in schemes_list]

        # Filter based on keyword
        if keyword:
            result = [s for s in schemes if keyword in s.lower()]
        else:
            result = schemes

    return render_template("scheme_awareness.html", selected=selected, keyword=keyword, result=result)


@app.route('/telemedicine', methods=['GET', 'POST'])
def telemedicine():
    response = ""
    if request.method == 'POST':
        query = request.form['query'].lower()

        if "fever" in query:
            response = "Drink plenty of fluids, take paracetamol, and rest. If the fever lasts more than 3 days, consult a doctor."
        elif "cough" in query:
            response = "Try warm fluids, use throat lozenges, and avoid cold drinks. If it persists, visit a respiratory specialist."
        elif "headache" in query:
            response = "Stay hydrated, take rest, and reduce screen time. If severe, see a neurologist."
        elif "cold" in query:
            response = "Stay warm, use nasal drops, and drink warm fluids. If symptoms worsen, consult a physician."
        elif "stomach pain" in query:
            response = "Avoid spicy food, stay hydrated, and rest. If pain is severe, consult a gastroenterologist."
        elif "vomiting" in query:
            response = "Take ORS or lemon water. Avoid solid foods. Consult a doctor if it continues."
        elif "diarrhea" in query:
            response = "Drink ORS and eat bland food. Avoid dairy. See a doctor if symptoms last."
        elif "skin rash" in query:
            response = "Apply soothing lotion. Avoid scratching. See a dermatologist if it worsens."
        elif "eye pain" in query:
            response = "Rest your eyes, avoid screens, and use eye drops. Visit an eye specialist if needed."
        elif "chest pain" in query:
            response = "If it's severe or radiates, seek emergency care immediately. Never ignore chest pain."
        elif "sore throat" in query:
            response = "Gargle with warm salt water. Drink warm fluids. If pain lasts, consult an ENT."
        else:
            response = "Symptom not recognized. Please consult a certified doctor for accurate diagnosis."

    return render_template('telemedicine.html', response=response)



@app.route('/ai_chat', methods=['GET', 'POST'])
def ai_chat():
    answer = ""
    if request.method == 'POST':
        user_message = request.form.get('message')
        try:
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful healthcare assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            answer = "This is a demo response. The AI chatbot is currently offline due to quota limits."

            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"Error: {str(e)}"
    return render_template('ai_chat.html', answer=answer)




@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    reminders = []
    user_email = None
    searched = False

    if request.method == 'POST':
        user_email = request.form.get('email', '').strip().lower()
        searched = True

        try:
            with open('reminders.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if 'email' not in row:
                        continue
                    if row['email'].strip().lower() == user_email:
                        reminders.append({
                            'name': row.get('name', ''),
                            'reason': row.get('reason', ''),
                            'reminder_type': row.get('reminder_type', ''),
                            'date': row.get('date', '')
                        })
        except FileNotFoundError:
            print("File not found: reminders.csv")
        except Exception as e:
            print("Error reading reminders.csv:", e)

    return render_template('reminder_dashboard.html', reminders=reminders, user_email=user_email, searched=searched)

def send_reminder_email(to_email, name, reason, date, reminder_type):
    subject = f"⏰ Health Reminder: {reminder_type}"
    body = f"""
Hi {name},

This is a gentle reminder for your upcoming health-related event.

🩺 Type: {reminder_type}
📆 Date: {date}
📝 Reason: {reason}

Stay healthy!
– SwasthaAI
"""

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return False

@app.route('/reminder', methods=['GET', 'POST'])
def reminder():
    today = datetime.today().date()
    upcoming = []
    message = None

    csv_file = "reminders.csv"
    fieldnames = ['name', 'email', 'reminder_type', 'date', 'reason']

    # Ensure file exists
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    # Handle form submission
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        reminder_type = request.form['reminder_type']
        date = request.form['date']
        reason = request.form['reason']

        with open(csv_file, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([name, email, reminder_type, date, reason])

        send_reminder_email(email, name, reason, date, reminder_type)
        message = "✅ Reminder saved & email sent!"
        return redirect('/reminder')

    # Show upcoming reminders
    try:
        with open(csv_file, newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    name, email, reminder_type, date_str, reason = row
                    reminder_date = datetime.strptime(date_str.strip(), '%Y-%m-%d').date()
                    if today <= reminder_date <= today + timedelta(days=3):
                        upcoming.append((name, reason, reminder_date))
                except:
                    continue
    except FileNotFoundError:
        pass

    return render_template('reminder.html', message=message, upcoming=upcoming)

def send_scheduled_reminders():
    today = datetime.now().date()
    try:
        with open("reminders.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    name, email, reminder_type, date_str, reason = row
                    reminder_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                    if reminder_date - timedelta(days=3) == today:
                        send_reminder_email(email, name, reason, date_str, reminder_type)
                except:
                    continue
    except FileNotFoundError:
        print("reminders.csv not found")

# Start scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=send_scheduled_reminders, trigger="interval", hours=24)
scheduler.start()


from generate_ics import create_ics_file

@app.route('/calendar-reminder', methods=['GET', 'POST'])
def calendar_reminder():
    if request.method == 'POST':
        name = request.form['name']
        reminder_type = request.form['reminder_type']
        reason = request.form['reason']
        date = request.form['date']

        filename = create_ics_file(name, reminder_type, reason, date)
        return render_template('calendar_download.html', filename=filename)

    return render_template('set_calendar_reminder.html')


# Ensure file exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump([], f)

@app.route('/mentalcheckin')
def mentalcheckin():
    return render_template('mental_checkin.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/api/mood', methods=['GET'])
def get_moods():
    with open(DATA_FILE, 'r') as f:
        return jsonify(json.load(f))

@app.route('/api/mood', methods=['POST'])
def post_mood():
    data = request.json
    required = ['date', 'mood', 'anxiety', 'sleep', 'energy', 'note']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing fields'}), 400

    with open(DATA_FILE, 'r') as f:
        moods = json.load(f)

    moods.append(data)

    with open(DATA_FILE, 'w') as f:
        json.dump(moods, f, indent=2)

    return jsonify({'message': 'Mood logged'}), 200

@app.route('/relaxation')
def relaxation():
    return render_template('relaxation.html')

@app.route('/medicine')
def medicine():
    return render_template('medicine_compare.html')

# Route to serve the Mental Health Support Page
@app.route("/mental-support")
def mental_support():
    return render_template("mental_support.html")

# API for text mood analysis
@app.route("/analyze-text", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    analysis = TextBlob(text)
    sentiment = analysis.sentiment.polarity

    if sentiment < -0.3:
        mood = "Negative - Possible depression or sadness"
    elif sentiment < 0.1:
        mood = "Neutral"
    else:
        mood = "Positive"

    return jsonify({"mood": mood, "score": sentiment})
@app.route("/face-emotion")
def face_emotion():
    return render_template("face_emotion.html")


os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def analyze_bp(s, d):
    """Analyze blood pressure and give detailed advice."""
    if s < 120 and d < 80:
        return "Normal", "Maintain healthy lifestyle, regular exercise, balanced diet."
    elif 120 <= s <= 129 and d < 80:
        return "Elevated", "Monitor blood pressure regularly, reduce salt intake, exercise."
    elif 130 <= s <= 139 or 80 <= d <= 89:
        return "Stage 1 Hypertension", "Consult a doctor, lifestyle changes, possible medication."
    elif 140 <= s or 90 <= d:
        return "Stage 2 Hypertension", "Medical attention required, follow prescribed treatment."
    else:
        return "Hypertensive Crisis", "Seek emergency medical care immediately!"

def analyze_sugar(fasting, post):
    """Analyze blood sugar levels with advice."""
    if fasting < 100 and (post is None or post < 140):
        return "Normal", "Maintain balanced diet, regular exercise."
    elif 100 <= fasting < 126 or (post is not None and 140 <= post < 200):
        return "Prediabetes", "Monitor sugar levels, reduce sugar intake, exercise regularly."
    else:
        return "Diabetes", "Consult a doctor for management plan, monitor blood sugar daily."

def analyze_cholesterol(chol):
    """Analyze cholesterol levels."""
    if chol < 200:
        return "Desirable", "Maintain healthy diet and exercise."
    elif 200 <= chol < 239:
        return "Borderline High", "Reduce saturated fats, increase fiber intake, exercise."
    else:
        return "High", "Consult a doctor, consider lifestyle changes or medications."

def analyze_bmi(bmi, height_m=None, weight_kg=None):
    """Analyze BMI with health risk and ideal weight range if height & weight provided."""
    advice = ""
    category = ""
    if bmi < 18.5:
        category = "Underweight"
        advice = "Increase calorie intake with healthy foods, strength training recommended."
    elif 18.5 <= bmi < 24.9:
        category = "Normal"
        advice = "Maintain current lifestyle, regular exercise and balanced diet."
    elif 25 <= bmi < 29.9:
        category = "Overweight"
        advice = "Consider weight loss strategies, balanced diet, and regular exercise."
    else:
        category = "Obese"
        advice = "Medical consultation recommended, weight reduction program advised."

    # Optional ideal weight calculation
    if height_m:
        min_weight = 18.5 * (height_m ** 2)
        max_weight = 24.9 * (height_m ** 2)
        advice += f" Ideal weight range: {min_weight:.1f}kg - {max_weight:.1f}kg."

    return category, advice

def analyze_heart_rate(hr, age=None):
    """Analyze resting heart rate."""
    if hr < 60:
        return "Bradycardia", "Low heart rate, may be normal for athletes; consult if symptomatic."
    elif 60 <= hr <= 100:
        return "Normal", "Maintain current lifestyle, regular physical activity."
    else:
        return "Tachycardia", "High heart rate, consult a doctor for evaluation."


@app.route('/health_form', methods=['GET', 'POST'])
def health_report():
    report_path = None

    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        gender = request.form['gender']
        height = float(request.form['height_cm']) / 100
        weight = float(request.form['weight_kg'])
        systolic = int(request.form['bp_systolic'])
        diastolic = int(request.form['bp_diastolic'])
        fasting = int(request.form['sugar_fasting'])
        post = request.form.get('sugar_post')
        cholesterol = request.form.get('cholesterol')
        heart_rate = request.form.get('heart_rate')
        hemoglobin = request.form.get('hemoglobin')
        notes = request.form.get('notes')

        # Convert optional fields
        post = int(post) if post else None
        cholesterol = int(cholesterol) if cholesterol else None
        heart_rate = int(heart_rate) if heart_rate else None
        hemoglobin = float(hemoglobin) if hemoglobin else None

        # Health Analysis
        bmi = weight / (height ** 2)
        bmi_cat, bmi_advice = analyze_bmi(bmi, height, weight)
        bp_cat, bp_advice = analyze_bp(systolic, diastolic)
        sugar_cat, sugar_advice = analyze_sugar(fasting, post)
        chol_cat, chol_advice = analyze_cholesterol(cholesterol) if cholesterol else ("Not provided", "No advice")
        hr_cat, hr_advice = analyze_heart_rate(heart_rate) if heart_rate else (None, None)

        # Generate PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, "SwasthaAI - Health Report", ln=True, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.ln(10)

        # Patient Info
        pdf.cell(200, 10, f"Patient Name: {name}", ln=True)
        pdf.cell(200, 10, f"Age: {age}   Gender: {gender}", ln=True)
        pdf.cell(200, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
        pdf.ln(10)

        # Health Analysis Section
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, "Health Analysis & Recommendations:", ln=True)
        pdf.set_font("Arial", '', 12)
        pdf.cell(200, 10, f"BMI: {bmi:.2f} - {bmi_cat}", ln=True)
        pdf.multi_cell(0, 10, f"Advice: {bmi_advice}")
        pdf.cell(200, 10, f"Blood Pressure: {systolic}/{diastolic} mmHg - {bp_cat}", ln=True)
        pdf.multi_cell(0, 10, f"Advice: {bp_advice}")
        pdf.cell(200, 10, f"Fasting Sugar: {fasting} mg/dL - {sugar_cat}", ln=True)
        if post:
            pdf.cell(200, 10, f"Post-Meal Sugar: {post} mg/dL", ln=True)
        pdf.multi_cell(0, 10, f"Advice: {sugar_advice}")
        pdf.cell(200, 10, f"Cholesterol: {cholesterol if cholesterol else 'Not provided'} mg/dL - {chol_cat}", ln=True)
        pdf.multi_cell(0, 10, f"Advice: {chol_advice}")
        if heart_rate:
            pdf.cell(200, 10, f"Heart Rate: {heart_rate} bpm - {hr_cat}", ln=True)
            pdf.multi_cell(0, 10, f"Advice: {hr_advice}")
        if hemoglobin:
            pdf.cell(200, 10, f"Hemoglobin: {hemoglobin} g/dL", ln=True)
        if notes:
            pdf.ln(5)
            pdf.multi_cell(0, 10, f"Additional Notes: {notes}")

        # Save PDF
        filename = f"{name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf.output(path)
        report_path = filename

    return render_template("health_form.html", report_path=report_path)


def send_email_report(to_email, filename, filepath):
    try:
        msg = EmailMessage()
        msg['Subject'] = 'SwasthaAI Health Report'
        msg['From'] = 'youremail@gmail.com'
        msg['To'] = to_email
        msg.set_content('Dear Patient,\n\nPlease find your SwasthaAI health report attached.\n\nRegards,\nSwasthaAI Team')

        with open(filepath, 'rb') as f:
            file_data = f.read()
            msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=filename)

        # Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('youremail@gmail.com', 'your_app_password')
            smtp.send_message(msg)

        print(f"Email sent to {to_email}")
    except Exception as e:
        print("Email sending failed:", e)




# Helper functions
def load_data(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except:
        return {}


def save_data(path, data):
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

def load_data(file):
    if not os.path.exists(file):
        return {}
    with open(file, 'r') as f:
        return json.load(f)

def save_data(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Admin Login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['role'] = 'admin'
            return redirect('/admin/dashboard')
    return render_template('admin_login.html')

# Admin Dashboard
# Admin Dashboard
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect('/admin')

    doctors = load_data(DOCTORS_FILE)
    if isinstance(doctors, list):
        doctors = {str(i): doc for i, doc in enumerate(doctors)}

    # Add new doctor
    if request.method == 'POST':
        doctor_id = str(uuid.uuid4())[:8]

        profile_pic = request.files.get('profile_pic')
        profile_filename = ""
        if profile_pic:
            profile_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'doctor_profiles')
            os.makedirs(profile_folder, exist_ok=True)
            profile_filename = f"{doctor_id}_{profile_pic.filename}"
            profile_path = os.path.join(profile_folder, profile_filename)
            profile_pic.save(profile_path)

        doctors[doctor_id] = {
            'id': doctor_id,
            'name': request.form['name'],
            'degree': request.form['degree'],
            'experience': request.form['experience'],
            'speciality': request.form['speciality'],
            'fees': request.form['fees'],
            'working_place': request.form['working_place'],
            'profile_pic': profile_filename,
            'password': request.form['password']
        }
        save_data(DOCTORS_FILE, doctors)

    return render_template('admin_dashboard.html', doctors=doctors)


# Delete Doctor
@app.route('/admin/delete_doctor/<doctor_id>')
def delete_doctor(doctor_id):
    if session.get('role') != 'admin':
        return redirect('/admin')
    
    doctors = load_data(DOCTORS_FILE)
    if doctor_id in doctors:
        # Delete profile picture file
        profile_filename = doctors[doctor_id].get('profile_pic', '')
        if profile_filename:
            profile_path = os.path.join(app.config['UPLOAD_FOLDER'], 'doctor_profiles', profile_filename)
            if os.path.exists(profile_path):
                os.remove(profile_path)
        # Delete doctor
        doctors.pop(doctor_id)
        save_data(DOCTORS_FILE, doctors)
    
    return redirect('/admin/dashboard')

# Doctor Login
@app.route('/doctor', methods=['GET', 'POST'])
def doctor_login():
    if request.method == 'POST':
        doc_id = request.form['id']
        password = request.form['password']
        doctors = load_data(DOCTORS_FILE)
        if doc_id in doctors and doctors[doc_id]['password'] == password:
            session['role'] = 'doctor'
            session['doctor_id'] = doc_id
            return redirect('/doctor/dashboard')
    return render_template('doctor_login.html')

# Doctor Dashboard
@app.route('/doctor/dashboard')
def doctor_dashboard():
    if session.get('role') != 'doctor':
        return redirect('/doctor')

    doc_id = session['doctor_id']
    patient_list = []

    for file in os.listdir('chats'):
        if file.startswith(f'chat_{doc_id}_') and file.endswith('.json'):
            patient_id = file.replace(f'chat_{doc_id}_', '').replace('.json', '')
            patient_list.append(patient_id)

    return render_template('doctor_dashboard.html', patient_list=patient_list, doctor_id=doc_id)

SYMPTOM_SPECIALTY_MAP = {
    'fever': 'General Physician',
    'cough': 'Pulmonologist',
    'headache': 'Neurologist',
    'stomach_pain': 'Gastroenterologist',
    'skin_rash': 'Dermatologist',
    'fatigue': 'General Physician'
}

# Patient Login/Register



PATIENTS_FILE = 'patients.json'

# Helper functions
def load_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Patient Register/Login
@app.route('/patient', methods=['GET','POST'])
def patient_login():
    patients = load_data(PATIENTS_FILE)

    if request.method == 'POST':
        # ---- LOGIN ----
        if 'login_id' in request.form:
            patient_id = request.form['login_id']
            password = request.form['login_password']

            if patient_id in patients and patients[patient_id]['password'] == password:
                session['role'] = 'patient'
                session['patient_id'] = patient_id
                return redirect('/patient/dashboard')
            else:
                return "Invalid Patient ID or Password"

        # ---- REGISTRATION ----
        elif 'reg_name' in request.form:
            name = request.form['reg_name']
            age = request.form['reg_age']
            gender = request.form['reg_gender']
            city = request.form['reg_city']
            password = request.form['reg_password']

            if not all([name, age, gender, city, password]):
                return "Please fill all registration fields."

            patient_id = 'P-' + str(uuid.uuid4())[:8]
            patients[patient_id] = {
                'id': patient_id,
                'name': name,
                'age': age,
                'gender': gender,
                'city': city,
                'password': password
            }
            save_data(PATIENTS_FILE, patients)
            return f"Registration Successful! Your Patient ID is {patient_id}. Please login now."

    return render_template('patient_login.html')

# Patient Dashboard


# Send message from patient
# Patient Dashboard
@app.route('/patient/dashboard', methods=['GET', 'POST'])
def patient_dashboard():
    # Ensure patient is logged in
    if session.get('role') != 'patient':
        return redirect('/patient')

    patient_id = session['patient_id']
    patients = load_data(PATIENTS_FILE)
    patient = patients.get(patient_id)

    doctors = load_data(DOCTORS_FILE)

    # Symptom → Specialty mapping
    SYMPTOM_SPECIALTY_MAP = {
        'fever': 'General Physician',
        'cough': 'Pulmonologist',
        'headache': 'Neurologist',
        'stomach_pain': 'Gastroenterologist',
        'skin_rash': 'Dermatologist',
        'fatigue': 'General Physician'
    }

    recommended = []
    selected_symptoms = []

    if request.method == 'POST':
        selected_symptoms = request.form.getlist('symptoms')
        for doc_id, doc in doctors.items():
            for symptom in selected_symptoms:
                if doc['speciality'] == SYMPTOM_SPECIALTY_MAP.get(symptom):
                    recommended.append((doc_id, doc))
                    break
        if not recommended:
            recommended = doctors.items()  # fallback to all doctors

    return render_template(
        'patient_dashboard.html',
        patient=patient,
        doctors=doctors,
        recommended=recommended,
        symptoms=selected_symptoms
    )


@app.route('/chat/send', methods=['POST'])
def send_message():
    if session.get('role') != 'patient':
        return redirect('/patient')

    doctor_id = request.form['doctor_id']
    patient_id = session['patient_id']
    message = request.form['message']

    chat_file = f'chats/chat_{doctor_id}_{patient_id}.json'
    messages = load_data(chat_file)
    messages[str(uuid.uuid4())] = {
        'sender': 'patient',
        'message': message
    }
    save_data(chat_file, messages)

    return redirect(f'/chat/{doctor_id}/{patient_id}')

# Doctor reply
@app.route('/chat/reply/<patient_id>', methods=['POST'])
def reply_message(patient_id):
    if session.get('role') != 'doctor':
        return redirect('/doctor')

    doctor_id = session['doctor_id']
    message = request.form['message']

    chat_file = f'chats/chat_{doctor_id}_{patient_id}.json'
    messages = load_data(chat_file)
    messages[str(uuid.uuid4())] = {
        'sender': 'doctor',
        'message': message
    }
    save_data(chat_file, messages)

    return redirect(f'/chat/{doctor_id}/{patient_id}')

# Chat View
@app.route('/chat/<doctor_id>/<patient_id>')
def chat_view(doctor_id, patient_id):
    role = session.get('role')
    if role not in ['doctor', 'patient']:
        return redirect('/')

    if role == 'doctor' and session.get('doctor_id') != doctor_id:
        return redirect('/doctor/dashboard')
    if role == 'patient' and session.get('patient_id') != patient_id:
        return redirect('/patient/dashboard')

    chat_file = f'chats/chat_{doctor_id}_{patient_id}.json'
    messages = load_data(chat_file)
    return render_template('chat_interface.html', messages=messages, doctor_id=doctor_id, patient_id=patient_id, role=role)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')



@app.route('/store')
def swastha_store():
    lang = request.args.get('lang', 'en')  # Default: English
    with open('store_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    products = data.get('products', [])
    return render_template('store.html', products=products, lang=lang)






def generate_diet(age, bmi, condition, lang='en'):
    plans = {
        "diabetes": {
            "en": "Low sugar diet with whole grains, lean proteins, and green vegetables.",
            "hi": "कम चीनी वाला आहार जिसमें साबुत अनाज, लीन प्रोटीन और हरी सब्जियां हों"
        },
        # add 9 more conditions (see earlier message)
        "general": {
            "en": "Balanced diet with fruits, vegetables, and water.",
            "hi": "फल, सब्ज़ियां और पानी के साथ संतुलित आहार"
        }
    }
    condition = condition.lower()
    if condition in plans:
        return plans[condition].get(lang, plans[condition]["en"])
    return plans["general"].get(lang)

@app.route("/diet", methods=["GET", "POST"])
def diet():
    diet_plan = None
    if request.method == "POST":
        age = int(request.form["age"])
        bmi = float(request.form["bmi"])
        condition = request.form["condition"]
        lang = request.form.get("language", "en")
        diet_plan = generate_diet(age, bmi, condition, lang)
    return render_template("diet.html", diet_plan=diet_plan)








with open("model/model.pkl", "rb") as f:
    model, symptom_labels = pickle.load(f)

@app.route('/disease_form')
def disease_form():
    return render_template('disease_form.html', all_symptoms=list(symptom_labels))

@app.route('/predict', methods=['POST'])
def predict():
    selected = request.form.getlist('symptoms')
    input_vector = [1 if s in selected else 0 for s in symptom_labels]
    prediction = model.predict([input_vector])[0]
    
    return render_template("disease_result.html", prediction=prediction, selected=selected)







@app.route('/pm')
def pm():
    return render_template('pm.html')

@app.route('/ab')
def ab():
    return render_template('ab.html')

@app.route('/video')
def video():
    return render_template('video.html')

@app.route('/js')
def js():
    return render_template('js.html')





@app.route('/indx')
def index():
    return render_template('indx.html')

@app.route('/check', methods=['POST'])
def check():
    image = request.files['image']
    if image.filename == '':
        return render_template('result.html', result="❌ No image uploaded.", sources=[])

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(filepath)

    img = Image.open(filepath)
    raw_text = pytesseract.image_to_string(img)
    cleaned_text = clean_text(raw_text)
    print("🔍 Extracted Text:", cleaned_text)

    is_genuine, sources = check_medicine_authenticity(cleaned_text)

    if not is_genuine:
        result = "❌ This doesn't appear to be a genuine or verified medicine."
    else:
        result = "✅ Genuine Medicine"

    return render_template('result.html', result=result, sources=sources)

def clean_text(text):
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def is_medicine_name(text):
    try:
        with open('medicines.txt', 'r') as f:
            medicine_list = [line.strip().lower() for line in f]
        return any(med in text.lower() for med in medicine_list)
    except:
        return False

def check_medicine_authenticity(text):
    sources = []
    keywords = " ".join(text.split()[:4])
    medicine_keywords = ['tablet', 'capsule', 'syrup', 'mg', 'injection', 'ointment', 'medicine', 'drug']

    if not any(word in text.lower() for word in medicine_keywords) and not is_medicine_name(text):
        return False, sources

    params = {
        "engine": "google",
        "q": f"{keywords} site:gov.in OR site:who.int OR site:fda.gov",
        "api_key": SERPAPI_KEY,
    }

    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        organic_results = results.get("organic_results", [])

        for result in organic_results:
            link = result.get("link", "")
            sources.append(link)

        return (len(sources) > 0), sources

    except Exception as e:
        print("🔍 Search failed:", e)
        return False, sources



APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, "data", "hacknavation.csv")

df = pd.read_csv(DATA_PATH).dropna()
required_cols = {"example", "response"}
if not required_cols.issubset(df.columns):
    raise ValueError("Expected columns 'example' and 'response' in hacknavation.csv")

# Load embedding model (small + fast, good accuracy)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Precompute embeddings for all examples
corpus = df["example"].astype(str).tolist()
corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)


def retrieve_response(query: str):
    """Retrieve best matching response from dataset using semantic similarity"""
    if not query or not query.strip():
        return {"answer": "Please say or type something.", "score": 0.0, "match": ""}

    # Encode query
    query_emb = embedder.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, corpus_embeddings)[0]

    # Get best match
    idx = int(scores.argmax())
    score = float(scores[idx])

    # Fallback if confidence is too low
    if score < 0.55:
        return {
            "answer": "I’m not fully sure I understood that. Could you rephrase?",
            "score": round(score, 4),
            "match": "",
        }

    answer = str(df.iloc[idx]["response"])
    match = str(df.iloc[idx]["example"])

    # Save context if follow-up columns exist
    follow_up_yes = str(df.iloc[idx].get("follow_up_yes", "")).strip() if "follow_up_yes" in df.columns else ""
    follow_up_no = str(df.iloc[idx].get("follow_up_no", "")).strip() if "follow_up_no" in df.columns else ""

    if follow_up_yes or follow_up_no:
        session["pending_followup"] = {
            "yes": follow_up_yes,
            "no": follow_up_no,
        }
        # Append follow-up question
        answer = f"{answer} Would you like me to help with this?"
    else:
        session.pop("pending_followup", None)

    return {"answer": answer, "score": round(score, 4), "match": match}


@app.route("/ai")
def ai_page():
    return render_template("ai.html")   # make an ai.html template



@app.post("/ask")
def ask():
    data = request.get_json(silent=True) or {}
    query = data.get("query", "").strip().lower()

    # ✅ Handle follow-ups if pending
    if session.get("pending_followup"):
        followup = session["pending_followup"]

        yes_words = {"yes", "yeah", "y", "sure", "ok", "okay"}
        no_words = {"no", "nah", "nope", "not now"}

        # Flexible matching (contains yes/no anywhere in input)
        if any(word in query for word in yes_words):
            answer = followup.get("yes", "Alright, let’s continue.")
            session.pop("pending_followup", None)
            return jsonify({"answer": answer, "score": 1.0, "match": "followup_yes"})

        elif any(word in query for word in no_words):
            answer = followup.get("no", "Okay, I understand.")
            session.pop("pending_followup", None)
            return jsonify({"answer": answer, "score": 1.0, "match": "followup_no"})

        # If not recognized as yes/no, clear follow-up and fall back
        session.pop("pending_followup", None)

    # ✅ Otherwise, do normal retrieval
    result = retrieve_response(query)
    return jsonify(result)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.route("/followup", methods=["POST"])
def followup():
    data = request.json
    choice = data.get("choice")

    if "pending_followup" not in session:
        return {"answer": "No follow-up pending."}

    followup_data = session.pop("pending_followup")

    if choice == "yes" and followup_data.get("yes"):
        return {"answer": followup_data["yes"]}
    elif choice == "no" and followup_data.get("no"):
        return {"answer": followup_data["no"]}
    else:
        return {"answer": "Okay, moving on."}
if __name__ == '__main__':
    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Get port from environment (Render sets this)
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)