from flask import Flask, request, jsonify, render_template
import json
import unicodedata

app = Flask(__name__)

# Cargar el contenido del archivo JSONL
def load_intents(file_path):
    intents = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            intents.append(json.loads(line))
    return intents

# Normalizar texto eliminando acentos y convirtiendo a minúsculas
def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

# Buscar una respuesta basada en la pregunta del usuario
def find_response(question, intents):
    normalized_question = normalize_text(question)
    for intent in intents:
        for keyword in intent.get('keywords', []):
            if keyword in normalized_question:
                return next((m['content'] for m in intent['messages'] if m['role'] == 'assistant'), "Lo siento, no tengo una respuesta para eso.")
    return "Lo siento, no tengo una respuesta para eso."

# Ruta principal para el chatbot
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    question = data.get('question', '')
    response = find_response(question, intents)
    return jsonify({'response': response})

# Ruta principal para la página de chat
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    # Cargar las intenciones desde el archivo JSONL
    intents = load_intents('intentemos.jsonl')
    app.run(debug=True)
