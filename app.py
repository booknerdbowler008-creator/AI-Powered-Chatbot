from flask import Flask, render_template, request
import sqlite3
from faq import faq
app = Flask(__name__)
conn = sqlite3.connect('chatbot.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS logs(
id INTEGER PRIMARY KEY AUTOINCREMENT,
question TEXT,
answer TEXT
)''')
conn.commit()
conn.close()
@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        user_input = request.form["message"].lower()
        response = faq.get(
            user_input,
            "Sorry, I didn't understand."
        )
        conn = sqlite3.connect('chatbot.db')
        c = conn.cursor()
        c.execute(
            "INSERT INTO logs(question, answer) VALUES (?, ?)",
            (user_input, response)
        )
        conn.commit()
        conn.close()
    return render_template(
        "index.html",
        response=response
    )
if __name__ == "__main__":
    app.run(debug=True)