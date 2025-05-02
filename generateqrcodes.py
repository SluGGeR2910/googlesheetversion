import qrcode
import pandas as pd
import os

# 1. Load Google Sheet data
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsGwDENzRRXUGVc3G0u2keq4epiVDbXL7m4IcTNzp8qg7YKxVbuHlGHe5xxoi5ZQ/pub?gid=1140504492&single=true&output=csv"
df = pd.read_csv(SHEET_URL)

# 2. Create 'qrcodes' folder if not exists
os.makedirs("qrcodes", exist_ok=True)

# 3. Base URL of your Render app
BASE_URL = "https://slugtries.onrender.com?id="

# 4. Loop through each asset and generate QR
for asset_id in df['Asset ID']:
    asset_id_str = str(asset_id).strip()  # Clean asset ID

    # Skip if asset ID is empty
    if not asset_id_str:
        continue

    full_url = f"{BASE_URL}{asset_id_str}"

    # Generate QR
    qr = qrcode.make(full_url)

    # Save QR image
    qr.save(f"qrcodes/{asset_id_str}.png")

print("QR codes generated successfully in 'qrcodes' folder!")
