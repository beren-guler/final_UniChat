# 🚀 UniChat Kurulum Rehberi

## Hızlı Kurulum (5 dakika)

### 1. Repository'yi klonlayın
```bash
git clone https://github.com/beren-guler/final_UniChat.git
cd final_UniChat
```

### 2. API anahtarını ayarlayın
```bash
# .env dosyası oluşturun
cp .env.example .env

# .env dosyasını düzenleyin
nano .env  # veya herhangi bir text editor
```

**.env dosyasında değiştirin:**
```env
GEMINI_API_KEY=buraya-gerçek-api-anahtarınızı-yazın
```

### 3. Uygulamayı başlatın
```bash
chmod +x start.sh
./start.sh
```

**Bu kadar!** 🎉 Tarayıcı otomatik açılacak.

---

## 🔑 Gemini API Anahtarı Alma

1. [Google AI Studio](https://aistudio.google.com/) adresine gidin
2. Google hesabınızla giriş yapın
3. "Get API Key" butonuna tıklayın
4. "Create API Key" seçin
5. Anahtarı kopyalayın ve `.env` dosyasına yapıştırın

**Not:** API ücretsizdir ve günlük kota limiti vardır.

---

## 🛠 Manuel Kurulum

### Gereksinimler:
- Python 3.7+
- pip
- İnternet bağlantısı

### Adımlar:
```bash
# 1. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 2. .env dosyasını oluşturun
cp .env.example .env
# API anahtarını .env dosyasına ekleyin

# 3. Uygulamayı başlatın
python app.py
```

### URL: http://localhost:8080

---

## 🎯 Başlatma Seçenekleri

| Komut | Açıklama | Önerilen |
|-------|----------|----------|
| `./start.sh` | Hızlı başlatma + tarayıcı açma | ✅ Evet |
| `./run.sh` | Gelişmiş başlatma + sanal ortam | 🔧 Geliştiriciler için |
| `./demo.sh` | Demo + test rehberi | 🎮 Test için |
| `python app.py` | Manuel başlatma | ⚙️ İleri seviye |

---

## 📱 Kullanım

### 1. Filtreleme
- **Sıralama:** 2025 YKS sıralamanızı girin
- **Puan Türü:** Sayısal/Eşit Ağırlık/Sözel seçin

### 2. Örnek Sorular
```
• "Sabancı üniversitesindeki bölümler nelerdir?"
• "15000 sıralamayla hangi bölümlere girebilirim?"
• "Bana öneri verir misin?"
• "Hangi üniversiteler var?"
```

### 3. Chat Özellikleri
- 💬 ChatGPT tarzı arayüz
- 📝 Chat geçmişi
- 🤖 AI destekli yanıtlar
- 📱 Mobil uyumlu

---

## 🚨 Sorun Giderme

### Port Sorunu:
```bash
# Port 8080 kullanımda ise
./start.sh  # Otomatik çözecek

# Manuel çözüm:
lsof -i :8080
sudo kill -9 <PID>
```

### API Sorunu:
```bash
# API test
python test_api.py

# Sistem test
python test.py
```

### Bağımlılık Sorunu:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📊 Özellikler

- ✅ **11,588 bölüm verisi**
- ✅ **3 puan türü** (Sayısal, EA, Sözel)
- ✅ **2022-2025 sıralama analizi**
- ✅ **AI destekli danışmanlık**
- ✅ **Türkçe karakter desteği**
- ✅ **Responsive tasarım**

---

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun: `git checkout -b feature/amazing-feature`
3. Commit edin: `git commit -m 'Add amazing feature'`
4. Push edin: `git push origin feature/amazing-feature`
5. Pull Request açın

---

## 📞 Destek

**Sorun mu yaşıyorsunuz?**
- GitHub Issues açın
- README.md'yi okuyun
- `./demo.sh` ile test edin

**İletişim:**
- GitHub: [@beren-guler](https://github.com/beren-guler)
- Repository: [final_UniChat](https://github.com/beren-guler/final_UniChat)
