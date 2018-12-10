import os
import telebot
from db import get_user, Location


BOT_TOKEN = os.getenv("BOT_TOKEN") or open("../BOT_TOKEN.txt").read()
START, TITLE, LOCATION, ADDITIONAL, IMAGE, DESCRIPTION, SAVE = range(7)
TEMP = dict()
CONFIRMATION = "y", "yes", "yea", "ok", "д", "да", "ок"
CANCELLATION = "n", "no", "not", "н", "не", "нет"
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    get_user(message)
    bot.send_message(message.chat.id, "Welcome, I can save locations for you")


@bot.message_handler(
    commands=["add"],
    func=lambda message: get_user(message).stage == START
)
def handle_add(message):
    TEMP[message.chat.id] = Location()
    bot.send_message(message.chat.id, "Let's save your location\nSend me title")
    user = get_user(message)
    user.change_stage(TITLE)


@bot.message_handler(func=lambda message: get_user(message).stage == TITLE)
def handle_title(message):
    TEMP[message.chat.id].title = message.text.title()
    bot.send_message(message.chat.id, "Send location")
    user = get_user(message)
    user.change_stage(LOCATION)


@bot.message_handler(
    func=lambda message: get_user(message).stage == LOCATION,
    content_types=["location"]
)
def handle_location(message):
    TEMP[message.chat.id].latitude = message.location.latitude
    TEMP[message.chat.id].longitude = message.location.longitude
    bot.send_message(message.chat.id, "Do you want to add additional information?")
    user = get_user(message)
    user.change_stage(ADDITIONAL)


@bot.message_handler(func=lambda message: get_user(message).stage == ADDITIONAL)
def handle_additional(message):
    user = get_user(message)
    lower_message = message.text.lower()
    if any(word in lower_message for word in CONFIRMATION):
        user.change_stage(IMAGE)
        bot.send_message(message.chat.id, "Send an image of location")
    elif any(word in lower_message for word in CANCELLATION):
        user.change_stage(SAVE)
        send_temp_location(message)
        bot.send_message(message.chat.id, "Do you want to save the location?")


@bot.message_handler(
    func=lambda message: get_user(message).stage == IMAGE,
    content_types=["photo"]
)
def handle_image(message):
    user = get_user(message)
    TEMP[message.chat.id].image = message.photo[2].file_id
    bot.send_message(message.chat.id, "Send location description")
    user.change_stage(DESCRIPTION)


@bot.message_handler(func=lambda message: get_user(message).stage == DESCRIPTION)
def handle_description(message):
    user = get_user(message)
    TEMP[message.chat.id].description = message.text
    user.change_stage(SAVE)

    send_temp_location(message)
    bot.send_message(message.chat.id, "Do you want to save the location?")


@bot.message_handler(func=lambda message: get_user(message).stage == SAVE)
def handle_save(message):
    chat_id = message.chat.id
    user = get_user(message)
    lower_message = message.text.lower()
    if any(word in lower_message for word in CONFIRMATION):
        bot.send_message(chat_id, "The location was saved")
        user.add_location(TEMP[chat_id])
    elif any(word in lower_message for word in CANCELLATION):
        bot.send_message(chat_id, "The location wasn't saved")
    TEMP[chat_id] = None
    user.change_stage(START)


@bot.message_handler(commands=["list"])
def handle_list(message):
    user = get_user(message)
    if user.locations:
        for location in user.locations:
            send_location(message.chat.id, location)
    else:
        bot.send_message(message.chat.id, "You don't have locations")


@bot.message_handler(commands=["reset"])
def handle_reset(message):
    user = get_user(message)
    user.delete_all_locations()
    bot.send_message(message.chat.id, "Your locations were deleted")


@bot.message_handler(content_types=["text"])
def handle_not_realized_message(message):
    bot.send_message(
        message.chat.id,
        "I don't understand you, choose one of the my commands"
    )


def send_location(chat_id, location: Location):
    bot.send_message(chat_id, f"Title: {location.title}")
    bot.send_location(chat_id, location.latitude, location.longitude)
    bot.send_photo(chat_id, location.image, caption=location.description)


def send_temp_location(message):
    chat_id = message.chat.id
    title = TEMP[message.chat.id].title
    latitude = TEMP[chat_id].latitude
    longitude = TEMP[chat_id].longitude
    image = TEMP[chat_id].image
    description = TEMP[chat_id].description

    bot.send_message(chat_id, f"Title: {title}")
    bot.send_location(chat_id, latitude, longitude)
    if image and description:
        bot.send_photo(chat_id, image, caption=description)


if __name__ == "__main__":
    bot.polling()
