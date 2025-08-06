# UniChat - Üniversite Tercihi Danışmanlık Chatbotu

Bu proje, öğrencilerin üniversite tercihi yapmalarına yardımcı olan bir AI destekli chatbot uygulamasıdır.

## 📁 Dosya Yapısı

```
final_UniChat/
├── templates/
│   └── 🎨 index.html            # Web arayüzü
├── datascrap/
│   └── 📖 sıralama.py           # Sıralama ile ilgili jsonları çekerken kullanılandı(Entegre değil jürilerin görmesi için eklendi)
│   └── 💰 ucret.py              # Vakıf üniversitelerinin ücret verilerini çekerken kullanıldı(Entegre değil jürilerin görmesi için eklendi)
├── 🚀 start.sh                   # Hızlı başlatma scripti
├── 🔧 run.sh                     # Gelişmiş başlatma scripti  
├── 🎯 demo.sh                    # Demo ve test scripti
├── 🐍 app.py                     # Ana Flask uygulaması
├── 🧪 test.py                    # Sistem test scripti
├── 🤖 test_api.py                # AI API test scripti
├── 📊 siralamadata.json         # Sayısal puan verileri (5,653)
├── 📈 siralamadata2_ea.json     # Eşit ağırlık verileri (3,987)  
├── 📉 siralamadata3_sozel.json  # Sözel puan verileri (1,948)
├── 📋 requirements.txt          # Python bağımlılıkları
├── ⚙️  .env                      # Çevre değişkenleri (API key)
├── 📖 README.md                 # Bu dosya
└── 💰 ucretdata/                # Vakıf üniversite ücret verileri (Hackathon için  hazırlandı - henüz entegre edilmedi)
│   └── acibadem_universitesi_data.json
│   └── ada_kent_universitesi_data.json
│   ...
```

## 🚀 Hızlı Başlatma

### 1. Tek Komutla Başlatma (Önerilen)
```bash
./start.sh
```
Bu komut:
- ✅ Port 8080'i otomatik ayarlar
- ✅ Kullanılan portları kapatır
- ✅ Tarayıcıyı otomatik açar
- ✅ Sistem kontrolü yapar

### 2. Gelişmiş Başlatma
```bash
./run.sh
```
- İlkini tercih ediyoruz, bu ekstra.

### 3. Demo ve Test
```bash
./demo.sh
```

## ✨ Özellikler

### 🎯 **Ana Özellikler:**

1. **Puan Türüne Göre Filtreleme**: 
   - **Sayısal** (siralamadata.json) - 5,653 kayıt
   - **Eşit Ağırlık** (siralamadata2_ea.json) - 3,987 kayıt 
   - **Sözel** (siralamadata3_sozel.json) - 1,948 kayıt

2. **Akıllı Üniversite Arama**:
   - "Sabancı üniversitesindeki bölümler nelerdir?" gibi doğal dil sorguları
   - Türkçe karakterleri otomatik İngilizceye çevirme
   - Esnek arama algoritması

3. **Geçmiş Yıl Analizi**:
   - 2025/2024/2023/2022 yılları için sıralama verileri
   - Son 3 yılda bölümlerin hangi sıralama ile kapandığı

4. **Chat Geçmişi Yönetimi**:
   - ChatGPT tarzı sol panel
   - Yeni chat oluşturma
   - Geçmiş chatler son kullanımlarına göre sıralandı

5. **AI Destekli Danışmanlık**:
   - Google Gemini API entegrasyonu ✅
   - Kullanıcının sıralamasına göre özel tavsiyeler
   - Akıllı soru-cevap sistemi

### 🤖 **AI Özellikleri:**
- **Sıralama Önerileri**: Kullanıcının sıralamasına uygun bölümler
- **Popüler Üniversiteler**: En çok bölümü olan üniversitelerin listesi
- **Responsive Tasarım**: Mobil uyumlu arayüz
- **Real-time Typing**: Yazıyor göstergesi

## 📝 Kullanım Örnekleri

### 🎓 Üniversite Sorguları:
```
• "Sabancı üniversitesindeki bölümler nelerdir?"
• "Koç üniversitesi bölümleri"
• "Bilkent üniversitesinde hangi bölümler var?"
```

### 📊 Sıralama Analizi:
```
• "15000 sıralamayla hangi bölümlere girebilirim?"
• "50000 sıralamayla seçeneklerim neler?"
• "Bana öneri verir misin?"
```

### 🏫 Genel Sorular:
```
• "Hangi üniversiteler var?"
• "En iyi mühendislik üniversiteleri"
• "Tıp fakültesi olan üniversiteler"
```

## 🛠 Kurulum

### Gereksinimler:
- Python 3.7+
- Flask
- Google Generative AI
- python-dotenv

### Manuel Kurulum:
1. **Bağımlılıkları yükleyin**:
```bash
pip install -r requirements.txt
```

2. **Gemini API anahtarını ayarlayın**:
```bash
# .env dosyasını düzenleyin
GEMINI_API_KEY=your-actual-api-key
```

3. **Uygulamayı başlatın**:
```bash
python app.py
```

## 🔧 Konfigürasyon

### Port Ayarları:
- **Varsayılan Port**: 8080
- **Yedek Portlar**: 8081, 8082, 8083, 8084, 8085

### API Ayarları:
- **Model**: gemini-1.5-flash
- **API Provider**: Google Generative AI
- **Rate Limiting**: Otomatik

## 🌐 Web Arayüzü

- **Tasarım**: Modern, kullanıcı dostu
- **Style**: ChatGPT benzeri konuşma arayüzü
- **Filtreleme**: Sıralama + Puan türü paneli
- **Feedback**: Emoji'li görsel yanıtlar
- **Mobile**: Responsive tasarım


## 🔌 API Endpoints

- `GET /` - Ana sayfa
- `POST /chat` - Chat mesajı gönderme
- `GET /new_chat` - Yeni chat oluşturma
- `GET /get_chats` - Tüm chatler
- `GET /get_chat/<chat_id>` - Belirli chat
- `POST /search_departments` - Bölüm arama
- `GET /test_ai` - AI API testi

## 🚨 Sorun Giderme

### Port Sorunu:
```bash
# Port 8080 kullanımda ise:
lsof -i :8080
sudo kill -9 <PID>

# Veya start.sh otomatik halledecek
./start.sh
```

### API Sorunu:
```bash
# API test için:
python test_api.py
```

### Sistem Testi:
```bash
# Genel sistem kontrolü:
python test.py
```

## 📊 İstatistikler

- **Toplam Bölüm**: 11,588
- **Sayısal Bölümler**: 5,653
- **Eşit Ağırlık**: 3,987  
- **Sözel Bölümler**: 1,948
- **Desteklenen Yıllar**: 2022-2025
- **API Modelleri**: 41 adet

## 🎉 Demo

UniChat şu anda **http://localhost:8080** adresinde çalışıyor!

**Hemen test edin:**
```bash
./start.sh
```

---

**Geliştirici**: UniChat Ekibi  
**Teknoloji**: Flask + Google Gemini AI  
**Platform**: Web (Responsive)  
**Lisans**: MIT
