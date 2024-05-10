from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data)  # Aqui você pode processar os dados recebidos do webhook
    return jsonify({'status': 'success'})


@app.route('/', methods=['GET'])
def outra_rota():
    data = request
    print(f"Recebido: {data}")
    return '{"status": "200","challenge": "token_wpp_alba"}'


if __name__ == '__main__':
    app.run(debug=True, port=5555)
