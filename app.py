from flask import Flask, render_template, request, jsonify
import json
import re
from datetime import datetime
import uuid
import os
from dotenv import load_dotenv
import google.generativeai as genai

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)

# Chat geçmişini hafızada tutmak için sunucu tarafında sözlük
chats = {}

# Gemini API anahtarını çevre değişkeninden al
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# JSON dosyalarını yükle
def load_data():
    with open('siralamadata.json', 'r', encoding='utf-8') as f:
        sayisal_data = json.load(f)
    
    with open('siralamadata2_ea.json', 'r', encoding='utf-8') as f:
        ea_data = json.load(f)
    
    with open('siralamadata3_sozel.json', 'r', encoding='utf-8') as f:
        sozel_data = json.load(f)
    
    return sayisal_data, ea_data, sozel_data

# Türk alfabesini İngilizce'ye çevir
def tr_to_en(text):
    tr_chars = "çğıöşüÇĞIÖŞÜ"
    en_chars = "cgiosuCGIOSU"
    
    for tr_char, en_char in zip(tr_chars, en_chars):
        text = text.replace(tr_char, en_char)
    
    return text

# Üniversite bölümlerini bul
def find_university_departments(university_name, puan_type):
    sayisal_data, ea_data, sozel_data = load_data()
    
    # Puan türüne göre veri setini seç
    if puan_type == "1":
        data = sayisal_data
    elif puan_type == "2":
        data = ea_data
    elif puan_type == "3":
        data = sozel_data
    else:
        return []
    
    # Üniversite adını normalize et
    university_name = tr_to_en(university_name.upper().strip())
    
    departments = []
    for entry in data:
        uni_name = tr_to_en(entry['universite'].upper().strip())
        
        # Daha esnek arama: üniversite adının bir kısmı eşleşirse
        if university_name in uni_name or uni_name.find(university_name) != -1:
            departments.append({
                'universite': entry['universite'].strip(),
                'bolum': entry['bolum'].strip(),
                'siralama': entry['siralama'],
                'puan': entry['puan']
            })
    
    # Benzersiz bölümleri al (aynı bölüm birden fazla kez olabilir)
    unique_departments = []
    seen_departments = set()
    
    for dept in departments:
        dept_key = f"{dept['universite']}_{dept['bolum']}"
        if dept_key not in seen_departments:
            seen_departments.add(dept_key)
            unique_departments.append(dept)
    
    return unique_departments

# Sıralama önerisi veren fonksiyon
def get_ranking_suggestions(user_ranking, puan_type, limit=10):
    """Kullanıcının sıralamasına göre girebileceği bölümleri önerir"""
    sayisal_data, ea_data, sozel_data = load_data()
    
    # Puan türüne göre veri setini seç
    if puan_type == "1":
        data = sayisal_data
    elif puan_type == "2":
        data = ea_data
    elif puan_type == "3":
        data = sozel_data
    else:
        return []
    
    def sanitize(value):
        """Remove non-digit characters and convert to int"""
        if value is None:
            return None
        digits = re.sub(r"[^0-9]", "", str(value))
        return int(digits) if digits else None

    user_ranking = sanitize(user_ranking)
    if user_ranking is None:
        return []
    
    suitable_departments = []
    
    for entry in data:
        ranking_data = parse_ranking_data(entry['siralama'])
        
        # Son 3 yıl ortalamasını al
        rankings = []
        for year in ['2024', '2023', '2022']:
            rank_val = sanitize(ranking_data.get(year))
            if rank_val is not None:
                rankings.append(rank_val)
        
        if rankings:
            avg_ranking = sum(rankings) / len(rankings)
            # Kullanıcının sıralaması ortalama sıralamadan iyi ise
            if user_ranking <= avg_ranking * 1.1:  # %10 tolerans
                suitable_departments.append({
                    'universite': entry['universite'].strip(),
                    'bolum': entry['bolum'].strip(),
                    'avg_ranking': avg_ranking,
                    'last_rankings': ranking_data
                })
    
    # Sıralamaya göre sırala
    suitable_departments.sort(key=lambda x: x['avg_ranking'])
    
    return suitable_departments[:limit]

