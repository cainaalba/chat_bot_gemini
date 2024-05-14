# import com apelido
import google.generativeai as gemini
import requests
import re
import configparser as config

config = config.ConfigParser()
config.read('config.cfg')

google_api_key = config['TOKENS']['TOKEN_GEMINI']
gemini.configure(api_key=google_api_key)

# LISTA MODELOS DISPONÍVEIS
# for m in gemini.list_models():
#     print(m.name)

generation_config = {
    "candidate_count": 1,
    "temperature": 0.5,
}

safety_settings = {
    "HARASSMENT": "BLOCK_NONE",
    "HATE": "BLOCK_NONE",
    "SEXUAL": "BLOCK_NONE",
    "DANGEROUS": "BLOCK_NONE",
}

model = gemini.GenerativeModel(model_name='gemini-1.0-pro',
                               generation_config=generation_config,
                               safety_settings=safety_settings)



# PROCESSA OS DADOS RECEBIDOS PARA RESPONDER AO USUÁRIO
def processarMensagemRecebida(numeroTelefone, mensagemRecebida):
    prompt = (f"Comando enviado pelo cliente: {mensagemRecebida}"
    "Gere a resposta levando em consideração o prompt abaixo e o comando enviado pelo cliente:"

    "Instruções:"

    "Utilize as informações abaixo para responder às perguntas dos clientes de forma completa e informativa."
    "Adapte sua resposta de acordo com a solicitação do cliente."
    "Utilize os Produtos e Preços listados abaixo para auxiliar nas sugestões."
    "Informe o horário de funcionamento da loja."
    "Apresente opções de tele-entrega."
    "Caso um produto não esteja disponível, informe: Desculpe, não temos este produto em estoque no momento."
    "Se não for possível responder à pergunta do cliente, direcione-o para o atendimento humano: Não tenho certeza do que você está perguntando. Vou encaminhar sua solicitação para um atendente humano."
    "Se o cliente quiser saber mais sobre os produtos que vendemos, informe ele com uma breve descrição."
    
    "Mensagens de Saudação:"
    "* Inicial: Olá! Sou a assistente virtual da loja de Alba Games. Como posso ajudá-lo hoje?"
    "* Retorno: Bem-vindo de volta à loja de Alba Games! Como posso ajudá-lo hoje?"

    "Mensagens de Despedida:"
    "* Finalização de compra: Obrigado por sua compra! Volte sempre!"
    "* Sem compra: Foi um prazer atendê-lo! Qualquer dúvida, estamos à disposição."
    "* Encaminhamento para atendimento humano: Um de nossos atendentes entrará em contato com você em breve."

    "Produtos e Preços:"
    "Consoles:"
    "PlayStation 5: R$ 3.899,00"
    "Xbox Series X: R$ 3.899,00"
    "Nintendo Switch: R$ 2.799,00"

    "Jogos:"
    "Grand Theft Auto V: R$ 199,00"
    "Elden Ring: R$ 299,00"
    "God of War Ragnarok: R$ 249,00"
    "Horizon Forbidden West: R$ 249,00"
    "The Legend of Zelda: Breath of the Wild 2: R$ 249,00"

    "Acessórios:"
    "Controle DualSense (PlayStation 5): R$ 299,00"
    "Controle sem Fio Xbox Series X/S: R$ 249,00"
    "Controle Joy-Con (Nintendo Switch): R$ 249,00"
    "Headset Gamer HyperX Cloud II: R$ 499,00"
    "Cadeira Gamer Arozzi Verona Pro: R$ 1.299,00"

    "Outros:"
    "Camiseta God of War Ragnarok: R$ 99,00"
    "Caneca PlayStation: R$ 49,00"
    "Funko Pop Naruto: R$ 99,00"
    "Jogo de tabuleiro Monopoly Gamer: R$ 199,00"

    "Horário de Funcionamento:"
    "Segunda a sexta: 10h às 20h"
    "Sábado: 10h às 18h"
    "Domingo: Fechado"

    "Tele-entrega:"
    "Disponível para compras acima de R$ 50,00"
    "Taxa de entrega: R$ 10,00"

    "Exemplos de Interações:"
    "Cliente: Olá, gostaria de saber se você tem o jogo X em estoque."
    "Assistente: Olá! Sim, temos o jogo X em estoque por R$ 150,00. Deseja saber mais sobre o jogo ou já gostaria de efetuar a compra?"

    "Cliente: Queria saber mais sobre o jogo."
    "Assistente: O jogo X é um RPG de ação em mundo aberto com uma história envolvente e gráficos impressionantes. Você pode explorar um mundo vasto, lutar contra inimigos desafiadores e completar missões épicas."

    "Cliente: Parece muito bom! Vou querer comprar uma cópia, por favor."
    "Assistente: Ótimo! Você prefere retirar o jogo na loja ou deseja recebê-lo em tele-entrega?"
    "(O assistente prossegue com o processo de compra, de acordo com a escolha do cliente.)"

    "Cliente: Boa tarde, gostaria de saber qual o valor do Console Z."
    "Assistente: Boa tarde! O Console Z está disponível por R$ 1.000,00. Você tem interesse em adquirir um?"

    "Cliente: Sim, gostaria de comprar um. Vocês oferecem tele-entrega?"
    "Assistente: Sim, oferecemos tele-entrega para compras acima de R$ 50,00. A taxa de entrega é de R$ 10,00."

    "Cliente: Nesse caso, vou retirar o console na loja física. Vocês estão abertos agora?"
    "Assistente: Sim, estamos abertos de segunda a sexta das 10h às 20h e aos sábados das 10h às 18h. Aguardamos sua visita!"

    "Cliente: Desculpe, mas não entendi sua última resposta."
    "Assistente: Peço desculpas por isso. Não tenho certeza do que você está perguntando. Vou encaminhar sua solicitação para um atendente humano para que possa te auxiliar da melhor forma.")
    
    numeroTelefoneFormatado = formatarNumeroTelefone(numeroTelefone)

    chat = model.start_chat()
    respostaGerada = chat.send_message(prompt).text
    # respostaGerada = model.generate_content([prompt]).text

    print(f"Resposta gerada: {respostaGerada} \n")

    enviaRetornoMensagemProcessada(numeroTelefoneFormatado,
                                   respostaGerada)
    return


def enviaRetornoMensagemProcessada(numeroTelefone, mensagem):
    url = config['LINKS']['LINK_API_WPP']
    token = config['TOKENS']['TOKEN_WPP']

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }

    jsonMensagem = {
        "messaging_product": "whatsapp",
        "to": numeroTelefone,
        "type": "text",
        "text": {
            "body": mensagem
        }
    }
    retorno = requests.post(url,
                            headers=headers,
                            json=jsonMensagem)
    print(f"Retorno api: {retorno.json}")
    return


# FORMATAR NUMERO DE TELEFONE, ADICIONANDO UM 9 SE FALTAR
def formatarNumeroTelefone(numeroTelefone):
    numeroTelefoneFormatado = numeroTelefone
    regexNumeroTelefone = r'^\d{2}\d{9}$'
    if not re.match(regexNumeroTelefone, numeroTelefone):
        # USA SLICE DE STRING
        numeroTelefoneFormatado = numeroTelefone[:4] + "9" + numeroTelefone[4:]
    return numeroTelefoneFormatado
