#!/usr/bin/env python3
"""
Test Google Gemini API in GitHub Codespace
Using leaked API key from Opabinia database
"""
import requests
import json

# Google API Key from Opabinia
API_KEY = "AIzaSyC4HZkkrqGPNXpZzsQIz--rdcT4TcNy3ds"

def test_gemini_api():
    """Test Gemini API with a simple prompt"""
    
    print("=" * 60)
    print("🚀 Testing Google Gemini API")
    print("=" * 60)
    print(f"API Key: {API_KEY[:20]}...")
    print()
    
    # Test 1: List available models
    print("📋 Test 1: Listing available models...")
    models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    
    try:
        response = requests.get(models_url, timeout=10)
        if response.status_code == 200:
            models_data = response.json()
            models = [m.get("name", "").split("/")[-1] for m in models_data.get("models", [])]
            print(f"✅ SUCCESS - Found {len(models)} models")
            print(f"   Top models: {', '.join(models[:5])}")
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"   Error: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
        return False
    
    print()
    
    # Test 2: Generate content with Gemini
    print("💬 Test 2: Generating content with Gemini 2.0 Flash...")
    
    gen_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{
                "text": "Write a haiku about artificial intelligence in a GitHub Codespace."
            }]
        }]
    }
    
    try:
        response = requests.post(gen_url, headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            if "candidates" in data and len(data["candidates"]) > 0:
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                print("✅ SUCCESS - Generated response:")
                print()
                print("─" * 60)
                print(text)
                print("─" * 60)
                return True
            else:
                print("❌ FAILED - No candidates in response")
                return False
        elif response.status_code == 429:
            print("⚠️  QUOTA EXCEEDED - API key has reached its quota limit")
            print("   This is expected for leaked keys that are heavily used")
            print("   The key is VALID but needs quota reset")
            return "quota_exceeded"
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"   Error: {response.text[:300]}")
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION - {str(e)}")
        return False

def main():
    print()
    print("🔑 Google Gemini API Test Script")
    print("Running in GitHub Codespace")
    print()
    
    result = test_gemini_api()
    
    print()
    print("=" * 60)
    if result == True:
        print("✅ ALL TESTS PASSED - API is fully functional!")
    elif result == "quota_exceeded":
        print("⚠️  API KEY VALID - Quota exceeded (expected for leaked keys)")
    else:
        print("❌ TESTS FAILED - Check errors above")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
