# Importing all required libraries
import pandas as pd
import pywhatkit as kit
import time

# Read the Excel file
excel_file = "contacts.xlsx"  # Replace with your actual Excel filename
df = pd.read_excel(excel_file)

# Your WhatsApp group invite link
group_link = "https://chat.whatsapp.com/your_group_invite_link"  # Replace with your link
message = f"Hello! 👋\n\nThank you for registering for the free Cyber Security Workshop by Stem Avishkar Pvt. Ltd.\nJoin our WhatsApp group for updates: {group_link}"

# Loop through each phone number and send the message
for index, row in df.iterrows():
    phone_number = row['Phone']  # Assumes column name is 'Phone'
    
    try:
        # Send message via WhatsApp
        kit.sendwhatmsg_instantly(
            phone_no=phone_number,
            message=message,
            wait_time=10,  # Seconds to wait before sending the message
            tab_close=True
        )
        print(f"Message sent to {phone_number}")
        time.sleep(15)  # Wait to prevent spamming/block
    except Exception as e:
        print(f"Failed to send message to {phone_number}: {e}")
