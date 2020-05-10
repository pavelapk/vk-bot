from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render
import json
import vk
import random
import os
import dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'web-gromily-ofrufe-751df123f0db.json'

DIALOGFLOW_PROJECT_ID = 'web-gromily-ofrufe'
DIALOGFLOW_LANGUAGE_CODE = 'ru'
SESSION_ID = 'me'

session_client = dialogflow.SessionsClient()
df_session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)

token = os.getenv("VK_TOKEN")
session = vk.Session(access_token=token)
api = vk.API(session)
print("START")


# Create your views here.


@csrf_exempt
def bot(request):
    body = json.loads(request.body)
    if body == {"type": "confirmation", "group_id": 194135907}:
        return HttpResponse('2344e407')

    if body['type'] == 'message_new':
        print(body['object']['message'])
        message = body['object']['message']['text']
        user_id = body['object']['message']['from_id']

        if len(message) > 0:
            text_input = dialogflow.types.TextInput(text=message, language_code=DIALOGFLOW_LANGUAGE_CODE)
            query_input = dialogflow.types.QueryInput(text=text_input)
            try:
                response = session_client.detect_intent(session=df_session, query_input=query_input)
                send(user_id, response.query_result.fulfillment_text)
            except InvalidArgument:
                raise
        else:
            send(user_id, "Ого, а где текст? Я такого не понимаю")
        # print("Query text:", response.query_result.query_text)
        # print("Detected intent:", response.query_result.intent.display_name)
        # print("Detected intent confidence:", response.query_result.intent_detection_confidence)
        # print("Fulfillment text:", response.query_result.fulfillment_text)

        return HttpResponse('ok')


def send(user_id, message):
    api.messages.send(v='5.103', user_id=user_id, message=message,
                      random_id=random.getrandbits(64))

# {'type': 'message_new', 'object': {'message': {'date': 1587272596, 'from_id': 190709425, 'id': 6, 'out': 0,
# 'peer_id': 190709425, 'text': 'qwe', 'conversation_message_id': 6, 'fwd_messages': [], 'important': False,
# 'random_id': 0, 'att achments': [], 'is_hidden': False}, 'client_info': {'button_actions': ['text', 'vkpay',
# 'open_app', 'location', 'open_link'], 'keyboard': True, 'inline_keyboard': True, 'lang_id': 0}}, 'group_id':
# 194135907, 'event_id': 'f79b505cdc0907 3286cdb6fe61376dda50225e80'}
