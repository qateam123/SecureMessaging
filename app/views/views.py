from app import app
from flask import request, redirect, json
from flask import render_template, jsonify
import requests
from app import settings
import sys
from app.forms import MessageForm
from app.authentication.jwt import encode
from app.authentication.jwe import Encrypter
import logging

logger = logging.getLogger(__name__)
token_data = {
            "user_urn": "respondent.12345678910"
        }
encrypter = Encrypter(_private_key=settings.SM_USER_AUTHENTICATION_PRIVATE_KEY,
                      _private_key_password=settings.SM_USER_AUTHENTICATION_PRIVATE_KEY_PASSWORD,
                      _public_key=settings.SM_USER_AUTHENTICATION_PUBLIC_KEY)
signed_jwt = encode(token_data)
encrypted_jwt = encrypter.encrypt_token(signed_jwt)
headers = {'Content-Type': 'application/json', 'authentication': encrypted_jwt}

modify_data = {'action': '',
               'label': ''}


def add_messages():
    sample_data = {'urn_to': token_data['user_urn'],
                   'urn_from': 'internal.789',
                   'subject': 'Notorious Toddlers',
                   'body': 'Big Gains',
                   'thread_id': '',
                   'collection_case': 'CCtest',
                   'reporting_unit': 'RUtest',
                   'survey': 'RSI'}
    for x in range(0, 2):
        requests.post(url=settings.SECURE_MESSAGING_API_URL + settings.SM_SEND_MESSAGE_URL, data=json.dumps(sample_data), headers=headers)


@app.route('/')
@app.route('/index')
def index():
    add_messages()
    return "Hello, World!"


@app.route('/new-message', methods=['GET', 'POST'])
def dev_mode():
    form = MessageForm(request.form)

    if request.method == 'POST' and form.validate():

        url = settings.SECURE_MESSAGING_API_URL
        if request.form['submit'] == 'Send Message':
            return send_message(request.form, url)
        elif request.form['submit'] == 'Save as Draft':
            return save_draft(request.form, url)

    return render_template('secure-messaging/new-message.html', form=form)


@app.route('/messages', methods=['GET'])
def get_msgs():
    url = settings.SECURE_MESSAGING_API_URL + settings.SM_GET_MESSAGES_URL
    resp = requests.get(url, headers=headers)
    resp_data = json.loads(resp.text)
    return render_template("secure-messaging/messages.html", messages=resp_data['messages'])


@app.route('/message/<message_id>', methods=['GET'])
def get_msg(message_id):
    url = settings.SECURE_MESSAGING_API_URL + settings.SM_GET_MESSAGE_URL.format(message_id)
    resp = requests.get(url, headers=headers)
    response = json.loads(resp.text)
    if 'UNREAD' in response['labels']:
        modify_data['action'] = 'remove'
        modify_data['label'] = 'UNREAD'
        requests.put(url=settings.SECURE_MESSAGING_API_URL + settings.SM_MODIFY_MESSAGE_URL.format(message_id), data=json.dumps(modify_data), headers=headers)
    return render_template("secure-messaging/message.html", message=response)


@app.route('/message/<message_id>/edit', methods=['GET', 'POST'])
def edit_msg(message_id):
    label = request.args.get('label')
    url = settings.SECURE_MESSAGING_API_URL + settings.SM_MODIFY_MESSAGE_URL.format(message_id)
    if label == 'READ':
        modify_data['action'] = 'remove'
        modify_data['label'] = 'UNREAD'
    elif label == 'UNREAD':
        modify_data['action'] = 'add'
        modify_data['label'] = 'UNREAD'
    requests.put(url, data=json.dumps(modify_data), headers=headers)
    return redirect("http://localhost:5000/" + settings.SM_GET_MESSAGES_URL)


@app.route('/validate', methods=['GET'])
def validate():
    message = request.args.get('msg')
    if not message:
        return jsonify(msgValid=False, msg="empty")
    else:
        return jsonify(msgValid=True, msg=message)


def send_message(form, url):
    data = {'urn_to': form['to_input'], 'urn_from': token_data['user_urn'], 'subject': form['subject_input'],
            'body': form['message_input'], 'thread_id': '', 'collection_case': 'testCC', 'reporting_unit': 'testRU', 'survey': 'testSurvey'}
    response = requests.post(url+settings.SM_SEND_MESSAGE_URL, data=json.dumps(data), headers=headers)
    resp_data = json.loads(response.text)
    logger.info(response.status_code, resp_data['msg_id'])
    return render_template("secure-messaging/sent-message.html", code=201)


def save_draft(form, url):
    data = {'urn_to': form['to_input'], 'urn_from': token_data['user_urn'], 'subject': form['subject_input'],
            'body': form['message_input'], 'thread_id': '', 'collection_case': 'testCC', 'reporting_unit': 'testRU', 'survey': 'testSurvey'}
    response = requests.post(url + settings.SM_SAVE_DRAFT_URL, data=json.dumps(data), headers=headers)
    resp_data = json.loads(response.text)
    logger.info(response.status_code, resp_data['msg_id'])
    return render_template("secure-messaging/save-draft.html", code=201)
