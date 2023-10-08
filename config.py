# Importing libraries
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

# Api data
api_token = 'your api token'
group_id = 'your group id'
group_url = 'your group url'

novels = ["Наше счастливое вчера", "Тени грешного города", "Черный человек",
                          "Из мажоров в люди", "Какой же выбор сделать",
                          "Повести о пространстве и времени"]


# Api and long poll
api = vk_api.VkApi(token=api_token)
vk = api.get_api()
long_poll = VkBotLongPoll(api, group_id)
