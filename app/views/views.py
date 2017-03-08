from app import app
from flask import request, redirect, json
from flask import render_template, jsonify
import requests
from app import settings
import sys


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/newmessage', methods=['GET', 'POST'])
def dev_mode():
    if request.method == 'POST':
        user = request.form
        url = settings.SECURE_MESSAGING_API_URL
        data = {'to': user.get("to"), 'from': user.get("from"), 'body': user.get("msg")}
        headers = {'Content-Type': 'application/json'}
        print(data, file=sys.stderr)
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print(r.text, file=sys.stderr)
        return r.text
        #return redirect("/validate?msg=" + message)
    return render_template("new-message.html")


@app.route('/validate', methods=['GET'])
def validate():
    message = request.args.get('msg')
    if not message:
        return jsonify(msgValid=False, msg="empty")
    else:
        return jsonify(msgValid=True, msg=message)
