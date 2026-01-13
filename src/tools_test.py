import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import sys

# Suppress gRPC warnings
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'

load_dotenv()

print("="*70)
print("🧪 TESTING TOOLS DIRECTLY")
print("="*70)

# Test 1: Check API Key
print("\n1️⃣  Testing API Key...")
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ FAILED: No API key found in .env")
    sys.exit(1)
print(f"✅ PASSED: API key found (starts with {api_key[:10]}...)")

# Test 2: Configure Gemini
print("\n2️⃣  Configuring Gemini...")
try:
    genai.configure(api_key=api_key)
    print("✅ PASSED: Gemini configured")
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    sys.exit(1)

# Test 3: List Available Models
print("\n3️⃣  Listing available models...")
try:
    models = list(genai.list_models())
    print(f"✅ PASSED: Found {len(models)} models")
    
    print("\n   📋 Available Vision Models:")
    vision_models = []
    for m in models:
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name.replace('models/', '')
            vision_models.append(model_name)
            print(f"      • {model_name}")
    
    if not vision_models:
        print("   ⚠️  WARNING: No vision models found!")
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    sys.exit(1)

# Test 4: Try to initialize a model
print("\n4️⃣  Testing model initialization...")
model_priority = [
    'gemini-1.5-flash-latest',
    'gemini-1.5-flash',
    'gemini-2.0-flash-exp',
    'gemini-2.5-pro-latest',
    'gemini-2.5-pro',
    'gemini-pro-vision'
]

working_model = None
for model_name in model_priority:
    try:
        test_model = genai.GenerativeModel(model_name)
        # Try a simple generation to verify it works
        response = test_model.generate_content("Say hello")
        print(f"✅ PASSED: Model '{model_name}' works!")
        print(f"   Response: {response.text[:50]}...")
        working_model = model_name
        break
    except Exception as e:
        print(f"   ⚠️  Model '{model_name}' failed: {str(e)[:50]}...")
        continue

if not working_model:
    print("❌ FAILED: No working models found!")
    print("\n🔧 TROUBLESHOOTING:")
    print("   1. Get a new API key: https://makersuite.google.com/app/apikey")
    print("   2. Enable Gemini API: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
    print("   3. Check regional restrictions")
    sys.exit(1)

# Test 5: Test with an image (if available)
print("\n5️⃣  Testing vision capability...")
test_images = [
    "examples/food-1.jpg",
    "examples/food-2.jpg",
    "uploaded_image.jpg"
]

test_image = None
for img_path in test_images:
    if os.path.exists(img_path):
        test_image = img_path
        break

if test_image:
    try:
        print(f"   Using test image: {test_image}")
        img = Image.open(test_image)
        model = genai.GenerativeModel(working_model)
        response = model.generate_content(["What food items do you see in this image?", img])
        print(f"✅ PASSED: Vision works!")
        print(f"   Response: {response.text[:100]}...")
    except Exception as e:
        print(f"❌ FAILED: Vision test failed: {str(e)}")
else:
    print("   ⚠️  SKIPPED: No test images found")

# Test 6: Test the actual tool
print("\n6️⃣  Testing ExtractIngredientsTool...")
try:
    from src.tools import ExtractIngredientsTool
    
    if test_image:
        result = ExtractIngredientsTool.extract_ingredient(test_image)
        print(f"✅ PASSED: Tool works!")
        print(f"   Result: {result[:100]}...")
    else:
        print("   ⚠️  SKIPPED: No test image available")
except Exception as e:
    print(f"❌ FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("🎯 SUMMARY")
print("="*70)
print(f"Working Model: {working_model}")
print(f"Vision Capable: {'Yes' if test_image else 'Not tested'}")
print("\n✅ If all tests passed, your setup is correct!")
print("   Run: python app.py")
print("\n❌ If tests failed, check the error messages above")
