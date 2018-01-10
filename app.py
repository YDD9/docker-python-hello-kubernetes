from flask import Flask
app = Flask(__name__)

import os

@app.route("/")
def hello():

    # os.getenv get hosting container env variable(user defined env via k8s pod), if not found, give "".
    # https://stackoverflow.com/questions/4906977/access-environment-variables-from-python
    msg = "Hello World!\n" +\
            os.getenv('PYTHON_HELLO_NODE_NAME', '') + '\n' +\
            os.getenv('PYTHON_HELLO_POD_NAME', '') + '\n' +\
            os.getenv('PYTHON_HELLO_POD_NAMESPACE', '') + '\n' +\
            os.getenv('PYTHON_HELLO_POD_IP', '') + '\n' +\
            os.getenv('PYTHON_HELLO_POD_SERVICE_ACCOUNT', '') + '\n'

    # must use return not print
    return msg

if __name__ == "__main__":
    # without port 8080, port 5000 will be used by Flask
    # it is listenning port for web connection
    app.run(host='0.0.0.0', port=8080)