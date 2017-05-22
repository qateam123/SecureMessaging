from app import app
from flask import request, redirect, json, g, url_for
from flask import render_template, jsonify
import requests
from app import settings
from app.forms import MessageForm, DraftForm
from app.authentication.jwt import encode
from app.authentication.jwe import Encrypter
import logging

logger = logging.getLogger(__name__)
token_data = {
            "user_urn": "0000"
        }

headers = {'Content-Type': 'application/json', 'Authorization': ''}


def update_encrypted_jwt():
    encrypter = Encrypter(_private_key=settings.SM_USER_AUTHENTICATION_PRIVATE_KEY,
                          _private_key_password=settings.SM_USER_AUTHENTICATION_PRIVATE_KEY_PASSWORD,
                          _public_key=settings.SM_USER_AUTHENTICATION_PUBLIC_KEY)
    signed_jwt = encode(token_data)
    return encrypter.encrypt_token(signed_jwt)

headers['Authorization'] = update_encrypted_jwt()

modify_data = {'action': '',
               'label': ''}


def check_login():
    if token_data['user_urn'] == "0000":
        return redirect(url_for('login'))


def add_messages():
    headers['Authorization'] = update_encrypted_jwt()
    sample_data = {'urn_to': token_data['user_urn'],
                   'urn_from': 'internal.789',
                   'subject': 'Notorious Toddlers',
                   'body': 'Big Gains',
                   'thread_id': '',
                   'collection_case': 'CCtest',
                   'reporting_unit': 'RUtest',
                   'survey': 'BRES'}
    for x in range(0, 2):
        requests.post(url=settings.SECURE_MESSAGING_API_URL + settings.SM_SEND_MESSAGE_URL, data=json.dumps(sample_data), headers=headers)


@app.route('/index')
def index():
    add_messages()
    return "Hello, World!"


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        token_data['user_urn'] = request.form['submit']
        headers['Authorization'] = update_encrypted_jwt()
        return redirect("http://localhost:5000/messages")
    return render_template("/secure-messaging/login.html")


@app.route('/new-message/<thread_id>', methods=['GET', 'POST'])
@app.route('/new-message', methods=['GET', 'POST'], defaults={'thread_id': ''})
def dev_mode(thread_id):
    check_login()
    form = MessageForm(request.form)
    headers['Authorization'] = update_encrypted_jwt()
    if request.method == 'POST' and form.validate():
        url = settings.SECURE_MESSAGING_API_URL
        if request.form['submit'] == 'Send Message':
            return send_message(request.form, url, thread_id)
        elif request.form['submit'] == 'Save as Draft':
            return save_draft(request.form, url, thread_id)

    return render_template('secure-messaging/new-message.html', form=form, user_urn=token_data['user_urn'])


@app.route('/messages/<label>', methods=['GET', 'POST'])
@app.route('/messages', methods=['GET', 'POST'])
def get_msgs(label=None):
    check_login()
    if request.method == 'GET':
        url = settings.SECURE_MESSAGING_API_URL + settings.SM_GET_MESSAGES_URL
        headers['Authorization'] = update_encrypted_jwt()
        if label is not None:
            url = url + "?label=" + label
        if 'internal' in token_data['user_urn']:
            if label is not None:
                url = url + "&survey=BRES"
            else:
                url = url + "?survey=BRES"
        resp = requests.get(url, headers=headers)
        resp_data = json.loads(resp.text)
        links = resp_data['_links']
    else:
        headers['Authorization'] = update_encrypted_jwt()
        url = request.form['submit']
        if label is not None:
            url = url + "&label=" + label
        if 'internal' in token_data['user_urn']:
            url = url + "&survey=BRES"
        resp = requests.get(url, headers=headers)
        resp_data = json.loads(resp.text)
        links = resp_data['_links']
    return render_template("secure-messaging/messages.html", messages=resp_data['messages'], links=links)


@app.route('/message/<message_id>', methods=['GET'])
def get_msg(message_id):
    check_login()
    url = settings.SECURE_MESSAGING_API_URL + settings.SM_GET_MESSAGE_URL.format(message_id)
    headers['Authorization'] = update_encrypted_jwt()
    resp = requests.get(url, headers=headers)
    response = json.loads(resp.text)
    if 'UNREAD' in response['labels']:
        modify_data['action'] = 'remove'
        modify_data['label'] = 'UNREAD'
        requests.put(url=settings.SECURE_MESSAGING_API_URL + settings.SM_MODIFY_MESSAGE_URL.format(message_id), data=json.dumps(modify_data), headers=headers)
    return render_template("secure-messaging/message.html", message=response)