# Popüler üniversiteleri listeleme
def get_popular_universities(puan_type):
    """Popüler üniversiteleri listeler"""
    sayisal_data, ea_data, sozel_data = load_data()
    
    # Puan türüne göre veri setini seç
    if puan_type == "1":
        data = sayisal_data
    elif puan_type == "2":
        data = ea_data
    elif puan_type == "3":
        data = sozel_data
    else:
        return []
    
    # Üniversiteleri say
    uni_count = {}
    for entry in data:
        uni_name = entry['universite'].strip()
        uni_count[uni_name] = uni_count.get(uni_name, 0) + 1
    
    # En çok bölümü olan üniversiteleri sırala
    sorted_unis = sorted(uni_count.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_unis[:15]  # İlk 15 üniversite
def parse_ranking_data(ranking_str):
    """
    Sıralama string'ini parse eder: "---/122/98/98" -> 2025/2024/2023/2022
    """
    parts = ranking_str.split('/')
    years = ['2025', '2024', '2023', '2022']
    
    result = {}
    for i, part in enumerate(parts):
        if i < len(years):
            result[years[i]] = part if part != '---' else None
    
    return result

# Chat geçmişini yönet
def get_chat_history():
    """Sunucu tarafındaki sohbet geçmişini döndür."""
    return chats

def save_chat_message(chat_id, message, sender):
    """Belirtilen sohbet kimliği için mesajı kaydet."""
    if chat_id not in chats:
        chats[chat_id] = {
            'id': chat_id,
            'title': message[:30] + '...' if len(message) > 30 else message,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'messages': []
        }

    chats[chat_id]['messages'].append({
        'message': message,
        'sender': sender,
        'timestamp': datetime.now().isoformat()
    })
    chats[chat_id]['last_updated'] = datetime.now().isoformat()

# Gemini API ile soru-cevap
def get_gemini_response(user_message, user_ranking, puan_type, chat_history):
    try:
        if not GEMINI_API_KEY:
            return "Gemini API anahtarı bulunamadı. Lütfen .env dosyasında GEMINI_API_KEY'i ayarlayın."
            
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Puan türü açıklaması
        puan_type_names = {
            "1": "Sayısal",
            "2": "Eşit Ağırlık", 
            "3": "Sözel"
        }
        
        # Kullanıcının sıralama ve puan türü bilgilerini context'e ekle
        context = f"""
        Sen bir üniversite tercihi danışmanlık asistanısın. Kullanıcının 2025 YKS sıralaması: {user_ranking}
        Puan türü: {puan_type_names.get(puan_type, "Bilinmiyor")} ({puan_type})
        
        Sıralama verileri şu format'ta: "2025/2024/2023/2022" yılları için sıralama bilgileri
        "---" boş veri anlamına gelir.
        
        Kullanıcının geçmiş yıllardaki verilere göre hangi bölümlere girebileceği konusunda tavsiyelerde bulun.
        2025 verisi genellikle boş olduğu için 2024, 2023, 2022 yıllarındaki verileri referans al.
        
        Chat geçmişi:
        {chr(10).join([f"{msg['sender']}: {msg['message']}" for msg in chat_history[-5:]])}
        
        Kullanıcının sorularını bu bilgilere göre yanıtla. Türkçe yanıt ver.
        """
        
        full_prompt = context + "\n\nKullanıcı Sorusu: " + user_message
        response = model.generate_content(full_prompt)
        return response.text
    
    except Exception as e:
        return f"Üzgünüm, AI yanıtı alınamadı. Hata: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_chat')
def new_chat():
    chat_id = str(uuid.uuid4())
    return jsonify({'chat_id': chat_id})

@app.route('/get_chats')
def get_chats():
    chats = get_chat_history()
    # Son güncelleme tarihine göre sırala
    sorted_chats = sorted(chats.values(), key=lambda x: x['last_updated'], reverse=True)
    return jsonify(sorted_chats)

@app.route('/get_chat/<chat_id>')
def get_chat(chat_id):
    chats = get_chat_history()
    return jsonify(chats.get(chat_id, {}))

@app.route('/delete_chat/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    chats = get_chat_history()
    if chat_id in chats:
        del chats[chat_id]
        return jsonify({'success': True, 'message': 'Chat başarıyla silindi'})
    else:
        return jsonify({'success': False, 'message': 'Chat bulunamadı'}), 404

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    message = data.get('message', '')
    chat_id = data.get('chat_id', str(uuid.uuid4()))
    user_ranking = data.get('user_ranking', '')
    puan_type = data.get('puan_type', '1')
    
    # Kullanıcı mesajını kaydet
    save_chat_message(chat_id, message, 'user')
    
    # Chat geçmişini al
    chats = get_chat_history()
    chat_history = chats.get(chat_id, {}).get('messages', [])
    
    response = ""
    
    # Üniversite bölümleri sorgusu kontrolü - daha kapsamlı pattern
    university_patterns = [
        r'(\w+)\s*(üniversite|university)\s*(.*?)\s*(bölüm|department|fakülte)',
        r'(\w+)\s*(üniversite|university)\s*(.*?)de\s*(bölüm|department)',
        r'(\w+)\s*(üniversite|university)\s*(.*?)deki\s*(bölüm|department)',
        r'(\w+)\s*(üniversite|university)\s*(.*?)ndeki\s*(bölüm|department)',
        r'(\w+)\s*(üniversite|university)\s*(.*?)da\s*(ne|hangi)',
        r'(\w+)\s*(üniversite|university)\s*(.*?)de\s*(ne|hangi)',
        r'(\w+)\s*üni\s*(.*?)\s*(bölüm|department)',
        r'(\w+)\s*(üniversite|university).*?(bölüm|department|program)'
    ]
    
    university_match = None
    for pattern in university_patterns:
        match = re.search(pattern, message.lower())
        if match:
            university_match = match
            break
    
    if university_match:
        university_name = university_match.group(1)
        departments = find_university_departments(university_name, puan_type)
        
        if departments:
            response = f"🎓 {university_name.title()} Üniversitesi'ndeki bölümler ({len(departments)} adet):\n\n"
            for i, dept in enumerate(departments[:25], 1):  # İlk 25 bölümü göster
                ranking_data = parse_ranking_data(dept['siralama'])
                response += f"{i}. 📚 {dept['bolum']}\n"
                
                # Son 3 yıl sıralamaları
                rankings = []
                for year in ['2024', '2023', '2022']:
                    if ranking_data.get(year) and ranking_data[year] != '---':
                        rankings.append(f"{year}: {ranking_data[year]}")
                
                if rankings:
                    response += f"   📊 Son sıralamaları: {' | '.join(rankings)}\n"
                else:
                    response += f"   📊 Sıralama verisi mevcut değil\n"
                response += "\n"
                
            if len(departments) > 25:
                response += f"... ve {len(departments) - 25} bölüm daha var.\n"
        else:
            response = f"❌ {university_name.title()} Üniversitesi için {['sayısal', 'eşit ağırlık', 'sözel'][int(puan_type)-1]} puan türünde bölüm bulunamadı.\n\n"
            response += "💡 İpucu: Üniversite adını tam olarak yazmayı deneyin (örn: 'Sabancı', 'Koç', 'Bilkent')"
    else:
        # Gemini API ile genel soru-cevap
        # Özel komutları kontrol et
        if any(word in message.lower() for word in ['öneri', 'tavsiye', 'girebilir', 'hangi bölüm']):
            # Sıralama önerisi
            if user_ranking:
                clean_ranking = re.sub(r"[^0-9]", "", user_ranking)
                if clean_ranking:
                    suggestions = get_ranking_suggestions(clean_ranking, puan_type, 15)
                    if suggestions:
                        response = f"🎯 {int(clean_ranking)}. sıralamanızla girebileceğiniz bölümler:\n\n"
                        for i, dept in enumerate(suggestions, 1):
                            response += f"{i}. 🏛️ {dept['universite']}\n"
                            response += f"   📚 {dept['bolum']}\n"
                            response += f"   📊 Ortalama sıralama: {int(dept['avg_ranking'])}\n\n"
                    else:
                        response = f"😔 {int(clean_ranking)}. sıralamanızla direkt girebileceğiniz bölüm bulunamadı.\n"
                        response += "💡 Daha yüksek sıralamadaki bölümleri de değerlendirebilir ve tercih listesine ekleyebilirsiniz."
                else:
                    response = "Öneri verebilmem için lütfen sıralamanızı yukarıdaki alana girin."
            else:
                response = "Öneri verebilmem için lütfen sıralamanızı yukarıdaki alana girin."
        
        elif any(word in message.lower() for word in ['üniversite', 'university', 'hangi üniversite']):
            # Popüler üniversiteleri listele
            popular_unis = get_popular_universities(puan_type)
            puan_type_names = ["sayısal", "eşit ağırlık", "sözel"]
            response = f"🏫 {puan_type_names[int(puan_type)-1].title()} puan türünde popüler üniversiteler:\n\n"
            for i, (uni, count) in enumerate(popular_unis, 1):
                response += f"{i}. {uni} ({count} bölüm)\n"
            response += "\n💡 Herhangi bir üniversitenin bölümlerini görmek için 'X üniversitesindeki bölümler nelerdir?' şeklinde sorun."
        
        else:
            # Genel AI yanıtı
            response = get_gemini_response(message, user_ranking, puan_type, chat_history)
    
    # Bot cevabını kaydet
    save_chat_message(chat_id, response, 'bot')
    
    return jsonify({
        'response': response,
        'chat_id': chat_id
    })

@app.route('/search_departments', methods=['POST'])
def search_departments():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    university_name = data.get('university_name', '')
    puan_type = data.get('puan_type', '1')
    
    departments = find_university_departments(university_name, puan_type)
    return jsonify(departments)

@app.route('/test_ai')
def test_ai():
    """AI API'sini test etmek için endpoint"""
    try:
        test_response = get_gemini_response(
            user_message="Merhaba! Bu bir test mesajıdır. Kısa bir yanıt ver.",
            user_ranking="15000",
            puan_type="1",
            chat_history=[]
        )
        return jsonify({
            'status': 'success',
            'message': 'AI başarıyla çalışıyor!',
            'response': test_response
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'AI hatası: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
