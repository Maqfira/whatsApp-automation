import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# Load and clean Excel file
df = pd.read_excel("Cyber security.xlsx", dtype={"phone number": str})
df["phone number"] = df["phone number"].str.replace(r'\D', '', regex=True)
df = df[df["phone number"].str.len() >= 10]

# WhatsApp-friendly message with pseudo-buttons
message = """🚨 STEM Avishkar – Cyber Security Training + Internship 🚨

💻 Learn from industry experts
🛠 Work on real projects
📜 Earn a certification & boost your career

🔥 Limited seats – Don’t miss out! 🔥

Are you interested?
[ ✅ Yes – I want to join ]
[ ❌ No – Not right now ]
"""

# Launch WebDriver
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
input("✅ Scan QR code in WhatsApp Web and press Enter to continue...")

wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

for index, row in df.iterrows():
    phone_number = row["phone number"]

    if not phone_number.startswith("91"):
        phone_number = "91" + phone_number

    print(f"📲 Sending message to {phone_number}...")

    try:
        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text&app_absent=0")
        time.sleep(10)

        # Wait for message input box
        msg_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, "//div[@contenteditable='true'][@data-tab='10']")
        ))

        # Send message line-by-line
        msg_box.click()
        for line in message.split("\n"):
            actions.send_keys(line)
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT)  # New line
        actions.send_keys(Keys.ENTER)  # Send message
        actions.perform()
        actions.reset_actions()

        print(f"✅ Message sent to {phone_number}")
        time.sleep(5)

    except Exception as e:
        print(f"❌ Failed to send to {phone_number}: {e}")
        continue

driver.quit()
print("🎉 All messages sent.")