@app.route('/message/<message_id>/edit', methods=['GET', 'POST'])
def edit_msg(message_id):
    check_login()
    label = request.args.get('label')
    headers['Authorization'] = update_encrypted_jwt()
    url = settings.SECURE_MESSAGING_API_URL + settings.SM_MODIFY_MESSAGE_URL.format(message_id)
    if label == 'READ':
        modify_data['action'] = 'remove'
        modify_data['label'] = 'UNREAD'
    elif label == 'UNREAD':
        modify_data['action'] = 'add'
        modify_data['label'] = 'UNREAD'
    requests.put(url, data=json.dumps(modify_data), headers=headers)
    return redirect("http://localhost:5000/" + settings.SM_GET_MESSAGES_URL)


@app.route('/draft/<draft_id>', methods=['GET'])
def get_draft(draft_id):
    check_login()
    headers['Authorization'] = update_encrypted_jwt()
    url = settings.SECURE_MESSAGING_API_URL + settings.SM_GET_DRAFT_URL.format(draft_id)
    resp = requests.get(url, headers=headers)
    response = json.loads(resp.text)
    return render_template("secure-messaging/draft.html", draft=response)


@app.route('/draft/<draft_id>/modify', methods=['GET', 'POST'])
def edit_draft(draft_id):
    check_login()
    headers['Authorization'] = update_encrypted_jwt()
    resp = requests.get(settings.SECURE_MESSAGING_API_URL + settings.SM_GET_DRAFT_URL.format(draft_id), headers=headers)
    resp_data = json.loads(resp.text)
    form = DraftForm(request.form)
    form.urn_to.data = resp_data['urn_to']
    form.subject.data = resp_data['subject']
    form.body.data = resp_data['body']

    if request.method == 'POST':
        url = settings.SECURE_MESSAGING_API_URL
        if request.form['submit'] == 'Send Message':
            return send_message(request.form, url, resp_data['thread_id'])
        elif request.form['submit'] == 'Save as Draft':
            return modify_draft(request.form, url, resp_data['thread_id'])

    return render_template('secure-messaging/draft-edit.html', form=form)


@app.route('/validate', methods=['GET'])
def validate():
    message = request.args.get('msg')
    if not message:
        return jsonify(msgValid=False, msg="empty")
    else:
        return jsonify(msgValid=True, msg=message)


def send_message(form, url, thread_id):
    headers['Authorization'] = update_encrypted_jwt()
    data = {'urn_to': form['to_input'], 'urn_from': token_data['user_urn'], 'subject': form['subject_input'],
            'body': form['message_input'], 'thread_id': thread_id, 'collection_case': 'testCC', 'reporting_unit': 'testRU', 'survey': 'BRES'}
    response = requests.post(url+settings.SM_SEND_MESSAGE_URL, data=json.dumps(data), headers=headers)
    resp_data = json.loads(response.text)
    logger.info(response.status_code, resp_data['msg_id'])
    return render_template("secure-messaging/sent-message.html", code=201)


def save_draft(form, url, thread_id):
    headers['Authorization'] = update_encrypted_jwt()
    data = {'urn_to': form['to_input'], 'urn_from': token_data['user_urn'], 'subject': form['subject_input'],
            'body': form['message_input'], 'thread_id': thread_id, 'collection_case': 'testCC', 'reporting_unit': 'testRU', 'survey': 'BRES'}
    response = requests.post(url + settings.SM_SAVE_DRAFT_URL, data=json.dumps(data), headers=headers)
    resp_data = json.loads(response.text)
    logger.info(response.status_code, resp_data['msg_id'])
    return render_template("secure-messaging/save-draft.html", code=201)


def modify_draft(form, url, thread_id):
    headers['Authorization'] = update_encrypted_jwt()
    modify_draft_data = {'urn_to': form['urn_to'], 'urn_from': token_data['user_urn'], 'subject': form['subject'],
                         'body': form['body'], 'thread_id': thread_id, 'collection_case': 'testCC', 'reporting_unit': 'testRU', 'survey': 'BRES'}
    response = requests.put(url + settings.SM_SAVE_DRAFT_URL, data=json.dumps(modify_draft_data), headers=headers)
    resp_data = json.loads(response.text)
    logger.info("1")
    return render_template("secure-messaging/save-draft.html", code=201)
