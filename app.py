from flask import Flask
app = Flask(__name__)
# single Flask one page HTML
# http://www.compjour.org/lessons/flask-single-page/
# http://flask.pocoo.org/docs/0.10/quickstart/#rendering-templates
import os

# portable way to get hostname on windows or linux
import socket
currHost = socket.gethostbyaddr(socket.gethostname())[0]

@app.route("/")
def hello():
    # os.getenv get hosting container env variable(which defined in kubernetes pod.yml).
    # https://stackoverflow.com/questions/4906977/access-environment-variables-from-python
    msg = "Hello World! FROM " + currHost + " " +\
            os.getenv('PYTHON_HELLO_NODE_NAME', ' ') +\
            os.getenv('PYTHON_HELLO_POD_NAME', ' ') +\
            os.getenv('PYTHON_HELLO_POD_NAMESPACE', ' ') +\
            os.getenv('PYTHON_HELLO_POD_IP', ' ') +\
            os.getenv('PYTHON_HELLO_POD_SERVICE_ACCOUNT', ' ')

    # must use return not print
    return msg

@app.route('/dev')
def dev():
    return 'Dev page FROM ' + currHost + ' ' + os.getenv('PYTHON_HELLO_POD_NAME', ' ')

# @app.route('/test')
# def test():
#     return 'Test page FROM ' + currHost + ' ' + os.getenv('PYTHON_HELLO_POD_NAME', ' ')

@app.route('/prod')
def prod():
    return 'Prod page FROM ' + currHost + ' ' + os.getenv('PYTHON_HELLO_POD_NAME', ' ')

if __name__ == "__main__":
    # without port 8080, port 5000 will be used by Flask
    # it is listenning port for web connection
    app.run(host='0.0.0.0', port=8080)