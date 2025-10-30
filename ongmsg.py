import time
import pandas as pd
import urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load and clean Excel file
df = pd.read_excel("Camp.xlsx", dtype={"phone number": str})
df["phone number"] = df["phone number"].str.replace(r'\D', '', regex=True)
df = df[df["phone number"].str.len() >= 10]

# Your message with bold text and clickable links
message = """🌟 Reminder! 🌟
Dasara Kids Tech Camp at STEM Avishkar, Mysuru 🚀

🔹 Juniors: Basic Electronics & Fun Activities
🔹 Seniors: Electronics, Avishkar Kit & 3D Printing

📲 Enroll Now: +91 90360 41555

✨ Registrations started – Limited seats, book soon!"""

# Encode message for WhatsApp URL
encoded_message = urllib.parse.quote(message)

# Launch WebDriver
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
input("[ok] Scan QR code in WhatsApp Web and press Enter to continue...")

wait = WebDriverWait(driver, 20)

for index, row in df.iterrows():
    phone_number = row["phone number"]

    if not phone_number.startswith("91"):
        phone_number = "91" + phone_number

    print(f"📲 Sending message to {phone_number}...")

    try:
        # Open chat with pre-filled message
        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text={encoded_message}")
        time.sleep(10)

        # Wait for input box and send the message
        msg_box = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")))
        msg_box.send_keys(Keys.ENTER)

        print(f"✅ Message sent to {phone_number}")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Failed to send to {phone_number}: {e}")
        continue

driver.quit()
print("🎉 All messages sent.")
