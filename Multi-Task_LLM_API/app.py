
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from gemini_wrapper import generate_text, generate_code, classify_text

app = Flask(__name__)


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)




@app.route('/generate/text', methods=['POST'])
@limiter.limit("10 per minute")

def generate_text_route():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400
    
    try:
        text = generate_text(prompt)
        return jsonify({'generated_text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate/code', methods=['POST'])
@limiter.limit("10 per minute")
def generate_code_route():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    try:
        code = generate_code(prompt)
        return jsonify({'generated_code': code})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/classify/text', methods=['POST'])
@limiter.limit("10 per minute")
def classify_text_route():
    data = request.get_json()
    text = data.get('text')
    categories = data.get('categories')

    if not text or not categories:
        return jsonify({'error': 'Text and categories are required'}), 400

    try:
        classification = classify_text(text, categories)
        return jsonify({'classification': classification})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
