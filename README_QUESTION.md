# Multi-Task LLM API Challenge

## Problem Statement

Build a comprehensive Flask REST API that integrates with Google's Gemini 2.0 Flash model to provide three distinct AI-powered services: text generation, code generation, and text classification. Your implementation must include enterprise-grade features such as rate limiting, retry logic with exponential backoff, comprehensive error handling, and interactive API documentation.

## Requirements

### Core Functionality
Your API must implement the following three endpoints:

1. **Text Generation Endpoint** (`POST /api/v1/generate/text`)
   - Accept a JSON payload with a `prompt` field
   - Use Gemini 2.0 Flash with temperature 0.7 for creative text generation
   - Return generated text in JSON format

2. **Code Generation Endpoint** (`POST /api/v1/generate/code`) 
   - Accept a JSON payload with a `prompt` field
   - Use Gemini 2.0 Flash with temperature 0.2 for consistent code generation
   - Return generated code in JSON format

3. **Text Classification Endpoint** (`POST /api/v1/classify/text`)
   - Accept a JSON payload with `text` and `categories` fields
   - Use Gemini 2.0 Flash with temperature 0.0 for deterministic classification
   - Return the most appropriate category from the provided list

### Technical Requirements

#### 1. API Framework & Documentation
- Use Flask with Flask-RESTX for automatic Swagger UI generation
- Implement proper API versioning (v1)
- Provide interactive documentation accessible at `/swagger/`
- Include comprehensive OpenAPI specifications for all endpoints

#### 2. Rate Limiting
- Implement multi-tier rate limiting using Flask-Limiter:
  - Global: 200 requests/day, 50 requests/hour
  - Per endpoint: 10 requests/minute
- Handle Gemini API's 60 RPM limit with intelligent retry logic

#### 3. Retry Logic & Error Handling
- Implement exponential backoff for API rate limits:
  - Initial delay: 1 second
  - Max delay: 60 seconds
  - Max retries: 5 attempts
  - Exponential multiplier
- Handle HTTP 429, quota exceeded, and resource exhausted errors
- Provide meaningful error messages with appropriate HTTP status codes

#### 4. Architecture & Code Quality
- Create a separate `gemini_wrapper.py` module for LLM interactions
- Use environment variables for secure API key management
- Implement comprehensive logging for monitoring and debugging
- Follow modular design principles with separation of concerns

#### 5. Configuration Management
- Load Google API key from environment variables
- Support `.env` file configuration
- Validate required environment variables on startup

### Input/Output Specifications

#### Text Generation
**Request:**
```json
{
  "prompt": "Write a short story about a robot discovering emotions"
}
```

**Response:**
```json
{
  "generated_text": "Unit 734, designated 'Custodian,' had cleaned the same corridors for three thousand days..."
}
```

#### Code Generation
**Request:**
```json
{
  "prompt": "Create a Python function to calculate fibonacci numbers recursively"
}
```

**Response:**
```json
{
  "generated_code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)"
}
```

#### Text Classification
**Request:**
```json
{
  "text": "This product exceeded my expectations! Amazing quality and fast shipping.",
  "categories": ["positive", "negative", "neutral"]
}
```

**Response:**
```json
{
  "classification": "positive"
}
```

### Error Handling Requirements

Your API must handle and return appropriate responses for:

- **400 Bad Request**: Missing required fields, invalid JSON
- **429 Too Many Requests**: Rate limit exceeded
- **500 Internal Server Error**: Gemini API failures, configuration issues

**Error Response Format:**
```json
{
  "error": "Detailed error message explaining the issue"
}
```

## Test Cases

Your implementation will be evaluated against the following test scenarios:

### Functionality Tests
1. **Basic Endpoint Testing**
   - All three endpoints return valid responses for correct inputs
   - Response format matches specifications
   - Different temperature settings produce appropriate outputs

2. **Input Validation**
   - Missing prompt/text fields return 400 error
   - Invalid JSON payloads are handled gracefully
   - Empty categories list for classification returns appropriate error

3. **Rate Limiting**
   - Per-minute rate limits are enforced correctly
   - Rate limit headers are included in responses
   - Exceeded limits return 429 status code

4. **Retry Logic**
   - Simulated Gemini API rate limits trigger exponential backoff
   - Maximum retry attempts are respected
   - Exponential delay intervals are correctly implemented

5. **Environment Configuration**
   - Missing API key prevents application startup
   - Valid API key allows successful initialization
   - Configuration is loaded from environment variables

### Integration Tests
1. **Swagger UI Accessibility**
   - `/swagger/` endpoint serves interactive documentation
   - All endpoints are documented with proper schemas
   - API can be tested directly through Swagger interface

2. **Error Propagation**
   - Gemini API errors are properly caught and formatted
   - Network timeouts are handled gracefully
   - Invalid API responses don't crash the application

### Performance Tests
1. **Concurrent Requests**
   - API handles multiple simultaneous requests
   - Rate limiting works correctly under load
   - Memory usage remains stable

2. **Large Payloads**
   - Long prompts are processed successfully
   - Large classification category lists are handled
   - Response times remain reasonable

## Implementation Guidelines

### Project Structure
```
Multi-Task_LLM_API/
├── app.py                 # Main Flask application
├── gemini_wrapper.py      # Gemini API integration layer
├── requirements.txt       # Dependencies
├── test_unit.py          # Unit test suite
├── .env.example          # Environment template
└── README.md             # Documentation
```

### Required Dependencies
- Flask & Flask-RESTX for web framework and documentation
- Flask-Limiter for rate limiting
- python-dotenv for environment management
- langchain & langchain-google-genai for Gemini integration
- tenacity for retry logic

### Key Implementation Notes
- Use LangChain's ChatGoogleGenerativeAI for Gemini integration
- Implement proper request/response models using Flask-RESTX
- Include comprehensive logging with appropriate log levels
- Use tenacity decorators for clean retry implementation
- Ensure thread safety for concurrent request handling

## Evaluation Criteria

Your solution will be scored based on:

1. **Correctness (40%)**
   - All endpoints function as specified
   - Proper response formats and status codes
   - Accurate error handling

2. **Rate Limiting & Resilience (25%)**
   - Correct rate limit implementation
   - Effective exponential backoff strategy
   - Graceful degradation under load

3. **Code Quality (20%)**
   - Clean, modular architecture
   - Proper separation of concerns
   - Comprehensive error handling

4. **Documentation & Testing (15%)**
   - Working Swagger UI
   - Comprehensive test coverage
   - Clear code documentation

## Submission Requirements

1. Complete source code with all required files
2. `requirements.txt` with pinned dependency versions
3. `.env.example` file showing required environment variables
4. Unit test suite demonstrating functionality
5. README.md with setup and usage instructions

## Time Limit
4 hours

## Difficulty Level
Intermediate to Advanced

---

**Note**: Ensure you have a valid Google Cloud API key with Gemini API access enabled before beginning implementation. The test environment will provide mock responses for evaluation purposes.
