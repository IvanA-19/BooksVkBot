# Importing libraries
import json

from config import *
from db_handler import check_member, add_member, remove_member
from vk_api.bot_longpoll import VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
import requests


# Sending message via bot
def write_message(send_id: int, message: str, keyboard=None, attachment=None) -> None:
    data = {'peer_id': send_id, 'message': message, 'random_id': get_random_id()}
    if keyboard is not None:
        data['keyboard'] = keyboard.get_keyboard()
    if attachment is not None:
        data['attachment'] = attachment
    api.method('messages.send', data)


# Getting of sending file
def get_sending_file(event, filename: str, path_to_file="") -> str:
    file = open(f'{path_to_file}/{filename}', 'rb')
    result = json.loads(requests.post(
        vk.docs.getMessagesUploadServer(type='doc', peer_id=event.object.peer_id)['upload_url'],
        files={'file': file}).text)
    jsonAnswer = vk.docs.save(file=result['file'], title=f'{filename}', tags=[])

    return f"doc{jsonAnswer['doc']['owner_id']}_{jsonAnswer['doc']['id']}"


# Message editing
def edit_message(event, text: str) -> None:
    vk.messages.edit(
        peer_id=event.object.peer_id,
        message=text,
        conversation_message_id=event.object.conversation_message_id,
    )


# Getting keyboard
def get_keyboard(callback_characters, callback_about):
    keyboard = VkKeyboard(inline=True)
    keyboard.add_callback_button(
        label='Персонажи',
        color=VkKeyboardColor.POSITIVE,
        payload={'type': 'my_own_100500_type_edit', f'text': f'{callback_characters}'})
    keyboard.add_callback_button(
        label='О романе',
        color=VkKeyboardColor.PRIMARY,
        payload={'type': 'my_own_100500_type_edit', f'text': f'{callback_about}'})
    keyboard.add_line()
    keyboard.add_callback_button(
        label='Меню',
        color=VkKeyboardColor.NEGATIVE,
        payload={'type': 'my_own_100500_type_edit', f'text': f'{'Меню'}'})
    return keyboard


# Getting menu keyboard
def get_menu_keyboard():
    keyboard = VkKeyboard(one_time=True)
    buttons = ["Выбрать произведение", "Контакты", "Назад"]
    color = VkKeyboardColor.POSITIVE
    for i, button in enumerate(buttons):
        match i:
            case 1:
                color = VkKeyboardColor.PRIMARY

            case 2:
                color = VkKeyboardColor.NEGATIVE
        keyboard.add_button(button, color)
        if i < len(buttons) - 1:
            keyboard.add_line()
    return keyboard


# Getting keyboard for open menu
def get_open_menu_keyboard():
    keyboard = VkKeyboard()
    keyboard.add_button("Меню", VkKeyboardColor.POSITIVE)
    return keyboard


