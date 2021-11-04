import requests
import time
import json
import os
from settings import TOKEN

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

MENU_PRINCIPAL = 1
MENU_2 = 2
SIM = 4
NAO = 5
ALFACE, BETERRABA, CENOURA, TOMATE, BERINJELA, PRINCIPAL = range(6)

MENU_ALFACE = 3
ALFACE_1, ALFACE_2, ALFACE_3, ALFACE_4, ALFACE_5 = range(5)


url_base = f'https://api.telegram.org/bot{TOKEN}/'#getUpdates?timeout=100'

primeira_resposta = 'De acordo com as características das folhas, as cultivares de alface são classificadas em grupos:' \
f'{os.linesep * 2}A) Grupo Americana: formação de cabeça com folhas grossas (Tainá, Lorca, Lucy Brown, Raider Plus e Laurel);'  \
f'{os.linesep * 2}B) Grupo Crespa: não formação de cabeça com folhas crespas (Verônica, Vera e Vanda);' \
f'{os.linesep * 2}C) Grupo Lisa ou Manteiga: formação de cabeça com folhas lisas (Brasil 303, Regina, Babá-de-verão, Elisa, ' \
f'Karla e Lídia);' \
f'{os.linesep * 2}D) Grupo Mimosa: não formação de cabeça com folhas com borda repicada (Salad Bowl);' \
f'{os.linesep * 2}E) Grupo Romana: formação de cabeça alongada com folhas lisas, alongadas, duras e grossas (Romana Balão, Romaine).' 
    
segunda_resposta = 'O cultivo em campo aberto ainda é predominante, apesar das perdas e limitações ainda' \
'existentes no cultivo da alface durante o verão. O cultivo em condições de ambiente protegido, seja no solo' \
'ou em sistema hidropônico, vem crescendo em função da redução dos riscos de perda, previsibilidade e constância' \
'da produção, principalmente durante o período de verão.' 

terceira_resposta = 'O cultivo em campo aberto ainda é predominante, apesar das perdas e limitações ainda existentes'  \
'no cultivo da alface durante o verão. O cultivo em condições de ambiente protegido, seja no solo ou em sistema'  \
'hidropônico, vem crescendo em função da redução dos riscos de perda, previsibilidade e constância da produção, ' \
'principalmente durante o período de verão.' \
f'{os.linesep * 2} Após a correção da fertilidade do solo, os canteiros são preparados respeitando as dimensões ' \
'de 1,1 a 1,2m de largura e 0,4m de espaçamento entre si. A altura variará de acordo com o tipo de solo e drenagem.' \
'Quanto mais úmido o solo, pior será a sua drenagem, sendo este um indicativo de que os canteiros deverão ser ' \
'construídos com altura mais elevada. Em regiões de solo arenoso e boa drenagem pode ser dispensado o preparo dos ' \
'de canteiros, porém, espaços maiores entre plantas devem ser adotados para facilitar o trânsito, realização dos' \
' tratos culturais e colheita.' 

quarta_resposta = 'Em solos propícios ao cultivo da alface é recomendada a utilização de 200 g de composto orgânico' \
'ou esterco de vaca curtido por planta. A aplicação poderá ser feita a lanço antes ou após o preparo dos canteiros' \
'devendo-se, logo em seguida, incorporá-los ao solo. Em solos com baixa fertilidade e/ou baixo teor de matéria orgânica,' \
'a adubação deverá ser localizada em pequenas “covas”, próximo às mudas. Para o plantio convencional, com a utilização' \
'de adubos químicos, seguir as recomendações do Boletim 200 do IAC.' 

quinta_resposta = f'Em solos propícios ao cultivo da alface é recomendada a utilização de 200 g de composto orgânico ' \
'ou esterco de vaca curtido por planta. A aplicação poderá ser feita a lanço antes ou após o preparo dos canteiros ' \
'devendo-se, logo em seguida, incorporá-los ao solo. Em solos com baixa fertilidade e/ou baixo teor de matéria orgânica,' \
' a adubação deverá ser localizada em pequenas “covas”, próximo às mudas. Para o plantio convencional, com a utilização' \
'de adubos químicos, seguir as recomendações do Boletim 200 do IAC.' \
f'{os.linesep * 2} A irrigação é fundamental nesta fase, pois o excesso de água propiciará o ' \
'estabelecimento de doenças causadas por fungos ou bactérias. As mudas estarão aptas para o transplante no campo ' \
'quando desenvolverem seis folhas definitivas, o que ocorre de 20 a 30 dias após a semeadura, conforme a temperatura ' \
'do período e dos tratos culturais empregados.' 

def start(update, context):
    message = 'Olá, Bem vindo ao BotAgroTech, aqui você vai encontar algumas informações sobre cultivo. Digite /menu para mais opções.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    
def menu_principal(update, context):
    question = 'Selecione qual deseja saber: '
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Alface", callback_data=str(ALFACE)),
          InlineKeyboardButton("Beterraba", callback_data=str(BETERRABA)),
          InlineKeyboardButton("Cenora", callback_data=str(CENOURA))], 
         # Segunda linha
         [InlineKeyboardButton("Tomate", callback_data=str(TOMATE)),
          InlineKeyboardButton("Berinjela", callback_data=str(BERINJELA))]])    
    
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
    f'{os.linesep * 2} 5 - Como     devo fazer para obter mudas de alface?' 
    
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
        [[InlineKeyboardButton("Continuar no menu de Alfaces", callback_data=str(ALFACE)),
          InlineKeyboardButton("Voltar ao menu principal", callback_data=str(PRINCIPAL))]])
        
    query.edit_message_text(
        text=question, reply_markup=keyboard
    )
    
    return MENU_PRINCIPAL

def alface_resposta_1(update, context):
    return respostas_alface(update, context, primeira_resposta)

def alface_resposta_2(update, context):
    return respostas_alface(update, context, segunda_resposta)

def alface_resposta_3(update, context):
    return respostas_alface(update, context, terceira_resposta)

def alface_resposta_4(update, context):
    return respostas_alface(update, context, quarta_resposta)

def alface_resposta_5(update, context):
    return respostas_alface(update, context, quinta_resposta)

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