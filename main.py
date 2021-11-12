from settings import TOKEN
from respostas.alface import PRIMEIRA_RESPOSTA, SEGUNDA_RESPOSTA, TERCEIRA_RESPOSTA, QUARTA_RESPOSTA, QUINTA_RESPOSTA
import os
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


ALFACE_1, ALFACE_2, ALFACE_3, ALFACE_4, ALFACE_5, FOTOS, FIM_FOTOS = range(7)
MENU_PRINCIPAL, MENU_ALFACE, IMAGENS = range(3)
ALFACE, PRINCIPAL = range(2)

class TelegramBot():
    def __init__(self):
        self.img_atual = None
        self.image = None

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
        if self.image:
            self.image.delete()
            self.image = None
            
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
        return self.respostas_alface(update, context, PRIMEIRA_RESPOSTA)

    def alface_resposta_2(self, update, context):
        return self.respostas_alface(update, context, SEGUNDA_RESPOSTA)

    def alface_resposta_3(self, update, context):
        return self.respostas_alface(update, context, TERCEIRA_RESPOSTA)

    def alface_resposta_4(self, update, context):
        return self.respostas_alface(update, context, QUARTA_RESPOSTA)

    def alface_resposta_5(self, update, context):
        return self.respostas_alface(update, context, QUINTA_RESPOSTA)

    def manda_fotos(self, update, context):
        if not self.image:
            self.image = context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('imgs/1_imagem.png', 'rb'))
            self.img_atual = 0
            doença = 'Míldio em Mudas de Alface'            
        elif self.img_atual == 0:
            self.image.delete()
            self.image = context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('imgs/2_imagem.png', 'rb'))
            self.img_atual = 1
            doença = 'Míldio em alface adulta'            
        elif self.img_atual == 1:
            self.image.delete()
            self.image = context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('imgs/3_imagem.png', 'rb'))    
            self.img_atual = 2
            doença = 'Septoriose'            
        elif self.img_atual == 2:
            self.image.delete()
            return IMAGENS
        else:    
            if self.image:
                self.image.delete()           
            
        query = update.callback_query
        query.answer()
        
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Sim", callback_data=str(FOTOS) if self.img_atual != 2 else str(FIM_FOTOS)), 
            InlineKeyboardButton("Não", callback_data=str(FOTOS) if self.img_atual != 2 else str(FIM_FOTOS))], 
            [InlineKeyboardButton("Voltar ao Menu", callback_data=str(ALFACE))]])
        
        query.edit_message_text(
            text=f"Seu alface se parece com isso? Pode ser {doença}", reply_markup=keyboard
        )
        
        return IMAGENS

    def fim_fotos(self, update, context):
        self.image.delete()
        self.image = None
        
        query = update.callback_query
        query.answer()
        
        keyboard = InlineKeyboardMarkup(
            [[InlineKeyboardButton("Voltar ao Menu", callback_data=str(ALFACE))]])
        
        query.edit_message_text(
            text=f"Desculpe, não possuimos mais imagens de possíveis doenças no nosso banco de dados.", reply_markup=keyboard
        )
        
        return IMAGENS
        
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
                        CallbackQueryHandler(self.manda_fotos, pattern='^' + str(FOTOS) + '$'),
                    ],
                    IMAGENS: [
                        CallbackQueryHandler(self.manda_fotos, pattern='^' + str(FOTOS) + '$'),
                        CallbackQueryHandler(self.menu_alface, pattern='^' + str(ALFACE) + '$'),
                        CallbackQueryHandler(self.fim_fotos, pattern='^' + str(FIM_FOTOS) + '$'),
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
