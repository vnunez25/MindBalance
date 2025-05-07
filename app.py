from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import os

app = Flask(__name__)

# Use PostgreSQL database from Render environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text)

# Random mental health quotes
quotes = [
    "You don’t have to control your thoughts. You just have to stop letting them control you.",
    "It’s okay to not be okay.",
    "Slow down. You’re doing the best you can.",
    "Your mental health is more important than your productivity.",
    "You are enough. Exactly as you are.",
    "Healing is not linear. Be kind to yourself today."
]

# Homepage
@app.route('/')
def home():
    quote = random.choice(quotes)
    return render_template('index.html', quote=quote)

# Mood form
@app.route('/mood', methods=['GET', 'POST'])
def mood():
    if request.method == 'POST':
        selected_mood = request.form.get('mood', '').strip()
        custom_mood = request.form.get('custom_mood', '').strip()
        note = request.form.get('note', '').strip()

        final_mood = custom_mood if custom_mood else selected_mood

        if final_mood:
            new_entry = MoodEntry(mood=final_mood, note=note)
            db.session.add(new_entry)
            db.session.commit()

        return redirect(url_for('home'))

    return render_template('mood.html')

# Mood history
@app.route('/history')
def history():
    entries = MoodEntry.query.order_by(MoodEntry.id.desc()).all()
    return render_template('history.html', entries=entries)

# Create tables on app startup (even in deployment)
with app.app_context():
    db.create_all()



