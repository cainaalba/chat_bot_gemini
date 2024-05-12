from flask import Flask, request, jsonify
from urllib.parse import urlparse, parse_qs
import chat
import json
import configparser as config

config = config.ConfigParser()
config.read('config.cfg')

app = Flask(__name__)

# RECEBE AS MENSAGENS DA CONVERSA DO WHATSAPP
@app.route('/', methods=['POST'])
def receberMensagem():
    dadosRecebidos = request.json
    print(f"JSON Recebido -> {dadosRecebidos}")
    
    dadosRecebidosFormatados = formatarDadosRecebidos(dadosRecebidos)
    if dadosRecebidosFormatados is None:
        return
    
    deserializarJson(dadosRecebidosFormatados)
    return jsonify({'status': 'success'})
    

@app.route('/', methods=['GET'])
def receberRequisicoesConfiguracaoWebhook():
    urlRecebida = request.url
    
    # "QUEBRA" URL PARA EXTRAIR OS PARÂMETROS
    parse = urlparse(urlRecebida)
    parametros = parse_qs(parse.query)
    print(f"Parse parametros: {parametros}")
    
    challenge = ''
    if 'hub.verify_token' in parametros:
        if parametros['hub.verify_token'][0] == config['TOKENS']['TOKEN_WPP_WEBHOOK']:
            if 'hub.challenge' in parametros:
                challenge = parametros['hub.challenge'][0]
                print(f"Challenge: {challenge}")
        else:
            print(f"Token invalido: {parametros['hub.verify_token']}")
    else:
        print('Token não localizado')
    return challenge

def formatarDadosRecebidos(dados):
    try:
        dadosFormatados = str(dados)
        # SUBSTITUI ASPAS SIMPLES POR DUPLAS
        if dadosFormatados.__contains__("'"):
            dadosFormatados = dadosFormatados.replace("'",'"')
        return dadosFormatados
    except TypeError as typeError:
        print(f"KeyError -> {typeError}")
        return None

# DESERIALIZA O JSON
def deserializarJson(dados):
    try:
        jsonDeserializado = json.loads(str(dados))
        print(f"JSON Deserializado -> {jsonDeserializado}")
        try:
            # BUSCA OBJETOS from E body - FEITO DIRETO ASSIM, PARA SOMENTE BUSCAR QUANDO FOR MENSAGENS ENVIADAS PELOS USUÁRIOS E NÃO OS RETORNOS DA API
            numeroRemetente = jsonDeserializado["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
            mensagem = jsonDeserializado["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
            print(f"Número remetente-> {numeroRemetente} \n")
            print(f"Mensagem -> {mensagem} \n")
            
            return chat.processarMensagemRecebida(numeroRemetente,
                                                  mensagem)
        except KeyError as keyError:
            print(f"KeyError -> {keyError}")
            return None
    except json.JSONDecodeError as decodeError:
        print(f"JSONDecodeError -> {decodeError}")
    return None

if __name__ == '__main__':
    app.run(debug=True, port=5555)
