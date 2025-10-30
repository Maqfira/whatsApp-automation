
import time
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

# Path to the image you want to send
IMAGE_PATH = r"C:\Users\ADMIN\Desktop\automation\Screenshot 2024-12-03 105623.png"  # Update this path

# Validate image path
if not os.path.exists(IMAGE_PATH):
    print(f"❌ Error: Image file at {IMAGE_PATH} does not exist.")
    exit()

# Load and clean Excel file
try:
    df = pd.read_excel("testImage.xlsx", dtype={"phone number": str})
    df["phone number"] = df["phone number"].str.replace(r'\D', '', regex=True)
    df = df[df["phone number"].str.len() == 10]  # Ensure exactly 10 digits for Indian numbers
    df["phone number"] = df["phone number"].apply(lambda x: "91" + x if not x.startswith("91") else x)
except FileNotFoundError:
    print("❌ Error: Excel file 'testImage.xlsx' not found.")
    exit()
except Exception as e:
    print(f"❌ Error reading Excel file: {e}")
    exit()

# Set up Chrome WebDriver with options
options = webdriver.ChromeOptions()
# Update with your Chrome profile path or remove to start fresh session
options.add_argument("--user-data-dir=C:/Users/ADMIN/AppData/Local/Google/Chrome/User Data/WhatsAppProfile")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-notifications")  # Disable notifications to avoid GCM errors
options.add_argument("--disable-extensions")  # Disable extensions for stability

try:
    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com/")
    print("✅ Please scan the QR code in WhatsApp Web...")
    input("✅ Press Enter after scanning the QR code to continue...")

    wait = WebDriverWait(driver, 60)

    for index, row in df.iterrows():
        phone_number = row["phone number"]
        print(f"� kjer4📲 Processing {phone_number}...")

        try:
            # Open chat with phone number
            driver.get(f"https://web.whatsapp.com/send?phone={phone_number}&app_absent=0")
            print("   🔍 Waiting for chat to load...")

            # Wait for message input box or check for invalid number
            try:
                wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='10']"))
                )
                print("   ✅ Chat loaded successfully.")
            except TimeoutException:
                # Check if invalid number message appears
                try:
                    invalid_msg = driver.find_element(By.XPATH, "//div[contains(text(), 'Phone number shared via url is invalid')]")
                    print(f"❌ Invalid phone number: {phone_number}")
                    continue
                except NoSuchElementException:
                    print(f"❌ Chat failed to load for {phone_number}, but no invalid number message found.")
                    continue

            # Attach image
            print("   🔍 Clicking attachment button...")
            attach_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[@title='Attach' or @aria-label='Attach']"))
            )
            attach_btn.click()

            # Wait for file input and send image path
            print("   🔍 Uploading image...")
            img_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
            )
            img_input.send_keys(IMAGE_PATH)

            # Wait for image preview and send
            print("   🔍 Waiting for send button...")
            send_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[@data-icon='send' or @aria-label='Send']"))
            )
            send_btn.click()
            print(f"✅ Brochure sent to {phone_number}")
            time.sleep(5)  # Avoid rate limiting

        except TimeoutException as e:
            print(f"❌ Timeout error for {phone_number}: {e}")
            continue
        except NoSuchElementException as e:
            print(f"❌ Element not found for {phone_number}: {e}")
            continue
        except Exception as e:
            print(f"❌ Unexpected error for {phone_number}: {e}")
            continue

except WebDriverException as e:
    print(f"❌ WebDriver error: {e}")
except Exception as e:
    print(f"❌ Error during WhatsApp Web setup: {e}")
finally:
    try:
        driver.quit()
    except:
        pass
    print("🎉 Script execution completed.")
