from settings import TOKEN
from respostas.alface import PRIMEIRA_RESPOSTA, SEGUNDA_RESPOSTA, TERCEIRA_RESPOSTA, QUARTA_RESPOSTA, QUINTA_RESPOSTA
import os
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

MENU_PRINCIPAL = 1
MENU_ALFACE = 2
ALFACE_1, ALFACE_2, ALFACE_3, ALFACE_4, ALFACE_5 = range(5)
FOTOS = 5
FOTO_1 = 6
FOTO_2 = 7
FOTO_3 = 8
IMAGENS = 9
ALFACE, PRINCIPAL = range(2)

class TelegramBot():
    def __init__(self):
        self.img_atual = 0

    def start(self, update, context):
        message = 'Olá, Bem vindo ao BotAgroTech, aqui você vai encontar algumas informações sobre cultivo.'
        message += f'{os.linesep}Digite /menu para mais informações.'
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        
    def menu_principal(self, update, context):    
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

    def menu_alface(self, update, context):
        query = update.callback_query
        query.answer()
        
        question = 'Insira qual opção deseja saber!'  \
        f'{os.linesep * 2} 1 -  Quais são as cultivares de alface posso escolher?' \
        f'{os.linesep * 2} 2 - Quais são os tipos de sistemas de cultivo para alface? ' \
        f'{os.linesep * 2} 3 - Como devo fazer o preparo do solo para cultivar alface? ' \
        f'{os.linesep * 2} 4 - Como devo fazer a adubação para a alface?'  \
        f'{os.linesep * 2} 5 - Como devo fazer para obter mudas de alface?' \
        f'{os.linesep * 2} 6 - Verificar doenças no Alface' 
        
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("1", callback_data=str(ALFACE_1)),
            InlineKeyboardButton("2", callback_data=str(ALFACE_2)),
            InlineKeyboardButton("3", callback_data=str(ALFACE_3)),
            InlineKeyboardButton("4", callback_data=str(ALFACE_4)),
            InlineKeyboardButton("5", callback_data=str(ALFACE_5)),
            InlineKeyboardButton("6", callback_data=str(FOTOS))]])
            
        query.edit_message_text(
            text=question, reply_markup=keyboard
        )
        
        return MENU_ALFACE

    def respostas_alface(self, update, context, resposta):
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

    def alface_resposta_1(self, update, context):
        return respostas_alface(update, context, PRIMEIRA_RESPOSTA)

    def alface_resposta_2(self, update, context):
        return respostas_alface(update, context, SEGUNDA_RESPOSTA)

    def alface_resposta_3(self, update, context):
        return respostas_alface(update, context, TERCEIRA_RESPOSTA)

    def alface_resposta_4(self, update, context):
        return respostas_alface(update, context, QUARTA_RESPOSTA)

    def alface_resposta_5(self, update, context):
        return respostas_alface(update, context, QUINTA_RESPOSTA)

    def manda_foto_1(self, update, context):
        query = update.callback_query
        query.answer()
        
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Sim", callback_data=str(FOTO_2)), 
            InlineKeyboardButton("Não", callback_data=str(FOTO_2))], 
            [InlineKeyboardButton("Voltar ao Menu", callback_data=str(PRINCIPAL))]])

        self.img_atual = context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('imgs/w.png', 'rb'))
        query.edit_message_text(
            text="Seu alface se parece com isso?", reply_markup=keyboard
        )
        return IMAGENS

    def manda_foto_2(self, update, context):
        query = update.callback_query
        query.answer()
        print(self.img_atual)
        self.img_atual.delete()
    def cancel(self, update, context):
        return ConversationHandler.END

    def main(self):
        try:
            updater = Updater(token=TOKEN, use_context=True)       
            
            updater.dispatcher.add_handler(CommandHandler('start', self.start))
            
            conversation_handler = ConversationHandler(
                entry_points=[CommandHandler('menu', self.menu_principal)],
                states={
                    MENU_PRINCIPAL: [
                        CallbackQueryHandler(self.menu_alface, pattern='^' + str(ALFACE) + '$'),
                        CallbackQueryHandler(self.menu_principal, pattern='^' + str(PRINCIPAL) + '$'),
                    ],                
                    MENU_ALFACE: [
                        CallbackQueryHandler(self.alface_resposta_1, pattern='^' + str(ALFACE_1) + '$'),
                        CallbackQueryHandler(self.alface_resposta_2, pattern='^' + str(ALFACE_2) + '$'),
                        CallbackQueryHandler(self.alface_resposta_3, pattern='^' + str(ALFACE_3) + '$'),
                        CallbackQueryHandler(self.alface_resposta_4, pattern='^' + str(ALFACE_4) + '$'),
                        CallbackQueryHandler(self.alface_resposta_5, pattern='^' + str(ALFACE_5) + '$'),
                        CallbackQueryHandler(self.manda_foto_1, pattern='^' + str(FOTOS) + '$'),
                    ],
                    IMAGENS: [
                        CallbackQueryHandler(self.manda_foto_2, pattern='^' + str(FOTO_2) + '$'),
                    ],    
                                                
                },
                fallbacks=[CommandHandler('cancel', self.cancel)])
            
            updater.dispatcher.add_handler(conversation_handler)        

            print("Updater no ar1: " + str(updater))
            updater.start_polling()
            updater.idle()
        except Exception as e:
            print(str(e))


if __name__ == '__main__':     
    bot = TelegramBot()
    bot.main()
