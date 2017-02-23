from app import app
from flask import request, redirect
from flask import render_template, jsonify

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/dev', methods=['GET', 'POST'])
def dev_mode():
    if request.method == 'POST':
        user = request.form
        username = user.get("username")
        return redirect("/validate?username=" + username)
    return render_template("dev.html")

@app.route('/validate', methods=['GET'])
def validate():
    username = request.args.get('username')
    if not username:
        return jsonify(usernameValid=False)
    else:
        return jsonify(usernameValid=True)
