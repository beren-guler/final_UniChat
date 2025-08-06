#!/bin/bash

# UniChat Demo Script
# Uygulamayı test etmek için çeşitli örnekler

echo "🎯 UniChat Demo ve Test Rehberi"
echo "==============================="
echo ""

echo "📋 Mevcut dosyalar:"
ls -la *.json *.py *.sh 2>/dev/null

echo ""
echo "🧪 Sistem testi yapılıyor..."
python3 test.py

echo ""
echo "🚀 Başlatma seçenekleri:"
echo ""
echo "1. Hızlı başlatma (önerilen):"
echo "   ./start.sh"
echo ""
echo "2. Gelişmiş başlatma:"
echo "   ./run.sh"
echo ""
echo "3. Manuel başlatma:"
echo "   python app.py"
echo ""

echo "💡 Demo sorular:"
echo "=================="
echo ""
echo "🎓 Üniversite arama örnekleri:"
echo "• Sabancı üniversitesindeki bölümler nelerdir?"
echo "• Koç üniversitesi bölümleri"
echo "• Bilkent üniversitesinde hangi bölümler var?"
echo "• İTÜ mühendislik bölümleri"
echo ""
echo "📊 Sıralama analizi örnekleri:"
echo "• 15000 sıralamayla hangi bölümlere girebilirim?"
echo "• 50000 sıralamayla seçeneklerim neler?"
echo "• Bana öneri verir misin?"
echo "• Hangi bölümleri tercih etmeliyim?"
echo ""
echo "🏫 Genel sorular:"
echo "• Hangi üniversiteler var?"
echo "• En iyi mühendislik üniversiteleri hangileri?"
echo "• Tıp fakültesi olan üniversiteler"
echo "• İngilizce eğitim veren bölümler"
echo ""

echo "⚙️  Puan türü seçenekleri:"
echo "1️⃣  Sayısal (Matematik-Fen)"
echo "2️⃣  Eşit Ağırlık (Mat-Türkçe)"
echo "3️⃣  Sözel (Edebiyat-Sosyal)"
echo ""

echo "🌐 URL: http://localhost:8080"
echo "📱 Mobil uyumlu arayüz"
echo "💬 ChatGPT benzeri kullanıcı deneyimi"
echo ""

read -p "Demo'yu başlatmak için Enter'a basın..." 
./start.sh
