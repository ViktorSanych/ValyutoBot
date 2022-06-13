import telebot
from extensions import CriptoConverter, ConvertExeption
from config import keys, TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Что бы начать работу введите команду боту в следующем формате:\n <имя валюты>  \
<в какую валюту перевести>  \
<количество переводимой валюты> \n Увидеть все доступные валюты /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertExeption(f'Слишком много/мало параметров.')

        quote, base, amount = values
        total_base = CriptoConverter.get_price(quote, base, amount)

    except ConvertExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n {e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
