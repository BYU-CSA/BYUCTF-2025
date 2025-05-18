# imports
from flask import Flask, request, redirect, make_response, jsonify
import jwt, os


# initialize flask
app = Flask(__name__)
FLAG = open('flag.txt', 'r').read()
APP_SECRET = os.urandom(32).hex()
ADMIN_SECRET = os.urandom(32).hex()
print(f'ADMIN_SECRET: {ADMIN_SECRET}')


# JRL - JWT Revocation List
jrl = [
    jwt.encode({"admin": True, "uid": '1337'}, APP_SECRET, algorithm="HS256")
]


# main
@app.route('/', methods=['GET'])
def main():
    resp = make_response('Hello World!')
    resp.set_cookie('session', jwt.encode({"admin": False}, APP_SECRET, algorithm="HS256"))
    return resp

# get admin cookie if you know the secret
@app.route('/get_admin_cookie', methods=['GET'])
def get_admin_cookie():
    secret = request.args.get('adminsecret', None)
    uid = request.args.get('uid', None)

    if secret is None or uid is None or uid == '1337':
        return redirect('/')

    if secret == ADMIN_SECRET:
        resp = make_response('Cookie has been set.')
        resp.set_cookie('session', jwt.encode({"admin": True, "uid": uid}, APP_SECRET, algorithm="HS256"))
        return resp

# get flag if you are an admin
@app.route('/flag', methods=['GET'])
def flag():
    session = request.cookies.get('session', None).replace('=','').strip()

    if session is None:
        return redirect('/')
    
    # check if the session is in the JRL
    if session in jrl:
        return redirect('/')

    try:
        payload = jwt.decode(session, APP_SECRET, algorithms=["HS256"])
        if payload['admin'] == True:
            return FLAG
        else:
            return redirect('/')
    except:
        return redirect('/')

# retrieve the JRL
@app.route('/jrl', methods=['GET'])
def jrl_endpoint():
    return jsonify(jrl)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337, threaded=True)