import os
import telebot


BOT_TOKEN = os.getenv("BOT_TOKEN") or open("../BOT_TOKEN.txt").read()

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.chat.id, "Hi, I can save locations for you")


@bot.message_handler()
def handle_not_realized_message(message):
    bot.send_message(
        message.chat.id,
        "I don't understand you, choose one of the my commands"
    )


if __name__ == "__main__":
    bot.polling()
