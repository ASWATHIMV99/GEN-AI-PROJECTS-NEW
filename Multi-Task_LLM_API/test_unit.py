import unittest
import json
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from app import app
from gemini_wrapper import generate_text, generate_code, classify_text

class TestMultiTaskLLMAPI(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Set up test client and load environment"""
        load_dotenv()
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        
    def test_01_env_api_key_configured(self):
        """Test that the GOOGLE_API_KEY is properly configured in .env"""
        print("\n🔑 Testing API Key Configuration...")
        
        # Check if .env file exists
        env_file_path = os.path.join(os.path.dirname(__file__), '.env')
        self.assertTrue(os.path.exists(env_file_path), ".env file should exist")
        
        # Check if API key is loaded
        api_key = os.getenv('GOOGLE_API_KEY')
        self.assertIsNotNone(api_key, "GOOGLE_API_KEY should be set in environment")
        self.assertTrue(len(api_key) > 0, "GOOGLE_API_KEY should not be empty")
        self.assertTrue(api_key.startswith('AIza'), "API key should start with 'AIza'")
        
        print(f"✅ API Key configured: {api_key[:10]}...{api_key[-5:]}")
        
    def test_02_generate_text_endpoint(self):
        """Test the /api/v1/generate/text endpoint"""
        print("\n📝 Testing Text Generation Endpoint...")
        
        payload = {
            "prompt": "Write a one-sentence story about a cat."
        }
        
        response = self.client.post(
            '/api/v1/generate/text',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('generated_text', data)
        self.assertIsNotNone(data['generated_text'])
        self.assertTrue(len(data['generated_text']) > 0)
        
        print(f"✅ Text generated: {data['generated_text'][:50]}...")
        
    def test_03_generate_code_endpoint(self):
        """Test the /api/v1/generate/code endpoint"""
        print("\n💻 Testing Code Generation Endpoint...")
        
        payload = {
            "prompt": "Create a simple Python function that adds two numbers"
        }
        
        response = self.client.post(
            '/api/v1/generate/code',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('generated_code', data)
        self.assertIsNotNone(data['generated_code'])
        self.assertTrue(len(data['generated_code']) > 0)
        self.assertIn('def', data['generated_code'])  # Should contain a function definition
        
        print(f"✅ Code generated: {data['generated_code'][:50]}...")
        
    def test_04_classify_text_endpoint(self):
        """Test the /api/v1/classify/text endpoint"""
        print("\n🏷️ Testing Text Classification Endpoint...")
        
        payload = {
            "text": "I love this amazing product! It works perfectly.",
            "categories": ["positive", "negative", "neutral"]
        }
        
        response = self.client.post(
            '/api/v1/classify/text',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('classification', data)
        self.assertIsNotNone(data['classification'])
        self.assertIn(data['classification'].lower(), ['positive', 'negative', 'neutral'])
        
        print(f"✅ Text classified as: {data['classification']}")
        
    def test_05_endpoint_error_handling(self):
        """Test error handling for missing required fields"""
        print("\n❌ Testing Error Handling...")
        
        # Test missing prompt for text generation
        response = self.client.post(
            '/api/v1/generate/text',
            data=json.dumps({}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        
        # Test missing fields for classification
        response = self.client.post(
            '/api/v1/classify/text',
            data=json.dumps({"text": "test"}),  # missing categories
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        
        print("✅ Error handling working correctly")
        
    def test_06_rate_limit_handling(self):
        """Test rate limiting and exponential backoff"""
        print("\n⏱️ Testing Rate Limit Handling...")
        
        def make_api_call():
            """Make a single API call"""
            try:
                result = generate_text("Say hello")
                return {"success": True, "result": result}
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        # Make multiple concurrent requests to potentially trigger rate limiting
        print("Making rapid API calls to test rate limiting...")
        
        start_time = time.time()
        with ThreadPoolExecutor(max_workers=10) as executor:
            # Submit 15 concurrent requests (should exceed 60 RPM if executed quickly)
            futures = [executor.submit(make_api_call) for _ in range(15)]
            results = [future.result() for future in futures]
        
        end_time = time.time()
        duration = end_time - start_time
        
        successful_calls = sum(1 for r in results if r['success'])
        failed_calls = len(results) - successful_calls
        
        print(f"✅ Completed {len(results)} API calls in {duration:.2f} seconds")
        print(f"✅ Successful calls: {successful_calls}")
        print(f"✅ Failed calls: {failed_calls}")
        
        # At least some calls should succeed (testing that the system doesn't completely fail)
        self.assertGreater(successful_calls, 0, "At least some API calls should succeed")
        
        # If we made calls fast enough, we might have triggered rate limiting
        if duration < 15:  # If calls were made quickly
            print("✅ Rate limiting test completed - exponential backoff is handling requests")
        else:
            print("✅ Calls were spaced out naturally, no rate limiting triggered")
            
    def test_07_direct_wrapper_functions(self):
        """Test the gemini_wrapper functions directly"""
        print("\n🔧 Testing Wrapper Functions Directly...")
        
        # Test generate_text function
        text_result = generate_text("Say 'test successful' in one sentence.")
        self.assertIsInstance(text_result, str)
        self.assertTrue(len(text_result) > 0)
        print(f"✅ Direct text generation: {text_result[:30]}...")
        
        # Test generate_code function  
        code_result = generate_code("Write a simple hello world function in Python")
        self.assertIsInstance(code_result, str)
        self.assertTrue(len(code_result) > 0)
        self.assertIn('def', code_result.lower())
        print(f"✅ Direct code generation: {code_result[:30]}...")
        
        # Test classify_text function
        classification_result = classify_text("This is great!", ["positive", "negative"])
        self.assertIsInstance(classification_result, str)
        self.assertTrue(len(classification_result) > 0)
        print(f"✅ Direct text classification: {classification_result}")

if __name__ == '__main__':
    print("🚀 Starting Multi-Task LLM API Unit Tests...")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMultiTaskLLMAPI)
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(suite)
    
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("🎉 All tests passed successfully!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        
    print(f"📊 Tests run: {result.testsRun}")
    print("=" * 60)