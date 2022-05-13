from io import BytesIO
from telegram import Update, ChatAction, ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters, ConversationHandler

import logging

from bot.ai.azure_caption import AzureCaption
from bot.ai.custom_sentiment import CustomSentiment
from bot.ai.openai_conversation import OpenAiConversation

from bot.config import Config

#CONVERSATION STATES
CHOOSE_TOPIC, MAKE_QUESTION = range(2)

azureCaption = AzureCaption()
customSentiment = CustomSentiment()
openaiCoversation = OpenAiConversation()

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
                    "\nUse /sentiment <strong>[text]</strong> and I will analyse sentiment of the text." \
                    "\nUse /conversation to start talking about a topic that I studied."

    context.bot.send_message(chat_id=update.effective_chat.id,
                            text=msg, parse_mode=ParseMode.HTML)

def coversation(update: Update, context: CallbackContext):

    user = update.message.from_user
    context.bot.send_chat_action(chat_id=update.message.chat_id, action=ChatAction.TYPING)

    if(openaiCoversation.getStatus()):

        msg = "Hi, %s. What topic do you want to talk about?" % user.first_name

        reply_keyboard = [openaiCoversation.getTopics()]

        update.message.reply_text(msg, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return CHOOSE_TOPIC
    else:

        msg = "Sorry <strong>%s</strong>, but this service is inactive at this moment :(" % user.first_name

        context.bot.send_message(chat_id=update.effective_chat.id,
                            text=msg, parse_mode=ParseMode.HTML)

        return ConversationHandler.END






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

def conversation_finish(update: Update, context: CallbackContext):

    context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text="Tanks for this conversation. If you want to talk again with me, just use the comand /conversation.")

    if "topic" in context.chat_data:
        del context.chat_data["topic"]


    return ConversationHandler.END

def conversation_topic(update: Update, context: CallbackContext):


    topic = update.message.text
    msg1 = "Let's talk about %s. What do you want know? To finish our conversation, just type /finish." % topic
 
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=msg1)

    context.chat_data['topic'] = topic


    return MAKE_QUESTION


def conversation_question(update: Update, context: CallbackContext):

    question = update.message.text
    topic = context.chat_data['topic']
    context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
    
    msg1 = "Humm, interesting question. Take a minute please."
 
    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=msg1)

    context.bot.send_chat_action(chat_id=update.effective_chat.id,action=ChatAction.TYPING)
    '''
    Ucomment this part to use OpenAI API.
    answer = openaiCoversation.sendQuestion(topic, question)

    context.bot.send_message(
        chat_id=update.message.chat_id, 
        text=answer)
    '''
    return MAKE_QUESTION



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help_)
dispatcher.add_handler(help_handler)

image_handler = MessageHandler(Filters.photo, image)
dispatcher.add_handler(image_handler)

sentiment_handler = CommandHandler('sentiment', sentiment, pass_args=True)
dispatcher.add_handler(sentiment_handler)

# Coversation Handler 

conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('conversation', coversation)],
    states = {
        CHOOSE_TOPIC: [MessageHandler(Filters.text, conversation_topic, pass_chat_data=True)],
        MAKE_QUESTION: [MessageHandler(Filters.text & ~(Filters.command), conversation_question,  pass_chat_data=True)],
    },
    fallbacks=[CommandHandler('finish', conversation_finish)]
)
dispatcher.add_handler(conversation_handler)



updater.start_polling()
updater.idle()