import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Load contacts from Excel (ensure your Excel file has a column "Phone Number")
df = pd.read_excel("New Microsoft Excel Worksheet (1).xlsx")

# WhatsApp Group Invite Link and Custom Message
group_invite_link = "https://chat.whatsapp.com/GI4p7UDLRGYGbLZhhMORj5?mode=ems_copy_t"
custom_message = (
    "Join this amazing community to explore cybersecurity internships, "
    "software and web development training, real-time projects, career assistance, "
    "and job support — all in one place!"
)

# Start WebDriver
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com/")
input("✅ Scan the QR code in WhatsApp Web and press Enter to continue...")

wait = WebDriverWait(driver, 30)

def send_group_invite(phone_number):
    try:
        # Open WhatsApp chat
        driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&text={group_invite_link}")
        time.sleep(10)  # give chat time to load fully

        # Wait for chat box
        input_box = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        )

        # Press Enter to send the group link
        input_box.send_keys(Keys.ENTER)
        print(f"✅ Group link sent to {phone_number}")
        time.sleep(3)

        # Send the custom text message
        input_box = wait.until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
        )
        input_box.send_keys(custom_message)
        time.sleep(1)
        input_box.send_keys(Keys.ENTER)

        print(f"✅ Custom message sent to {phone_number}")
        time.sleep(4)

    except Exception as e:
        print(f"❌ Could not send messages to {phone_number}: {e}")

# Loop through contacts
for index, row in df.iterrows():
    phone_number = str(row["Phone Number"]).strip()
    send_group_invite(phone_number)

driver.quit()
