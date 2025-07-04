from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import openai
import matplotlib.pyplot as plt
import uuid

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET', 'secret-key')

# Simple in-memory model database
MODELS = {
    'NeuViz ACE': {
        'door_width': 1200,
        'power_kva': 50,
        'room_height': 250,
    },
    'Brand X': {
        'door_width': 1100,
        'power_kva': 60,
        'room_height': 260,
    },
}

def engineer_required(func):
    def wrapper(*args, **kwargs):
        if session.get('role') != 'engineer':
            flash('Engineer role required.')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def login_required(func):
    def wrapper(*args, **kwargs):
        if 'role' not in session:
            flash('Please log in.')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@app.route('/')
def index():
    role = session.get('role')
    return render_template('index.html', models=MODELS.keys(), role=role)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        session['username'] = username
        session['role'] = role
        flash(f'Logged in as {username} ({role})')
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out')
    return redirect(url_for('index'))

@app.route('/compare', methods=['POST'])
@login_required
def compare():
    m1 = request.form.get('model1')
    m2 = request.form.get('model2')
    model1 = MODELS.get(m1)
    model2 = MODELS.get(m2)
    return render_template('compare.html', m1=m1, m2=m2, model1=model1, model2=model2)

@app.route('/conformity', methods=['GET', 'POST'])
@login_required
@engineer_required
def conformity():
    result = None
    chart = None
    if request.method == 'POST':
        door_width = int(request.form.get('door_width'))
        power_kva = int(request.form.get('power_kva'))
        room_height = int(request.form.get('room_height'))

        prompt = (
            f"Door width: {door_width} mm\nPower: {power_kva} kVA\nRoom height: {room_height} cm\n"
            "Check compliance with requirements: door >=1200mm, power>=50kVA, room height>=250cm."
        )
        openai.api_key = os.getenv('OPENAI_API_KEY')
        try:
            resp = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role': 'user', 'content': prompt}]
            )
            result = resp.choices[0].message['content']
        except Exception as e:
            result = f"Error contacting OpenAI: {e}"

        required = [1200, 50, 250]
        actual = [door_width, power_kva, room_height]
        labels = ['Door (mm)', 'Power (kVA)', 'Height (cm)']
        x = range(len(labels))
        plt.figure()
        plt.bar(x, required, width=0.4, label='Required')
        plt.bar([i + 0.4 for i in x], actual, width=0.4, label='Actual')
        plt.xticks([i + 0.2 for i in x], labels)
        plt.legend()
        fname = f"static/conformity_{uuid.uuid4().hex}.png"
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        chart = fname
    return render_template('conformity.html', result=result, chart=chart)

if __name__ == '__main__':
    app.run(debug=True)
