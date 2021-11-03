import requests
import time
import json
import os


class TelegramBot:
  def __init__(self):
        token = '2055112037:AAGO3zJywyDtHtCM9yHCRBfsGyhX7b3kAcg'
        self.url_base = f'https://api.telegram.org/bot{token}/'#getUpdates?timeout=100'
  
  #Iniciar o bot
  def Iniciar(self):
    update_id = None
    while True:
      atualizacao = self.obter_novas_mensagens(update_id)
      mensagens = atualizacao["result"]      
      if 'message' in mensagens:
        for mensagem in mensagens:
          update_id = mensagem['update_id']          
          #mensagem = str(mensagem["message"]["text"])
          chat_id = mensagem['message']['from']['id']
          primeira_mensagem = int (mensagem["message"]["message_id"]) == 1
          resposta = self.criar_resposta(mensagem,primeira_mensagem)
          self.responder(resposta,chat_id)

  #Obter as mensagens
  def obter_novas_mensagens(self,update_id):
    link_requisicao = f'{self.url_base}getUpdates?timeout=100'
    if update_id:
      #recebe sempre a ultima mensagem
      link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
    resultado = requests.get(link_requisicao)
    return json.loads(resultado.content)

  #Criar respostas
  def criar_resposta(self,mensagem,primeira_mensagem):
    
    mensagem = mensagem['message']['text']

    if primeira_mensagem == True or mensagem.lower() == 'menu':
          return f'''Olá, Bem vindo ao BotAgroTech, aqui você vai encontar algumas informações sobre o culttivo de alface. Digite o número da opção que deseja saber! {os.linesep} 1 -  Quais são as cultivares de alface posso escolher?{os.linesep}{os.linesep} 2 - Quais são os tipos de sistemas de cultivo para alface? {os.linesep}{os.linesep} 3 - Como devo fazer o preparo do solo para cultivar alface? 
          {os.linesep}{os.linesep} 4 - Como devo fazer a adubação para a alface? {os.linesep}{os.linesep} 5 - Como devo fazer para obter mudas de alface?'''
    
    if mensagem == '1':
      return f'''De acordo com as características das folhas, as cultivares de alface são classificadas em grupos:
      {os.linesep}A) Grupo Americana: formação de cabeça com folhas grossas (Tainá, Lorca, Lucy Brown, Raider Plus e Laurel);
      {os.linesep}B) Grupo Crespa: não formação de cabeça com folhas crespas (Verônica,
      Vera e Vanda);
      {os.linesep}C) Grupo Lisa ou Manteiga: formação de cabeça com folhas lisas (Brasil
      303, Regina, Babá-de-verão, Elisa, Karla e Lídia);
      {os.linesep}D) Grupo Mimosa: não formação de cabeça com folhas com borda repicada
      (Salad Bowl);
      {os.linesep}E) Grupo Romana: formação de cabeça alongada com folhas lisas, alongadas, duras e grossas (Romana Balão, Romaine). 
      {os.linesep}Finalizar consulta (S/N)?'''
    
    if mensagem == '2':
      return f'''O cultivo em campo aberto ainda é predominante, apesar das perdas e limitações ainda existentes no cultivo da alface durante o verão. O cultivo em condições de ambiente protegido, seja no solo ou em sistema hidropônico, vem crescendo em função da redução dos riscos de perda, previsibilidade e constância da produção, principalmente durante o período de verão.
      {os.linesep}Finalizar consulta (S/N)?''' 
    
    if mensagem == '3':
      return f'''O cultivo em campo aberto ainda é predominante, apesar das perdas e limitações ainda existentes no cultivo da alface durante o verão. O cultivo em condições de ambiente protegido, seja no solo ou em sistema hidropônico, vem crescendo em função da redução dos riscos de perda, previsibilidade e constância da produção, principalmente durante o período de verão. 
      {os.linesep} Após a correção da fertilidade do solo, os canteiros são preparados respeitando as dimensões de 1,1 a 1,2m de largura e 0,4m de espaçamento entre si. A altura variará de acordo com o tipo de solo e drenagem. Quanto mais úmido o solo, pior será a sua drenagem, sendo este um indicativo de que os canteiros deverão ser construídos com altura mais elevada. Em regiões de solo arenoso e boa drenagem pode ser dispensado o preparo dos de canteiros, porém, espaços maiores entre plantas devem ser adotados para facilitar o trânsito, realização dos tratos culturais e colheita.
      {os.linesep}Finalizar consulta (S/N)?''' 
    
    if mensagem == '4':
      return f'''Em solos propícios ao cultivo da alface é recomendada a utilização de 200 g de composto orgânico ou esterco de vaca curtido por planta. A aplicação poderá ser feita a lanço antes ou após o preparo dos canteiros devendo-se, logo em seguida, incorporá-los ao solo. Em solos com baixa fertilidade e/ou baixo teor de matéria orgânica, a adubação deverá ser localizada em pequenas “covas”, próximo às mudas. Para o plantio convencional, com a utilização de adubos químicos, seguir as recomendações do Boletim 200 do IAC.
      {os.linesep}Finalizar consulta (S/N)?'''

    if mensagem == '5':
      return f'''Em solos propícios ao cultivo da alface é recomendada a utilização de 200 g de composto orgânico ou esterco de vaca curtido por planta. A aplicação poderá ser feita a lanço antes ou após o preparo dos canteiros devendo-se, logo em seguida, incorporá-los ao solo. Em solos com baixa fertilidade e/ou baixo teor de matéria orgânica, a adubação deverá ser localizada em pequenas “covas”, próximo às mudas. Para o plantio convencional, com a utilização de adubos químicos, seguir as recomendações do Boletim 200 do IAC.
      {os.linesep} A irrigação é fundamental nesta fase, pois o excesso de água propiciará o estabelecimento de doenças causadas por fungos ou bactérias. As mudas estarão aptas para o transplante no campo quando desenvolverem seis folhas definitivas, o que ocorre de 20 a 30 dias após a semeadura, conforme a temperatura do período e dos tratos culturais empregados.
      {os.linesep}Finalizar consulta (S/N)?'''

    if mensagem.lower() in ('s','sim'):
      return 'Agradecemos seu contato, precisando é só chamar!'
    else:
      return 'Gostaria de voltar o menu? Digite "menu"!'

  
  #Responder
  def responder(self,resposta,chat_id):
    #enviar
    link_de_envio = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta}'
    requests.get(link_de_envio)

bot = TelegramBot()
bot.Iniciar()

  
