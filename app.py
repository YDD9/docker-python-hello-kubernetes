from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    # it is return not print
    return "Hello World!"

if __name__ == "__main__":
    # without port 8080, port 5000 will be used by Flask
    # it is listenning port for web connection
    app.run(host='0.0.0.0', port=8080)