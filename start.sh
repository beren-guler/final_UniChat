#!/bin/bash

# UniChat Quick Start Script
# Bu script UniChat'i hızlıca başlatır ve tarayıcıda açar

# Renk kodları
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner göster
show_banner() {
    echo -e "${PURPLE}"
    echo "███╗   ██╗██╗ ██████╗██╗  ██╗ █████╗ ████████╗"
    echo "██╔╝   ██║██║██╔════╝██║  ██║██╔══██╗╚══██╔══╝"
    echo "██║    ██║██║██║     ███████║███████║   ██║   "
    echo "██║    ██║██║██║     ██╔══██║██╔══██║   ██║   "
    echo "███████╗██║██║╚██████╗██║  ██║██║  ██║   ██║   "
    echo "╚══════╝╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   "
    echo -e "${NC}"
    echo -e "${CYAN}🎓 Üniversite Tercihi Danışmanlık Chatbotu${NC}"
    echo -e "${BLUE}============================================${NC}"
    echo ""
}

# Port kontrolü fonksiyonu
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1 # Port kullanımda
    else
        return 0 # Port boş
    fi
}

# Kullanılan port'u öldürme fonksiyonu
kill_process_on_port() {
    local port=$1
    echo -e "${YELLOW}⚡ Port $port kullanımda olan process kapatılıyor...${NC}"
    
    local pids=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pids" ]; then
        echo -e "${YELLOW}🔍 Process ID'ler: $pids${NC}"
        for pid in $pids; do
            local process_name=$(ps -p $pid -o comm= 2>/dev/null || echo "bilinmeyen")
            echo -e "${YELLOW}💀 Kapatılıyor: $process_name (PID: $pid)${NC}"
            kill -9 $pid 2>/dev/null
        done
        
        sleep 2
        
        # Tekrar kontrol et
        if check_port $port; then
            echo -e "${GREEN}✅ Port $port başarıyla temizlendi${NC}"
            return 0
        else
            echo -e "${RED}❌ Port $port temizlenemedi${NC}"
            return 1
        fi
    else
        echo -e "${GREEN}✅ Port $port zaten boş${NC}"
        return 0
    fi
}

# Tarayıcıyı açma fonksiyonu
open_browser() {
    local url=$1
    echo -e "${CYAN}🌐 Tarayıcı açılıyor: $url${NC}"
    
    # 3 saniye bekle ki uygulama başlasın
    (sleep 3 && {
        # macOS için
        if command -v open >/dev/null 2>&1; then
            open "$url"
        # Linux için  
        elif command -v xdg-open >/dev/null 2>&1; then
            xdg-open "$url"
        # Windows için (Git Bash)
        elif command -v start >/dev/null 2>&1; then
            start "$url"
        else
            echo -e "${YELLOW}⚠️  Tarayıcı otomatik açılamadı.${NC}"
            echo -e "${YELLOW}   Manuel olarak şu adresi açın: $url${NC}"
        fi
    }) &
}

# Hızlı sistem kontrolü
quick_check() {
    echo -e "${BLUE}🔍 Sistem kontrolü...${NC}"
    
    # Python kontrolü
    if ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
        echo -e "${RED}❌ Python yüklü değil!${NC}"
        echo -e "${YELLOW}💡 Python'u yüklemek için: https://python.org${NC}"
        exit 1
    fi
    
    # app.py kontrolü
    if [ ! -f "app.py" ]; then
        echo -e "${RED}❌ app.py dosyası bulunamadı!${NC}"
        echo -e "${YELLOW}💡 Doğru dizinde olduğunuzdan emin olun${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Temel kontroller tamam${NC}"
}

# Port 8080'i ayarla ve kullan
setup_port_8080() {
    local port=8080
    
    echo -e "${BLUE}🔧 Port $port ayarlanıyor...${NC}"
    
    # Port kontrolü
    if ! check_port $port; then
        echo -e "${YELLOW}⚠️  Port $port kullanımda!${NC}"
        
        # Kullanıcıya sor
        echo -e "${CYAN}❓ Port $port'u kullanan process'i kapatmak istiyor musunuz? (y/n):${NC}"
        read -r response
        
        if [[ "$response" =~ ^[Yy]$ ]]; then
            if kill_process_on_port $port; then
                echo -e "${GREEN}✅ Port $port hazır${NC}"
            else
                echo -e "${RED}❌ Port temizlenemedi!${NC}"
                show_manual_commands $port
                exit 1
            fi
        else
            echo -e "${YELLOW}💡 Alternatif çözümler:${NC}"
            show_manual_commands $port
            exit 1
        fi
    else
        echo -e "${GREEN}✅ Port $port kullanılabilir${NC}"
    fi
    
    return $port
}

