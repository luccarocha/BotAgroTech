import requests
import time
import json
import os
from settings import TOKEN

from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          RegexHandler, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

STATE1 = 1
STATE2 = 2

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

# iniciar o bot
def iniciar():
    print("press CTRL + C to cancel.")
    update_id = None
    while True:
      atualizacao = obter_novas_mensagens(update_id)
      mensagens = atualizacao["result"]      
      if mensagens:
        for mensagem in mensagens:
          update_id = mensagem['update_id']          
          #mensagem = str(mensagem["message"]["text"])
          if 'message' in mensagem:
            chat_id = mensagem['message']['from']['id']
            primeira_mensagem = int (mensagem["message"]["message_id"]) == 1
            resposta = criar_resposta(mensagem, primeira_mensagem)
            responder(resposta,chat_id)
            
# obter as mensagens
def obter_novas_mensagens(update_id):
    link_requisicao = f'{url_base}getUpdates?timeout=100'
    if update_id:
      # recebe sempre a ultima mensagem
      link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
    resultado = requests.get(link_requisicao)
    return json.loads(resultado.content)

# criar respostas
def criar_resposta(mensagem, primeira_mensagem):      
    mensagem = mensagem['message']['text']
    qt_respostas = ('1', '2', '3', '4', '5')
    
    msg_menu = 'Digite o número da opção que deseja saber!'  \
    f'{os.linesep * 2} 1 -  Quais são as cultivares de alface posso escolher?' \
    f'{os.linesep * 2} 2 - Quais são os tipos de sistemas de cultivo para alface? ' \
    f'{os.linesep * 2} 3 - Como devo fazer o preparo do solo para cultivar alface? ' \
    f'{os.linesep * 2} 4 - Como devo fazer a adubação para a alface?'  \
    f'{os.linesep * 2} 5 - Como devo fazer para obter mudas de alface?' \
        
    msg_boas_vindas = 'Olá, Bem vindo ao BotAgroTech, aqui você vai encontar algumas informações sobre o cultivo de alface.' \
    'Gostaria de ir para o menu? Digite "Menu"!'
    
    if primeira_mensagem or mensagem == '/start':
        return msg_boas_vindas
    elif mensagem.lower() =='menu':
        return 'Olá, Bem vindo ao BotAgroTech, aqui você vai encontar algumas informações sobre o culttivo de alface. \n' + msg_menu
    else:
        if mensagem in qt_respostas:
          if mensagem == '1':
            return primeira_resposta     
          if mensagem == '2':
            return segunda_resposta
          if mensagem == '3':
            return terceira_resposta
          if mensagem == '4':
            return quarta_resposta
          if mensagem == '5':
            return quinta_resposta
        else:
          if mensagem.lower() in ('s','sim'):
            return 'Agradecemos seu contato, precisando é só chamar!'
          elif mensagem.lower() in ('n','nao'):
            return 'Ótimo! \n' + msg_menu
          else:
            return 'Não entemos sua solicitação. \nGostaria de voltar ao menu? Digite "menu"!'
# responder
def responder(resposta, chat_id):
    # enviar
    link_de_envio = f'{url_base}sendMessage?chat_id={chat_id}&text={resposta}'
    requests.get(link_de_envio)

def welcome(update, context):
    message = 'Olá, Bem vindo ao BotAgroTech, aqui você vai encontar algumas informações sobre o cultivo de alface.' \
    'Gostaria de ir para o menu? Digite "/menu"!'
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def feedback(update, context):
    try:
        message = 'Por favor, digite um feedback para o nosso tutorial:'
        update.message.reply_text(message, reply_markup=ReplyKeyboardMarkup([], one_time_keyboard=True)) 
        return STATE1
    except Exception as e:
        print(str(e))

def inputFeedback(update, context):
    feedback = update.message.text
    print(feedback)
    if len(feedback) < 10:
        message = """Seu feedback foi muito curtinho... 
                        \nInforma mais pra gente, por favor?"""
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        return STATE1
    else:
        message = "Muito obrigada pelo seu feedback!"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        
def inputFeedback2(update, context):
    feedback = update.message.text
    message = "Muito obrigada pelo seu feedback!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def cancel(update, context):
    return ConversationHandler.END

def menu_options(update, context):
    question = 'Insira qual opção deseja saber!'  \
    f'{os.linesep * 2} 1 -  Quais são as cultivares de alface posso escolher?' \
    f'{os.linesep * 2} 2 - Quais são os tipos de sistemas de cultivo para alface? ' \
    f'{os.linesep * 2} 3 - Como devo fazer o preparo do solo para cultivar alface? ' \
    f'{os.linesep * 2} 4 - Como devo fazer a adubação para a alface?'  \
    f'{os.linesep * 2} 5 - Como devo fazer para obter mudas de alface?' 
    
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("1", callback_data='1'),
          InlineKeyboardButton("2", callback_data='2'),
          InlineKeyboardButton("3", callback_data='3'),
          InlineKeyboardButton("4", callback_data='4'),
          InlineKeyboardButton("5", callback_data='5')]])
    update.message.reply_text(question, reply_markup=keyboard)


def get_option(update, context):
    query = update.callback_query
    print(query.data)
    
    if query.data == '1':        
        context.bot.send_message(chat_id=update.effective_chat.id, text=primeira_resposta)        
    elif query.data == '2':
        context.bot.send_message(chat_id=update.effective_chat.id, text=segunda_resposta)
    elif query.data == '3':
        context.bot.send_message(chat_id=update.effective_chat.id, text=terceira_resposta)
    elif query.data == '4':
        context.bot.send_message(chat_id=update.effective_chat.id, text=quarta_resposta)
    elif query.data == '5':
        context.bot.send_message(chat_id=update.effective_chat.id, text=quinta_resposta)           
    
def main():
    try:
        updater = Updater(token=TOKEN, use_context=True)    
        updater.dispatcher.add_handler(CommandHandler('start', welcome))

        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('feedback', feedback)],
            states={
                STATE1: [MessageHandler(Filters.text, inputFeedback)],
                STATE2: [MessageHandler(Filters.text, inputFeedback2)]
            },
            fallbacks=[CommandHandler('cancel', cancel)])
        
        updater.dispatcher.add_handler(conversation_handler)
        updater.dispatcher.add_handler(CommandHandler('menu', menu_options))
        updater.dispatcher.add_handler(CallbackQueryHandler(get_option))

        print("Updater no ar1: " + str(updater))
        updater.start_polling()
        updater.idle()
    except Exception as e:
        print(str(e))



if __name__ == '__main__':     
    main()