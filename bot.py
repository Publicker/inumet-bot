import telegram
from config import *

# GET AUTH FOR USE TELEGRAM API
bot = telegram.Bot(token=TELEGRAM_KEY)

chat_id = "@inumet_alertas"

# SEND PHOTO
# status = bot.sendPhoto(chat_id="@inumet_alertas", photo="https://images.unsplash.com/photo-1568216874968-b74b3b69872b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=683&q=80", parse_mode=telegram.ParseMode.HTML, caption = "Alerta naranja")

def sendMessage(message):
  # Send message to channel
  status = bot.send_message(chat_id=chat_id, text=message, parse_mode=telegram.ParseMode.HTML)
  return status

def sendPhoto(url_photo, caption):
  # Send photo to channel
  status = bot.sendPhoto(chat_id=chat_id, photo=url_photo, caption = caption, parse_mode=telegram.ParseMode.HTML)

  return status

def sendMediaGroup(media, caption):
  media_to_send = []

  # Append the first element with captions
  media_to_send.append(telegram.InputMediaPhoto(media[0], caption=caption, parse_mode=None))
  
  # And remove from media
  media.pop(0)

  # For the other -> Append to array
  for element in media:
    media_to_send.append(telegram.InputMediaPhoto(element))

  status = bot.sendMediaGroup(chat_id=chat_id, media=media_to_send)

  return status


# status_multiple = sendMediaGroup()
# print(status_multiple)