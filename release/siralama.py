from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
baseurl = "https://yokatlas.yok.gov.tr/tercih-sihirbazi-t4-tablo.php"
listtype = "say" # say/söz/ea
finalurl = f'{baseurl}?p={listtype}'
driver.get(finalurl)

rows_data = []
pageamount = 114 # manually: say: 114

for i in range(pageamount):

    time.sleep(3)
    tbodies = driver.find_elements(By.XPATH, '//*[@id="mydata"]/tbody')

    for tbody in tbodies:
        rows = tbody.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            cell_texts = [cell.text.strip() for cell in cells]

            if len(cell_texts[1]) > 1:
                universite = cell_texts[1].replace("  ", "").split("\n")[0]
                bolum = cell_texts[2].replace("\n\nListeme Ekle", "").replace("   \n", " ")
                siralama = cell_texts[3].replace("\n", "/")
                puan = cell_texts[4].replace("\n", "/")
                row_json = {
                    "universite": universite,
                    "bolum": bolum,
                    "siralama": siralama,
                    "puan": puan,
                }

                rows_data.append(row_json)

    wait = WebDriverWait(driver, 10)
    sonraki_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//a[contains(text(), "Sonraki")]'))
    )
    sonraki_button.click()

    print(f'{i + 1}: {len(rows)} kadar entry listeye eklendi.')
    
jsondatafinal = json.dumps(rows_data, ensure_ascii=False, indent=2)
print(jsondatafinal)
fname = f'siralamadata_{listtype}.json'
with open(fname, "w") as f:
  f.write(jsondatafinal)

driver.quit()