import time
import pandas as pd
import urllib.parse
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load and clean Excel file
df = pd.read_excel("testImage.xlsx", dtype={"phone number": str})
df["phone number"] = df["phone number"].str.replace(r'\D', '', regex=True)
df = df[df["phone number"].str.len() >= 10]

# Path to your PDF
pdf_path = os.path.abspath("Camp- Dasara.pdf")   # change filename here

# Launch WebDriver
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
input("[ok] Scan QR code in WhatsApp Web and press Enter to continue...")

wait = WebDriverWait(driver, 20)

for index, row in df.iterrows():
    phone_number = row["phone number"]

    if not phone_number.startswith("91"):
        phone_number = "91" + phone_number

    print(f"📲 Sending PDF to {phone_number}...")

    try:
        # Open chat
        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
        time.sleep(10)

        # Click attachment button (📎)
        attach_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@title='Attach']")))
        attach_btn.click()
        time.sleep(2)

        # Select document upload option
        doc_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@accept='*']")))
        doc_btn.send_keys(pdf_path)  # Upload PDF
        time.sleep(3)

        # Click send button
        send_btn = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-icon='send']")))
        send_btn.click()

        print(f"✅ PDF sent to {phone_number}")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Failed to send to {phone_number}: {e}")
        continue

driver.quit()
print("🎉 All PDFs sent.")