# Main circle
def check_events() -> None:
    for event in long_poll.listen():
        # Answering on message from user
        if event.type == VkBotEventType.MESSAGE_NEW:
            if event.object.message['text'].lower() == 'Hello'.lower():
                write_message(event.object.message['peer_id'], "Hello! Welcome to our group!")
            elif "Меню".lower() in event.object.message['text'].lower():
                if check_member(event.object.message['from_id']):
                    keyboard = get_menu_keyboard()
                    write_message(event.object.message['peer_id'],
                                  "Спасибо, за подписку!\nВыберите, что вы хотите сделать", keyboard)
                else:
                    write_message(event.object.message['peer_id'],
                                  f"Для использования всех функций подпишитесь на группу!\n{group_url}")
            elif event.object.message['text'].lower() == "Выбрать произведение".lower():
                if check_member(event.object.message['from_id']):
                    keyboard = VkKeyboard(inline=True)
                    buttons = [novel for novel in novels[:5]]
                    buttons.append('Страница 2')
                    color = VkKeyboardColor.POSITIVE
                    for i, button in enumerate(buttons):
                        if i == len(buttons) - 1:
                            color = VkKeyboardColor.PRIMARY
                        keyboard.add_callback_button(
                            label=button,
                            color=color,
                            payload={'type': 'my_own_100500_type_edit', f'text': f'{button}'})
                        if i < len(buttons) - 1:
                            keyboard.add_line()
                    write_message(event.object.message['peer_id'], "Какое произведение вас интересует?", keyboard)
                else:
                    write_message(event.object.message['peer_id'],
                                  f"Для использования всех функций подпишитесь на группу!\n{group_url}")
            elif event.object.message['text'].lower() == 'Start'.lower():
                keyboard = get_open_menu_keyboard()
                write_message(event.object.message['peer_id'], "Рад приветствовать!", keyboard)
            elif event.object.message['text'].lower() == 'Назад'.lower():
                keyboard = get_open_menu_keyboard()
                write_message(event.object.message['peer_id'], "До новых встреч!", keyboard)
            elif event.object.message['text'].lower() == 'Контакты'.lower():
                keyboard = get_open_menu_keyboard()
                write_message(event.object.message['peer_id'],
                              'Kristina Taylor\nVK: https://vk.com/kristin37\nTelegram: https://t.me/KristinT37',
                              keyboard)
            else:
                write_message(event.object.message['peer_id'], "Sorry I don't understand. Write start.")

        # Processing clicks on callback buttons
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            if event.object.payload.get('type') == 'my_own_100500_type_edit':
                path = 'novels'
                if event.object.payload.get('text') == 'Меню':
                    keyboard = get_open_menu_keyboard()
                    write_message(event.object.peer_id, 'Меню открыто', keyboard)
                elif event.object.payload.get('text') == 'Страница 2':
                    # If elements count will be > 10 then need do [5:10], next [10:15] and next, next, next
                    buttons = [novel for novel in novels[5:]]
                    buttons.append('Страница 3')
                    buttons.append('На страницу 1')
                    keyboard = VkKeyboard(inline=True)
                    color = VkKeyboardColor.POSITIVE
                    for i, button in enumerate(buttons):
                        if i == len(buttons) - 1:
                            color = VkKeyboardColor.NEGATIVE
                        elif i == len(buttons) - 2:
                            color = VkKeyboardColor.PRIMARY
                        keyboard.add_callback_button(
                            label=button,
                            color=color,
                            payload={'type': 'my_own_100500_type_edit', f'text': f'{button}'})
                        if i < len(buttons) - 1:
                            keyboard.add_line()
                    edit_message(event, 'Секунду, загружаю страницу 2')
                    write_message(event.object.peer_id,"Какое произведение вас интересует?", keyboard)
                elif event.object.payload.get('text') == 'Страница 3':
                    write_message(event.object.peer_id, 'Еще больше романов будет доступно совсем скоро!')
                elif event.object.payload.get('text') == 'На страницу 1':
                    buttons = [novel for novel in novels[:5]]
                    buttons.append('Страница 2')
                    keyboard = VkKeyboard(inline=True)
                    color = VkKeyboardColor.POSITIVE
                    for i, button in enumerate(buttons):
                        if i == len(buttons) - 1:
                            color = VkKeyboardColor.PRIMARY

                        keyboard.add_callback_button(
                            label=button,
                            color=color,
                            payload={'type': 'my_own_100500_type_edit', f'text': f'{button}'})
                        if i < len(buttons) - 1:
                            keyboard.add_line()
                    edit_message(event, 'Секунду, загружаю страницу 1')
                    write_message(event.object.peer_id,"Какое произведение вас интересует?", keyboard)

                # In next block(lines 164 - 193) in future will be used functions get_sending_file and write_message
                # Information about characters of novels and about novels will be collected in docx files
                # When user clicks button - bot must send him file with description or characters from
                # Information about novels will be located in /description
                # Information about characters will be located in /characters
                elif event.object.payload.get('text') == 'Персонажи НСВ':
                    write_message(event.object.peer_id, 'В разработке...', None)
                elif event.object.payload.get('text') == 'О НСВ':
                    write_message(event.object.peer_id, 'В разработке...', None)

                elif event.object.payload.get('text') == 'Персонажи ТГГ':
                    write_message(event.object.peer_id, 'В разработке...', None)
                elif event.object.payload.get('text') == 'О ТГГ':
                    write_message(event.object.peer_id, 'В разработке...', None)

                elif event.object.payload.get('text') == 'Персонажи ЧЧ':
                    write_message(event.object.peer_id, 'В разработке...', None)
                elif event.object.payload.get('text') == 'О ЧЧ':
                    write_message(event.object.peer_id, 'В разработке...', None)

                elif event.object.payload.get('text') == 'Персонажи ИМВЛ':
                    write_message(event.object.peer_id, 'В разработке...', None)
                elif event.object.payload.get('text') == 'О ИМВЛ':
                    write_message(event.object.peer_id, 'В разработке...', None)

                elif event.object.payload.get('text') == 'Персонажи КВС':
                    write_message(event.object.peer_id, 'В разработке...', None)
                elif event.object.payload.get('text') == 'О КВС':
                    write_message(event.object.peer_id, 'В разработке...', None)

                elif event.object.payload.get('text') == 'Персонажи ПОПИВ':
                    write_message(event.object.peer_id, 'В разработке...', None)
                elif event.object.payload.get('text') == 'О ПОПИВ':
                    write_message(event.object.peer_id, 'В разработке...', None)

                else:
                    attachment = get_sending_file(event, f'{event.object.payload.get('text')}.docx', path)
                    text = 'Немного терпения, пожалуйста.\nУже отправляю!&#128522;'
                    match event.object.payload.get('text'):
                        case 'Наше счастливое вчера':
                            edit_message(event, text)
                            keyboard = get_keyboard('Персонажи НСВ', 'О НСВ')
                            write_message(event.object.peer_id, 'Отличный детективный роман!', keyboard,
                                          attachment)
                        case 'Тени грешного города':
                            edit_message(event, text)
                            keyboard = get_keyboard('Персонажи ТГГ', 'О ТГГ')
                            write_message(event.object.peer_id,
                                          'Начало истории необычной компании демонов. Приятного прочтения!',
                                          keyboard,
                                          attachment)
                        case 'Черный человек':
                            edit_message(event, text)
                            keyboard = get_keyboard('Персонажи ЧЧ', 'О ЧЧ')
                            write_message(event.object.peer_id,
                                          'Пора узнать секреты прошлого темного мастера и его свиты.',
                                          keyboard,
                                          attachment)
                        case 'Из мажоров в люди':
                            edit_message(event, text)
                            keyboard = get_keyboard('Персонажи ИМВЛ', 'О ИМВЛ')
                            write_message(event.object.peer_id,
                                          'Первая часть увлекательной истории семьи Алехиных. Классика!',
                                          keyboard,
                                          attachment)
                        case 'Какой же выбор сделать':
                            edit_message(event, text)
                            keyboard = get_keyboard('Персонажи КВС', 'О КВС')
                            write_message(event.object.peer_id,
                                          'А вот и продолжение истории о семье Алехиных!',
                                          keyboard,
                                          attachment)
                        case 'Повести о пространстве и времени':
                            keyboard = get_keyboard('Персонажи ПОПИВ', 'О ПОПИВ')
                            edit_message(event, text)
                            write_message(event.object.peer_id,
                                          'Интересное произведение о путешествиях во времени и не только!',
                                          keyboard,
                                          attachment)
        # Checking following of new user
        elif event.type == VkBotEventType.GROUP_JOIN:
            write_message(event.object.user_id, "Thanks for following!\nEnjoy your use!")
            add_member(event.object.user_id)
        elif event.type == VkBotEventType.GROUP_LEAVE:
            write_message(event.object.user_id, "Было приятно с вами работать! Всего доброго!")
            remove_member(event.object.user_id)
