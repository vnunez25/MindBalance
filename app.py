from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

# ✅ Use DATABASE_URL from Render (fix prefix for SQLAlchemy)
uri = os.environ.get("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ✅ Initialize database
db = SQLAlchemy(app)

# ✅ MoodEntry model
class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(100), nullable=False)
    note = db.Column(db.Text)

# ✅ Random wellness quotes
quotes = [
    "You don’t have to control your thoughts. You just have to stop letting them control you.",
    "It’s okay to not be okay.",
    "Slow down. You’re doing the best you can.",
    "Your mental health is more important than your productivity.",
    "You are enough. Exactly as you are.",
    "Healing is not linear. Be kind to yourself today."
]

# ✅ Home page
@app.route('/')
def home():
    quote = random.choice(quotes)
    return render_template('index.html', quote=quote)

# ✅ Mood form page
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

# ✅ Mood history page
@app.route('/history')
def history():
    entries = MoodEntry.query.order_by(MoodEntry.id.desc()).all()
    return render_template('history.html', entries=entries)

# ✅ Create database tables on startup (for Render)
with app.app_context():
    db.create_all()



