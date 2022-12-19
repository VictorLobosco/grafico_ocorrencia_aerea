from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)