from flask import Flask, render_template, request
import os
import openai

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html', models=MODELS.keys())

@app.route('/compare', methods=['POST'])
def compare():
    m1 = request.form.get('model1')
    m2 = request.form.get('model2')
    model1 = MODELS.get(m1)
    model2 = MODELS.get(m2)
    return render_template('compare.html', m1=m1, m2=m2, model1=model1, model2=model2)

@app.route('/conformity', methods=['GET', 'POST'])
def conformity():
    result = None
    if request.method == 'POST':
        door_width = request.form.get('door_width')
        power_kva = request.form.get('power_kva')
        room_height = request.form.get('room_height')
        prompt = f"Door width: {door_width} mm\nPower: {power_kva} kVA\nRoom height: {room_height} cm\n" \
                 "Check compliance with requirements: door >=1200mm, power>=50kVA, room height>=250cm."
        openai.api_key = os.getenv('OPENAI_API_KEY')
        try:
            resp = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[{'role':'user','content':prompt}]
            )
            result = resp.choices[0].message['content']
        except Exception as e:
            result = f"Error contacting OpenAI: {e}"
    return render_template('conformity.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
