from settings import TOKEN
from respostas.alface import PRIMEIRA_RESPOSTA, SEGUNDA_RESPOSTA, TERCEIRA_RESPOSTA, QUARTA_RESPOSTA, QUINTA_RESPOSTA
import os

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

MENU_PRINCIPAL = 1
MENU_ALFACE = 2
ALFACE_1, ALFACE_2, ALFACE_3, ALFACE_4, ALFACE_5 = range(5)
ALFACE, PRINCIPAL = range(2)

def start(update, context):
    message = 'Olá, Bem vindo ao BotAgroTech, aqui você vai encontar algumas informações sobre cultivo. Digite /menu para mais opções.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
def menu_principal(update, context):
    question = 'Selecione qual deseja saber: '
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Alface", callback_data=str(ALFACE))]])
    
    if update.callback_query:
        query = update.callback_query
        query.answer()
        
        query.edit_message_text(
            text=question, reply_markup=keyboard
        )        
    else:
        update.message.reply_text(question, reply_markup=keyboard)
    
    return MENU_PRINCIPAL    

def menu_alface(update, context):
    query = update.callback_query
    query.answer()
    
    question = 'Insira qual opção deseja saber!'  \
    f'{os.linesep * 2} 1 -  Quais são as cultivares de alface posso escolher?' \
    f'{os.linesep * 2} 2 - Quais são os tipos de sistemas de cultivo para alface? ' \
    f'{os.linesep * 2} 3 - Como devo fazer o preparo do solo para cultivar alface? ' \
    f'{os.linesep * 2} 4 - Como devo fazer a adubação para a alface?'  \
    f'{os.linesep * 2} 5 - Como devo fazer para obter mudas de alface?' 
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("1", callback_data=str(ALFACE_1)),
          InlineKeyboardButton("2", callback_data=str(ALFACE_2)),
          InlineKeyboardButton("3", callback_data=str(ALFACE_3)),
          InlineKeyboardButton("4", callback_data=str(ALFACE_4)),
          InlineKeyboardButton("5", callback_data=str(ALFACE_5))]])
        
    query.edit_message_text(
        text=question, reply_markup=keyboard
    )
    
    return MENU_ALFACE

def respostas_alface(update, context, resposta):
    query = update.callback_query
    query.answer()
        
    question = resposta
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Continuar no menu de Alfaces", callback_data=str(ALFACE))], 
         [InlineKeyboardButton("Voltar ao menu principal", callback_data=str(PRINCIPAL))]])
        
    query.edit_message_text(
        text=question, reply_markup=keyboard
    )
    
    return MENU_PRINCIPAL

def alface_resposta_1(update, context):
    return respostas_alface(update, context, PRIMEIRA_RESPOSTA)

def alface_resposta_2(update, context):
    return respostas_alface(update, context, SEGUNDA_RESPOSTA)

def alface_resposta_3(update, context):
    return respostas_alface(update, context, TERCEIRA_RESPOSTA)

def alface_resposta_4(update, context):
    return respostas_alface(update, context, QUARTA_RESPOSTA)

def alface_resposta_5(update, context):
    return respostas_alface(update, context, QUINTA_RESPOSTA)

def cancel(update, context):
    return ConversationHandler.END

def main():
    try:
        updater = Updater(token=TOKEN, use_context=True)       
        
        updater.dispatcher.add_handler(CommandHandler('start', start))
        
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('menu', menu_principal)],
            states={
                MENU_PRINCIPAL: [
                    CallbackQueryHandler(menu_alface, pattern='^' + str(ALFACE) + '$'),
                    CallbackQueryHandler(menu_principal, pattern='^' + str(PRINCIPAL) + '$'),
                ],                
                MENU_ALFACE: [
                    CallbackQueryHandler(alface_resposta_1, pattern='^' + str(ALFACE_1) + '$'),
                    CallbackQueryHandler(alface_resposta_2, pattern='^' + str(ALFACE_2) + '$'),
                    CallbackQueryHandler(alface_resposta_3, pattern='^' + str(ALFACE_3) + '$'),
                    CallbackQueryHandler(alface_resposta_4, pattern='^' + str(ALFACE_4) + '$'),
                    CallbackQueryHandler(alface_resposta_5, pattern='^' + str(ALFACE_5) + '$')
                ]   
                                            
            },
            fallbacks=[CommandHandler('cancel', cancel)])
        
        updater.dispatcher.add_handler(conversation_handler)        

        print("Updater no ar1: " + str(updater))
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(str(e))



if __name__ == '__main__':     
    main()
