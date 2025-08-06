from selenium import webdriver
from selenium.webdriver.common.by import By
from google import genai
from unidecode import unidecode

example_json = '''{
  "university": {
    "name": "Sabancı Üniversitesi",
    "url": "https://www.sabanciuniv.edu/tr/lisans-programlari-burs-ve-ucretleri",
    "last_updated": "2024-2025"
  },
  "tuition_fees": {
    "academic_year": "2024-2025",
    "new_students": {
      "annual_fee": {
        "amount": 1100000,
        "currency": "TL"
      },
      "semester_fee": {
        "fall": 550000,
        "spring": 550000,
        "currency": "TL"
      }
    }
  },
  "scholarships": {
    "full_scholarships": [
      {
        "name": "Üstün Başarı Bursu",
        "coverage": "Öğrenim ücreti + 15.000 TL aylık",
        "monthly_cash": 15000,
        "condition": "YKS sınavında üstün başarı",
        "percentage": "100%"
      },
      {
        "name": "Sabancı Vakfı Bursu",
        "coverage": "Tam öğrenim ücreti + yaşam giderleri",
        "monthly_cash": 12000,
        "condition": "Sosyoekonomik koşullar + akademik başarı",
        "percentage": "100%"
      },
      {
        "name": "Milli Sporcu Bursu",
        "coverage": "Tam öğrenim ücreti",
        "condition": "Milli takım sporcusu olmak",
        "percentage": "100%"
      }
    ],
    "partial_scholarships": [
      {
        "name": "Diploma Katkı Bursu",
        "coverage": "Öğrenim ücretinde indirim",
        "percentage": "25%-75%",
        "condition": "Lise diploma notu"
      }
    ]
  },
  "dormitory_fees": {
    "academic_year": "2024-2025",
    "period": "9 months",
    "room_types": [
      {
        "type": "Tek Kişilik Oda",
        "price": 135000,
        "currency": "TL"
      },
      {
        "type": "Çift Kişilik Oda",
        "price": 90000,
        "currency": "TL"
      },
      {
        "type": "Üç Kişilik Oda",
        "price": 67500,
        "currency": "TL"
      }
    ]
  }
}
'''

def get_text_between(text, start, end):
    start_idx = text.find(start)
    end_idx = text.find(end, start_idx)
    if start_idx == -1 or end_idx == -1:
        return ""
    start_idx += len(start)
    return text[start_idx:end_idx].strip()

client = genai.Client(api_key="API_KEY")
chat = client.chats.create(model="gemini-2.0-flash")

driver = webdriver.Chrome()
driver.get("https://www.basarisiralamalari.com/ozel-universite-ogrenim-egitim-ucretleri/")

ulbody1 = driver.find_elements(By.XPATH, '//*[@id="singleContent"]/ul[1]')
ulbody2 = driver.find_elements(By.XPATH, '//*[@id="singleContent"]/ul[2]')
linklist = []
#türkiye
ulbi = ulbody1[0].find_elements(By.TAG_NAME, 'li')
for li in ulbi:
    a_tags = li.find_elements(By.TAG_NAME, 'a')
    if a_tags:
        linklist.append(a_tags[0].get_attribute('href'))
#kıbrıs
ulbi2 = ulbody2[0].find_elements(By.TAG_NAME, 'li')
for li in ulbi2:
    a_tags = li.find_elements(By.TAG_NAME, 'a')
    if a_tags:
        linklist.append(a_tags[0].get_attribute('href'))


START_TEXT = 'Eğitim Ücretleri ve Bursları 2025-2026'
END_TEXT = 'NOT: LÜTFEN TERCİH YAPMADAN ÖNCE KILAVUZU DİKKATLİCE KONTROL EDİNİZ.'
i = 0
for unilink in linklist:
    if (i > 3):
        driver.get(unilink)
        html_ = get_text_between(driver.page_source, START_TEXT, END_TEXT)

        response = chat.send_message(f'i\'ll provide you a html and i want you to parse the html and make me a structured list about university prices. please write a single message only and only. no nothing, just the response. i want the response format be like the json: {example_json}. here is the necessary html: {html_}')

        filename = unidecode(driver.find_element(By.XPATH, "//h1[@class='title']").text.replace(' Eğitim Ücretleri 2025-2026 ve Bursları', '').lower().replace(' ', '_'))
        with open(f'ucretdata/{filename}_data.json', 'w', encoding='utf-8') as file:
            file.write(response.text.replace('```json\n', '').replace('```', ''))

        print(f'ucretdata/{filename}_data.json yazıldı.')
    i += 1

driver.quit()