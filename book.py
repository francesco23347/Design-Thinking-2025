from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import csv
import os

# ตั้งค่า Chrome
chrome_options = Options()
# chrome_options.add_argument("--headless")  # เปิดใช้ถ้าไม่ต้องการให้ browser แสดงผล

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    url = "https://easytimetable.pro/education-timetable-generator/"
    driver.get(url)
    time.sleep(3)

    # ดึงเฉพาะ Paragraph
    paragraphs = driver.find_elements(By.TAG_NAME, "p")

    data = []

    for p in paragraphs:
        text = p.text.strip()
        if text != "":
            data.append([text])

    # บันทึกลง Desktop (Windows)
    file_path = "easytimetable_paragraph_only.csv"

    with open(file_path, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Paragraph_Content"])
        writer.writerows(data)

    print("บันทึกสำเร็จที่:", os.path.abspath(file_path))

finally:
    driver.quit()
