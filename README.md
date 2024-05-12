Projeto de uma assistente virtual com IA em **Python**, integrado à API do **WhatsApp Business** e ao **Google Gemini** através da biblioteca _google.generativeai_.

O número de celular de testes, recebe as mensagens no whatsapp, que são processdas pelo webhook e pelas funções python. O _body_ do json recebido é extraído e, 
junto com um **prompt modelo** (solicitei ao Gemini gerar um promopt de uma loja de games, com algumas instruções) é enviado à IA Google Gemini que devolve uma **resposta**, 
de acordo com os parâmetros definidos no prompt. A resposta é enviada ao rementente original.

**Instruções de configuração:**
Criar uma conta no Meta Developers e um app criado com a Api do WhatsApp e Webhook.
Configurar um link público no webhook da api do WhatsApp Business, no modelo Whatsapp Business Account. Ao salvar,  api do whatsapp envia uma requisição _GET_ para o link, que deve devolver o valor do parâmetro _hub.challenge_, que vem na url da requisição.

Neste modelo, foi usado o **Ngrok** para criar um link público, apontando para o _http://localhost:5555_ - configurado no arquivo _webhook.py_. 

Baixe o Ngrok _https://ngrok.com/download_.

Para iniciar o Ngrok, navegue até a pasta onde o arquivo baixado foi extraído, via terminal, e rode o comando: _./ngrok http http://localhost:5555_

<img width="492" alt="Captura de Tela 2024-05-12 às 19 11 07" src="https://github.com/cainaalba/chat_bot_gemini/assets/57020103/cdec6127-03fc-49b1-9eb5-47f376888e7e">

A url para enviar a mensagem ao rementente, é gerada no app da api do whatsapp no Meta Developers, bem como o token.

**Projeto ainda está na versão inicial.**

**Modelo de arquivo config.cfg:**

![image](https://github.com/cainaalba/chat_bot_gemini/assets/57020103/c29813b5-d63e-457a-8b86-4ea84338b3fa)

Para iniciar o projeto rode o arquivo _webhook.py_.

**Prints da execução**

![Captura de Tela 2024-05-11 às 22 32 49](https://github.com/cainaalba/chat_bot_gemini/assets/57020103/c36c4511-3658-4bfa-947f-aab0e4d20b35)

![Captura de Tela 2024-05-11 às 22 33 15](https://github.com/cainaalba/chat_bot_gemini/assets/57020103/f5c7794a-3b16-429a-8bf2-e237cb06e57d)

![Captura de Tela 2024-05-11 às 22 33 39](https://github.com/cainaalba/chat_bot_gemini/assets/57020103/e286e91c-0ffa-496d-ae81-321033dfd68a)

![Captura de Tela 2024-05-11 às 22 34 20](https://github.com/cainaalba/chat_bot_gemini/assets/57020103/97c69e44-b230-4838-a328-7bc5ab2f4c21)
