import vk_api
import json
from vk_api.vk_api import VkApiMethod
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

token = "92cbfb70aa304a39ba49a4359f5c53487368e80c3d17f729c4748a1f2109f69341c0a319b9ba573af03d5"

vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': get_random_id()})
def game_citi(city):
    VkApiMethod('database.getCities',{'country_id': 1, 'q': city, 'count': 1})


keyboard_choose_game = {
    'one_time': False,
    'buttons': [[{
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '1'}),
            'label': 'Угайдай число',
        },
        'color': 'primary'
    },
    {
        'action': {
            'type': 'text',
            'payload': json.dumps({'buttons': '2'}),
            'label': 'Города',
        },
        'color': 'primary'
    }
    ]]
}
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        text_user = event.text
        if text_user == 'привет':
            write_msg(event.user_id, "Хай")
        if text_user == 'удали':
            vk.method('messages.send', {
                'user_id': event.user_id,
                'message': "Нет",
                'random_id': get_random_id(),
                'keyboard': str(json.dumps(keyboard_choose_game, ensure_ascii=False))
            })
        if text_user == 'Города':
            vk.method('database.getCities', {
                'country_id': 1
            })