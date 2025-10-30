import time
import pandas as pd
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ===== CONFIG =====
IMAGE_PATH = r"C:\Users\ADMIN\Desktop\automation\Screenshot 2024-12-03 105623.png"
EXCEL_PATH = "Dasara camp contact.xlsx"
COUNTRY_CODE = "91"  # India

# ===== LOAD CONTACTS =====
df = pd.read_excel(EXCEL_PATH, dtype={"phone number": str})
# print("Columns in Excel:", df.columns.tolist())

df["phone number"] = df["phone number"].str.replace(r'\D', '', regex=True)
df = df[df["phone number"].str.len() >= 10]

# ===== SELENIUM SETUP =====
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://web.whatsapp.com/")
input("📌 Scan the QR code and press Enter here...")

wait = WebDriverWait(driver, 30)

for index, row in df.iterrows():
    phone_number = row["phone number"]

    if not phone_number.startswith(COUNTRY_CODE):
        phone_number = COUNTRY_CODE + phone_number

    print(f"📲 Sending image to {phone_number}...")

    try:
        # Open chat
        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&app_absent=0")
        time.sleep(5)  # let chat load

        # Click attach button
        attach_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='Attach']")))
        attach_btn.click()
        time.sleep(1)

        # Click Photos & Videos icon
        photo_btn = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='file']/preceding::div[@role='button'][1]")  # first icon before input
        ))
        photo_btn.click()
        time.sleep(1)  # wait for Windows dialog

        # Type file path in the dialog
        pyautogui.write(IMAGE_PATH)
        time.sleep(1)
        pyautogui.press("enter")

        # Wait for preview
        wait.until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src,'blob:')]")))

        # Click send button
        send_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send']")))
        send_btn.click()

        print(f"✅ Image sent to {phone_number}")
        time.sleep(3)

    except Exception as e:
        print(f"❌ Failed for {phone_number}: {e}")
        continue

driver.quit()
print("🎉 All done!")
