from flask import Flask, render_template, request, redirect, url_for
import requests

BACKEND_URL = 'http://127.0.0.1:3000'

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    age = request.form.get('age')

    if not name or not age:
        return render_template('index.html', error="Both name and age are required!")

    form_data = {'name': name, 'age': age}

    # Send the POST request to the backend 
    response = requests.post(f"{BACKEND_URL}/submit", json=form_data)

    if response.status_code == 200:
        return redirect(url_for('success'))
    else:
        try:
            error_msg = response.json().get('error', 'Unknown error')
        except ValueError:
            error_msg = "Backend returned invalid response."
        return render_template('index.html', error=error_msg)

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