# Manuel komutları göster
show_manual_commands() {
    local port=$1
    echo ""
    echo -e "${YELLOW}📝 Manuel çözümler:${NC}"
    echo -e "${YELLOW}1. Port'u kullanan process'i görmek için:${NC}"
    echo "   lsof -i :$port"
    echo ""
    echo -e "${YELLOW}2. Process'i öldürmek için:${NC}"
    echo "   sudo kill -9 <PID>"
    echo ""
    echo -e "${YELLOW}3. Farklı port kullanmak için app.py'yi düzenleyin:${NC}"
    echo "   app.run(debug=True, port=8081)"
    echo ""
    echo -e "${YELLOW}4. AirPlay Receiver'ı kapatın (macOS):${NC}"
    echo "   System Preferences > General > AirDrop & Handoff"
}

# App.py'de port'u güncelle
update_port_in_app() {
    local port=$1
    
    if [ -f "app.py" ]; then
        echo -e "${BLUE}📝 app.py port ayarları güncelleniyor...${NC}"
        
        # Backup oluştur
        cp app.py app.py.bak
        
        # Port'u güncelle - çeşitli formatları destekle
        sed -i.tmp \
            -e "s/app\.run(debug=True)/app.run(debug=True, port=$port, host='0.0.0.0')/" \
            -e "s/app\.run(debug=True, port=[0-9]*)/app.run(debug=True, port=$port, host='0.0.0.0')/" \
            -e "s/app\.run(debug=True, port=[0-9]*, host='[^']*')/app.run(debug=True, port=$port, host='0.0.0.0')/" \
            app.py
        
        # Geçici dosyayı temizle
        rm -f app.py.tmp 2>/dev/null
        
        echo -e "${GREEN}✅ Port $port olarak ayarlandı${NC}"
    fi
}

# Bağımlılıkları hızlı yükle
install_dependencies() {
    echo -e "${BLUE}📦 Gerekli paketler kontrol ediliyor...${NC}"
    
    # Hangi python komutunu kullanacağımızı belirle
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
        PIP_CMD="pip3"
    else
        PYTHON_CMD="python"
        PIP_CMD="pip"
    fi
    
    # Gerekli paketleri sessizce yükle
    if [ -f "requirements.txt" ]; then
        $PIP_CMD install -q -r requirements.txt >/dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Bağımlılıklar hazır${NC}"
        else
            echo -e "${YELLOW}⚠️  Bazı paketler yüklenemedi, devam ediliyor...${NC}"
        fi
    fi
}

# Ana fonksiyon
main() {
    # Banner göster
    show_banner
    
    # Hızlı kontroller
    quick_check
    
    # Port ayarla
    setup_port_8080
    local port=8080
    
    # Port'u app.py'de güncelle
    update_port_in_app $port
    
    # Bağımlılıkları yükle
    install_dependencies
    
    # URL oluştur
    local url="http://localhost:$port"
    
    echo ""
    echo -e "${GREEN}🚀 UniChat başlatılıyor...${NC}"
    echo -e "${CYAN}📍 URL: $url${NC}"
    echo -e "${YELLOW}⏹️  Durdurmak için: Ctrl+C${NC}"
    echo ""
    echo -e "${PURPLE}💡 İpucu: Sayıfa yüklenmesi birkaç saniye sürebilir${NC}"
    echo ""
    
    # Tarayıcıyı aç
    open_browser "$url"
    
    # Flask uygulamasını başlat
    echo -e "${BLUE}🔥 Sunucu başlatılıyor...${NC}"
    
    # Hangi python komutunu kullanacağımızı belirle
    if command -v python3 >/dev/null 2>&1; then
        python3 app.py
    else
        python app.py
    fi
}

# Trap ile Ctrl+C yakalandığında temizlik yap
trap 'echo -e "\n${YELLOW}👋 UniChat kapatılıyor...${NC}"; exit 0' INT

# Script'i çalıştır
main "$@"
