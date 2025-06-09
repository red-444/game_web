from flask import Flask, render_template, request, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'

TOTAL_ATTEMPTS = 7  # You can change this value

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'number' not in session:
        session['number'] = random.randint(1, 100)
        session['attempts'] = TOTAL_ATTEMPTS

    message = ""

    if request.method == 'POST':
        try:
            guess = int(request.form['guess'])
        except ValueError:
            message = "⚠️ Please enter a valid number."
            return render_template('index.html', message=message, attempts=session['attempts'])

        session['attempts'] -= 1
        attempts_used = TOTAL_ATTEMPTS - session['attempts']

        if guess == session['number']:
            message = f"🎉 Correct! The number was {session['number']}. You guessed it in {attempts_used} attempt(s)."
            session.clear()
        elif session['attempts'] == 0:
            message = f"❌ Game over! The number was {session['number']}. You used all {TOTAL_ATTEMPTS} attempts."
            session.clear()
        elif guess < session['number']:
            message = "🔼 Try a higher number."
        else:
            message = "🔽 Try a lower number."

    return render_template('index.html', message=message, attempts=session.get('attempts', 0))

if __name__ == '__main__':
    app.run(debug=True)
