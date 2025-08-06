#!/usr/bin/env python3
# UniChat Test ve Demo Scripti

import sys
import os
import json

def test_dependencies():
    """Gerekli bağımlılıkları test et"""
    print("UniChat Test Başlatılıyor...")
    print("============================")
    
    try:
        import flask
        print('✓ Flask yüklü')
    except ImportError:
        print('✗ Flask yüklü değil - pip install flask')
        return False

    try:
        import google.generativeai as genai
        print('✓ Google Generative AI yüklü')
    except ImportError:
        print('✗ Google Generative AI yüklü değil - pip install google-generativeai')

    try:
        from dotenv import load_dotenv
        print('✓ python-dotenv yüklü')
    except ImportError:
        print('✗ python-dotenv yüklü değil - pip install python-dotenv')
    
    return True

def test_data_files():
    """JSON veri dosyalarını test et"""
    files_to_check = ['siralamadata.json', 'siralamadata2_ea.json', 'siralamadata3_sozel.json']
    
    for file in files_to_check:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f'✓ {file} - {len(data)} kayıt')
            except Exception as e:
                print(f'✗ {file} - Hata: {e}')
                return False
        else:
            print(f'✗ {file} - Dosya bulunamadı')
            return False
    
    return True

def test_env_file():
    """Environment dosyasını test et"""
    if os.path.exists('.env'):
        print('✓ .env dosyası mevcut')
        try:
            from dotenv import load_dotenv
            load_dotenv()
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key and api_key != 'your-gemini-api-key-here':
                print('✓ GEMINI_API_KEY ayarlanmış')
            else:
                print('⚠ GEMINI_API_KEY ayarlanmamış veya varsayılan değerde')
        except Exception as e:
            print(f'✗ .env dosyası okunamadı: {e}')
    else:
        print('⚠ .env dosyası bulunamadı')

def show_demo_commands():
    """Demo komutlarını göster"""
    print("\nDemo için örnek sorular:")
    print("- Sabancı üniversitesindeki bölümler nelerdir?")
    print("- Koç üniversitesindeki bölümler")
    print("- 15000 sıralamayla hangi bölümlere girebilirim?")
    print("- Bana öneri verir misin?")
    print("- Hangi üniversiteler var?")
    print("")
    print("Uygulamayı başlatmak için: python app.py")

if __name__ == "__main__":
    if test_dependencies():
        test_data_files()
        test_env_file()
        print('\nTest tamamlandı!')
        show_demo_commands()
