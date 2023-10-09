# Importing libraries
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll

# Api data
api_token = 'vk1.a.vync5o0T6s1Xawobx8YQ-tQETHbzG6dEm7eax4Km913WHZBVOENBsjuYMsMV5mS51oiHI32Ivjsu4zD3DGkQQAkHVq5YBkZnka6M1hqP9AsUfaEct6Rsm3qqU_5zabUFAFZIVW3YSKaCDExRupKTWuFXbdvA6IW_w5r-iOwONtH9l8aZcOhtuUQJX_aOTc0sgX_Qwu8uBPnBXy9lGGxkUQ'
group_id = '222896495'
group_url = 'https://vk.com/club222896495'

novels = ["Наше счастливое вчера", "Тени грешного города", "Черный человек",
                          "Из мажоров в люди", "Какой же выбор сделать",
                          "Повести о пространстве и времени"]


# Api and long poll
api = vk_api.VkApi(token=api_token)
vk = api.get_api()
long_poll = VkBotLongPoll(api, group_id)
