from io import BytesIO
from telegram import Update, ChatAction, ParseMode
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters

import logging

from ai.azure_caption import AzureCaption
from ai.azure_translator import AzureTranslator
from ai.custom_sentiment import CustomSentiment

from bot.config import Config

azureCaption = AzureCaption()
azureTranlator = AzureTranslator()
customSentiment = CustomSentiment()

c = Config()

updater = Updater(token=c.get_value("TELEGRAMBOT","TOKEN"), use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):

    user = update.message.from_user
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    msg = "Hi, <strong>%s</strong>. I am a bot that can do some artificial intelligence activities. Typing /help to see what I can do." % user.first_name

    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=msg, parse_mode=ParseMode.HTML)

def help_(update: Update, context: CallbackContext):

    msg = "Just send an image and I will describe it." \
                    "\nUse /translate <strong>[text]</strong> and I will translate the text for you. For a while, I just know translate from english to portuguese." \
                    "\nUse /sentiment <strong>[text]</strong> and I will analyse sentiment of the text." 

    context.bot.send_message(chat_id=update.effective_chat.id,
                            text=msg, parse_mode=ParseMode.HTML)

def image(update: Update, context: CallbackContext):
    photo = update.message.photo[-1].get_file()
    try:
        context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
        f =  BytesIO(photo.download_as_bytearray())
        description = azureCaption.caption_image(f)
        context.bot.send_message(chat_id=update.effective_chat.id,
                        text=description)
    except Exception as e:
        logger.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id,
                        text="Unfortunately, the image could not be recognized.")

def translate(update: Update, context: CallbackContext):
    message = ' '.join(context.args)
    
    try: 
        context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
        translation = azureTranlator.translate(message)
        update.message.reply_text(translation)
    except Exception as e:
        logger.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id,
                        text="Unfortunately, it was not possible to translate.")

def sentiment(update: Update, context: CallbackContext):

    message = ' '.join(context.args)

    try: 
        context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        sentiment = customSentiment.sentiment(message)
        response_ = "Humm, I think this text has a <strong>%s</strong> sentiment." % sentiment
        update.message.reply_text(response_, reply_to_message_id=update.message.message_id,parse_mode=ParseMode.HTML)

    except Exception as e:
        logger.error(e)
        context.bot.send_message(chat_id=update.effective_chat.id,
                        text="Unfortunately, it was not possible to get the sentiment.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help_)
dispatcher.add_handler(help_handler)

image_handler = MessageHandler(Filters.photo, image)
dispatcher.add_handler(image_handler)

translate_handler = CommandHandler('translate', translate, pass_args=True)
dispatcher.add_handler(translate_handler)

sentiment_handler = CommandHandler('sentiment', sentiment, pass_args=True)
dispatcher.add_handler(sentiment_handler)


updater.start_polling()
updater.idle()