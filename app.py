appfrom flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import os
import random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "my_secret_cookie"  # Change this to anything yummy!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ketocoach.db'
db = SQLAlchemy(app)

# Simple database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    plan = db.Column(db.String(20), default='free')

class MealLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    meal = db.Column(db.String(500))
    ai_feedback = db.Column(db.String(1000))

# Setup database
with app.app_context():
    db.create_all()

# Fake AI responses (like fortune cookies!)
def generate_ai_response(meal):
    responses = [
        f"Great choice! {meal} is perfect for ketosis 🌟",
        f"{meal}? Excellent fat content for energy! 💪",
        f"Yum! {meal} will keep you in fat-burning mode 🔥",
        f"Pro tip: Add avocado to {meal} for extra healthy fats 🥑"
    ]
    return random.choice(responses)

# Website routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()
    session['user_id'] = new_user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    
    user_id = session['user_id']
    meals = MealLog.query.filter_by(user_id=user_id).all()
    
    return render_template('dashboard.html', meals=meals)

@app.route('/log_meal', methods=['POST'])
def log_meal():
    meal = request.form['meal']
    feedback = generate_ai_response(meal)
    
    new_log = MealLog(
        user_id=session['user_id'],
        meal=meal,
        ai_feedback=feedback
    )
    db.session.add(new_log)
    db.session.commit()
    
    return f"""
    <div style='background:#06d6a010; padding:1rem; border-radius:10px; border-left:3px solid #06d6a0; margin-top:1rem'>
      <strong>🧠 AI Coach:</strong> {feedback}
    </div>
    """

@app.route('/upgrade')
def upgrade():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
.py
