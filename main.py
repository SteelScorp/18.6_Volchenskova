import telebot
from config import TOKEN, currency
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
   text = 'Чтобы начать работу введите команду боту в следующем формате:' \
          '\n<имя валюты> <в какую валюту перевести> <количество валюты>' \
          '\nУвидеть список всех доступных валют: /values'
   bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for money in currency.keys():
        text = '\n'.join((text, money, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException("Неверное количество параметров.")

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя:\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} = {round(float(total_base) * float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()
