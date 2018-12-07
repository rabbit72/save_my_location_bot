import os
import telebot


BOT_TOKEN = os.getenv("BOT_TOKEN") or open("../BOT_TOKEN.txt").read()

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hi, I can save locations for you")


if __name__ == "__main__":
    bot.polling()
