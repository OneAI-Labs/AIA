from flask import Flask

app = Flask(__name__)  # Create Flask app instance

@app.route("/")
def home():
    return "Hello, Flask is running!"

if __name__ == "__main__":
    app.run(debug=True)
 
