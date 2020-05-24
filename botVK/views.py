from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import json
import vk
import random
import os
import dialogflow
import database
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'web-gromily-ofrufe-751df123f0db.json'

DIALOGFLOW_PROJECT_ID = 'web-gromily-ofrufe'
DIALOGFLOW_LANGUAGE_CODE = 'ru'

token = os.getenv("VK_TOKEN")
session = vk.Session(access_token=token)
api = vk.API(session)
print("START")


# Create your views here.


@csrf_exempt
def bot(request):
    body = json.loads(request.body)
    if body == {"type": "confirmation", "group_id": 194135907}:
        return HttpResponse('2e71f495')

    if body['type'] == 'message_new':
        print(body['object']['message'])
        if body['object']['message'].get('payload'):
            user_id = body['object']['message']['from_id']
            payload = json.loads(body['object']['message'].get('payload'))
            if payload == {"command": "start"}:
                keyboard = getKeyboard()
                send(user_id, "Нажми на кнопку", json.dumps(keyboard))
            elif payload.get('button'):
                button = payload.get('button')
                if not database.get('user', 'id=' + str(user_id)):
                    database.insert('user', ['id', 'groupId'], [(user_id, button)])
                else:
                    database.update('user', ['groupId'], [button], 'id=' + str(user_id))
                send(user_id, "Спасибо за ответ")
        else:
            message = body['object']['message']['text']
            user_id = body['object']['message']['from_id']

            if len(message) > 0:
                session_client = dialogflow.SessionsClient()
                df_session = session_client.session_path(DIALOGFLOW_PROJECT_ID, user_id)
                text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
                query_input = dialogflow.types.QueryInput(text=text_input)
                try:
                    response = session_client.detect_intent(session=df_session, query_input=query_input)
                    if response.query_result.action == "update_group":
                        keyboard = getKeyboard()
                        send(user_id, response.query_result.fulfillment_text, json.dumps(keyboard))
                    else:
                        send(user_id, response.query_result.fulfillment_text)
                    print("Query text:", response.query_result.query_text)
                    print("intent/action:",
                          response.query_result.intent.display_name + "/" + response.query_result.action)
                    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
                    print("Fulfillment text:", response.query_result.fulfillment_text)
                except InvalidArgument:
                    raise
            else:
                send(user_id, "Ого, а где текст? Я такого не понимаю")

        return HttpResponse('ok')


def getKeyboard():
    keyboard = {
        'buttons': [
            [
                {'action': {'type': 'text', 'label': '   ', 'payload': """{"button": 1}"""},
                 'color': 'primary'},
                {'action': {'type': 'text', 'label': 'Не кнопка', 'payload': """{"button": 2}"""},
                 'color': 'positive'},
                {'action': {'type': 'text', 'label': 'Кнопка', 'payload': """{"button": 3}"""},
                 'color': 'negative'}
            ]
        ],
        'one_time': True}
    return keyboard


def send(user_id, message, keyboard=None):
    api.messages.send(v='5.103', user_id=user_id, message=message,
                      random_id=random.getrandbits(64), keyboard=keyboard)


# {'type': 'message_new', 'object': {'message': {'date': 1587272596, 'from_id': 190709425, 'id': 6, 'out': 0,
# 'peer_id': 190709425, 'text': 'qwe', 'conversation_message_id': 6, 'fwd_messages': [], 'important': False,
# 'random_id': 0, 'att achments': [], 'is_hidden': False}, 'client_info': {'button_actions': ['text', 'vkpay',
# 'open_app', 'location', 'open_link'], 'keyboard': True, 'inline_keyboard': True, 'lang_id': 0}}, 'group_id':
# 194135907, 'event_id': 'f79b505cdc0907 3286cdb6fe61376dda50225e80'}

lg = {
    'success': False
}


def login(request):
    global lg

    print(request.POST)
    if request.POST.get('login') == 'admin' and request.POST.get('pass') == '123':
        print("sadasd")
        lg['success'] = True
        lg['groups'] = database.get('groups')
    elif 'spam' in request.POST:
        group = request.POST.get('group')
        message = request.POST.get('message')
        for user in database.get('user', 'groupId=' + group):
            send(user[0], message)
    return render(request, "login.html", lg)
