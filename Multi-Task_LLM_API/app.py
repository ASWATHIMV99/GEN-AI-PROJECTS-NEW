
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from gemini_wrapper import generate_text, generate_code, classify_text

app = Flask(__name__)

api = Api(
    app, 
    version='1.0', 
    title='Multi-Task LLM API',
    description='A Flask API that provides text generation, code generation, and text classification using Google Gemini Pro',
    doc='/swagger/',
    prefix='/api/v1'
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

ns_generate = api.namespace('generate', description='Text and code generation operations')
ns_classify = api.namespace('classify', description='Text classification operations')

text_generation_model = api.model('TextGeneration', {
    'prompt': fields.String(required=True, description='The text prompt for generation', example='Write a short story about a robot')
})

code_generation_model = api.model('CodeGeneration', {
    'prompt': fields.String(required=True, description='The prompt for code generation', example='Create a Python function to calculate fibonacci numbers')
})

text_classification_model = api.model('TextClassification', {
    'text': fields.String(required=True, description='The text to classify', example='This movie was amazing!'),
    'categories': fields.List(fields.String, required=True, description='List of categories to classify into', example=['positive', 'negative', 'neutral'])
})

text_response_model = api.model('TextResponse', {
    'generated_text': fields.String(description='The generated text response')
})

code_response_model = api.model('CodeResponse', {
    'generated_code': fields.String(description='The generated code response')
})

classification_response_model = api.model('ClassificationResponse', {
    'classification': fields.String(description='The classification result')
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message')
})




@ns_generate.route('/text')
class TextGeneration(Resource):
    @ns_generate.expect(text_generation_model)
    @ns_generate.doc(
        description='Generate text based on a given prompt using Google Gemini Pro',
        responses={
            200: 'Success - Text generated',
            400: 'Bad Request - Missing prompt',
            500: 'Internal Server Error'
        }
    )
    @limiter.limit("10 per minute")
    def post(self):
        data = request.get_json()
        prompt = data.get('prompt')
        if not prompt:
            return {'error': 'Prompt is required'}, 400
        
        try:
            text = generate_text(prompt)
            return {'generated_text': text}
        except Exception as e:
            return {'error': str(e)}, 500

@ns_generate.route('/code')
class CodeGeneration(Resource):
    @ns_generate.expect(code_generation_model)
    @ns_generate.doc(
        description='Generate code based on a given prompt using Google Gemini Pro with optimized settings for code generation',
        responses={
            200: 'Success - Code generated',
            400: 'Bad Request - Missing prompt',
            500: 'Internal Server Error'
        }
    )
    @limiter.limit("10 per minute")
    def post(self):
        data = request.get_json()
        prompt = data.get('prompt')

        if not prompt:
            return {'error': 'Prompt is required'}, 400

        try:
            code = generate_code(prompt)
            return {'generated_code': code}
        except Exception as e:
            return {'error': str(e)}, 500

@ns_classify.route('/text')
class TextClassification(Resource):
    @ns_classify.expect(text_classification_model)
    @ns_classify.doc(
        description='Classify text into one of the provided categories using Google Gemini Pro',
        responses={
            200: 'Success - Text classified',
            400: 'Bad Request - Missing text or categories',
            500: 'Internal Server Error'
        }
    )
    @limiter.limit("10 per minute")
    def post(self):
        data = request.get_json()
        text = data.get('text')
        categories = data.get('categories')

        if not text or not categories:
            return {'error': 'Text and categories are required'}, 400

        try:
            classification = classify_text(text, categories)
            return {'classification': classification}
        except Exception as e:
            return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=True)
