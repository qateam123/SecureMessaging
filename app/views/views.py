from app import app
from flask import request, redirect, json
from flask import render_template, jsonify
import requests
from app import settings
import sys
from app.forms import MessageForm


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/new-message', methods=['GET', 'POST'])
def dev_mode():
    form = MessageForm(request.form)

    if request.method == 'POST' and form.validate():
        to_input = request.form['to_input']
        from_input = request.form['from_input']
        message_input = request.form['message_input']
        url = settings.SECURE_MESSAGING_API_URL
        data = {'to': request.form['to_input'], 'from': request.form['from_input'], 'body': request.form['message_input']}
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print (to_input, from_input, message_input, file=sys.stderr)
        #if to_input == "":

    return render_template('secure-messaging/new-message.html', form=form)
        # user = request.form
        # url = settings.SECURE_MESSAGING_API_URL
        # data = {'to': user.get("to"), 'from': user.get("from"), 'body': user.get("msg")}
        # headers = {'Content-Type': 'application/json'}
        # print(data, file=sys.stderr)
        # r = requests.post(url, data=json.dumps(data), headers=headers)
        # print(r.text, file=sys.stderr)
        # return render_template("secure-messaging/sent-message.html")
        #return redirect("/validate?msg=" + message)
    # return render_template("secure-messaging/new-message.html",
    #                       form=form)

@app.route('/validate', methods=['GET'])
def validate():
    message = request.args.get('msg')
    if not message:
        return jsonify(msgValid=False, msg="empty")
    else:
        return jsonify(msgValid=True, msg=message)
