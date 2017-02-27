from app import app
from flask import request, redirect
from flask import render_template, jsonify


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


@app.route('/message', methods=['GET', 'POST'])
def dev_mode():
    if request.method == 'POST':
        user = request.form
        message = user.get("msg")
        return redirect("/validate?msg=" + message)
    return render_template("message.html")


@app.route('/validate', methods=['GET'])
def validate():
    message = request.args.get('msg')
    if not message:
        return jsonify(msgValid=False, msg="empty")
    else:
        return jsonify(msgValid=True, msg=message)
