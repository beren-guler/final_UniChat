#!/bin/bash

# UniChat uygulamasını başlatma scripti
# Kullanım: ./run.sh

echo "🚀 UniChat Uygulaması başlatılıyor..."
echo "===================================="

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Port ayarları
DEFAULT_PORT=8080
BACKUP_PORTS=(8081 8082 8083 8084 8085)

# Port kontrolü fonksiyonu
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1 # Port kullanımda
    else
        return 0 # Port boş
    fi
}

# Portu öldür fonksiyonu
kill_port() {
    local port=$1
    echo -e "${YELLOW}⚠️  Port $port kullanımda. Kapatılıyor...${NC}"
    
    # Port'u kullanan process'i bul ve öldür
    local pids=$(lsof -ti:$port)
    if [ ! -z "$pids" ]; then
        echo "Process ID'ler: $pids"
        kill -9 $pids 2>/dev/null
        sleep 2
        
        # Tekrar kontrol et
        if check_port $port; then
            echo -e "${GREEN}✅ Port $port başarıyla kapatıldı${NC}"
            return 0
        else
            echo -e "${RED}❌ Port $port kapatılamadı${NC}"
            return 1
        fi
    fi
}

# Uygun port bul
find_available_port() {
    # Önce varsayılan portu dene
    if check_port $DEFAULT_PORT; then
        echo $DEFAULT_PORT
        return
    fi
    
    # Varsayılan port kullanımda, kapatmayı dene
    if kill_port $DEFAULT_PORT; then
        echo $DEFAULT_PORT
        return
    fi
    
    # Yedek portları dene
    for port in "${BACKUP_PORTS[@]}"; do
        if check_port $port; then
            echo $port
            return
        fi
    done
    
    # Hiçbir port bulunamadı
    echo "NONE"
}

# Tarayıcıyı açma fonksiyonu
open_browser() {
    local url=$1
    echo -e "${BLUE}🌐 Tarayıcı açılıyor: $url${NC}"
    
    # macOS için
    if command -v open >/dev/null 2>&1; then
        sleep 3 && open "$url" &
    # Linux için
    elif command -v xdg-open >/dev/null 2>&1; then
        sleep 3 && xdg-open "$url" &
    # Windows için (Git Bash)
    elif command -v start >/dev/null 2>&1; then
        sleep 3 && start "$url" &
    else
        echo -e "${YELLOW}⚠️  Tarayıcı otomatik açılamadı. Manuel olarak şu adresi açın: $url${NC}"
    fi
}

# Sanal ortam kurulumu
setup_virtual_env() {
    if [ ! -d "venv" ]; then
        echo -e "${YELLOW}📦 Sanal ortam bulunamadı. Oluşturuluyor...${NC}"
        python3 -m venv venv
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Sanal ortam oluşturulamadı!${NC}"
            exit 1
        fi
    fi

    echo -e "${BLUE}🔧 Sanal ortam aktifleştiriliyor...${NC}"
    source venv/bin/activate
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Sanal ortam aktif${NC}"
    else
        echo -e "${RED}❌ Sanal ortam aktifleştirilemedi!${NC}"
        exit 1
    fi
}

# Bağımlılık kontrolü
check_dependencies() {
    echo -e "${BLUE}📋 Gerekli paketler kontrol ediliyor...${NC}"
    
    if [ -f "requirements.txt" ]; then
        pip install -q -r requirements.txt
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Bağımlılıklar yüklendi${NC}"
        else
            echo -e "${RED}❌ Bağımlılık yükleme hatası!${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}⚠️  requirements.txt bulunamadı${NC}"
    fi
}

# Dosya kontrolü
check_files() {
    echo -e "${BLUE}📁 Gerekli dosyalar kontrol ediliyor...${NC}"
    
    missing_files=()
    required_files=("app.py" "siralamadata.json" "siralamadata2_ea.json" "siralamadata3_sozel.json")
    
    for file in "${required_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo -e "${RED}❌ Eksik dosyalar:${NC}"
        for file in "${missing_files[@]}"; do
            echo -e "${RED}  - $file${NC}"
        done
        exit 1
    else
        echo -e "${GREEN}✅ Tüm dosyalar mevcut${NC}"
    fi
}

# .env kontrolü
check_env() {
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠️  .env dosyası bulunamadı!${NC}"
        echo -e "${YELLOW}💡 AI özellikleri çalışmayabilir${NC}"
    else
        echo -e "${GREEN}✅ .env dosyası mevcut${NC}"
    fi
}

# Ana başlatma fonksiyonu
main() {
    # Sistem kontrolü
    setup_virtual_env
    check_dependencies
    check_files
    check_env
    
    # Port kontrolü ve seçimi
    echo -e "${BLUE}🔍 Uygun port aranıyor...${NC}"
    SELECTED_PORT=$(find_available_port)
    
    if [ "$SELECTED_PORT" = "NONE" ]; then
        echo -e "${RED}❌ Uygun port bulunamadı!${NC}"
        echo -e "${YELLOW}💡 Şu komutları deneyebilirsiniz:${NC}"
        echo "   sudo lsof -i :8080 (port kullanan process'i görmek için)"
        echo "   sudo kill -9 <PID> (process'i öldürmek için)"
        echo "   python app.py --port 9000 (farklı port denemek için)"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Port $SELECTED_PORT kullanılacak${NC}"
    
    # app.py dosyasında port'u güncelle
    if [ -f "app.py" ]; then
        # Port değişikliği için geçici dosya oluştur
        sed "s/app\.run(debug=True, port=[0-9]*)/app.run(debug=True, port=$SELECTED_PORT, host='0.0.0.0')/" app.py > app_temp.py
        mv app_temp.py app.py
    fi
    
    echo ""
    echo -e "${GREEN}🎉 UniChat başlatılıyor...${NC}"
    echo -e "${BLUE}📍 URL: http://localhost:$SELECTED_PORT${NC}"
    echo -e "${YELLOW}⏹️  Durdurmak için: Ctrl+C${NC}"
    echo ""
    
    # Tarayıcıyı aç
    open_browser "http://localhost:$SELECTED_PORT"
    
    # Flask uygulamasını başlat
    python app.py
}

# Script'i çalıştır
main "$@"
