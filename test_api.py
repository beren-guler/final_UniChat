#!/usr/bin/env python3
# Gemini API Test Scripti

import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_gemini_api():
    """Gemini API'yi test et ve kota durumunu kontrol et"""
    
    # .env dosyasını yükle
    load_dotenv()
    
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key or api_key == 'your-gemini-api-key-here':
        print("❌ GEMINI_API_KEY bulunamadı veya ayarlanmamış!")
        return False
    
    print(f"🔑 API Key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        # API'yi yapılandır
        genai.configure(api_key=api_key)
        print("✅ API anahtarı yapılandırıldı")
        
        # Modelleri listele
        print("\n📋 Mevcut modeller:")
        models = genai.list_models()
        model_count = 0
        for model in models:
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
                model_count += 1
        
        print(f"📊 Toplam {model_count} model mevcut")
        
        # Basit bir test sorgusu gönder
        print("\n🧪 Test sorgusu gönderiliyor...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        test_prompt = "Merhaba! Bu bir test mesajıdır. Sadece 'Test başarılı!' diye yanıtla."
        
        response = model.generate_content(test_prompt)
        
        if response and response.text:
            print("✅ API başarıyla çalışıyor!")
            print(f"📝 Yanıt: {response.text}")
            return True
        else:
            print("❌ API yanıt vermedi")
            return False
            
    except Exception as e:
        error_msg = str(e).lower()
        
        if 'quota' in error_msg or 'limit' in error_msg:
            print("❌ KOTA HATASI: API kotanız dolmuş!")
            print("💡 Çözüm: Google AI Studio'da yeni API anahtarı oluşturun veya billing ayarlarını kontrol edin.")
        elif 'invalid' in error_msg or 'authentication' in error_msg:
            print("❌ GEÇERSİZ API ANAHTARI!")
            print("💡 Çözüm: API anahtarının doğru olduğundan emin olun.")
        elif 'permission' in error_msg:
            print("❌ İZİN HATASI: API anahtarının izinleri yetersiz!")
        else:
            print(f"❌ BEKLENMEYEN HATA: {e}")
        
        return False

def test_unichat_integration():
    """UniChat entegrasyonunu test et"""
    print("\n" + "="*50)
    print("🔄 UniChat entegrasyonu test ediliyor...")
    
    try:
        # UniChat modülünü import et
        import sys
        sys.path.append('.')
        
        from app import get_gemini_response
        
        # Test sorgusu
        test_response = get_gemini_response(
            user_message="Merhaba, test mesajıdır",
            user_ranking="15000",
            puan_type="1",
            chat_history=[]
        )
        
        if "hata" not in test_response.lower() and len(test_response) > 10:
            print("✅ UniChat entegrasyonu çalışıyor!")
            print(f"📝 Örnek yanıt: {test_response[:100]}...")
            return True
        else:
            print("❌ UniChat entegrasyonunda sorun var")
            print(f"📝 Hata mesajı: {test_response}")
            return False
            
    except Exception as e:
        print(f"❌ UniChat entegrasyonu hatası: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Gemini API Test Başlatılıyor...")
    print("="*50)
    
    api_success = test_gemini_api()
    
    if api_success:
        integration_success = test_unichat_integration()
        
        if integration_success:
            print("\n🎉 TÜM TESTLER BAŞARILI!")
            print("UniChat artık AI özelliklerini kullanabilir.")
        else:
            print("\n⚠️ API çalışıyor ama entegrasyon sorunlu")
    else:
        print("\n❌ API testi başarısız")
        print("UniChat AI özellikleri çalışmayabilir")
    
    print("\n" + "="*50)
