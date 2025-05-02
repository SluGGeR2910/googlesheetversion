import streamlit as st
import pandas as pd
import requests
from io import StringIO
import qrcode
from io import BytesIO

# --- Login Part ---
username = st.text_input('Username')
password = st.text_input('Password', type="password")

if username == 'Slugger' and password == 'mnco':
    st.success("Login successful! Redirecting...")

    # --- Load Google Sheet Data ---
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTsGwDENzRRXUGVc3G0u2keq4epiVDbXL7m4IcTNzp8qg7YKxVbuHlGHe5xxoi5ZQ/pub?gid=1140504492&single=true&output=csv"

    try:
        response = requests.get(sheet_url)
        response.raise_for_status()
        data = response.content.decode("utf-8")
        
        df = pd.read_csv(StringIO(data))
        df.columns = df.columns.str.strip().str.lower()  # Clean column names
        
        # Safe handle for asset ID
        query_params = st.query_params
        asset_id = query_params.get('id', None)

        if asset_id:
            if isinstance(asset_id, list):
                asset_id = asset_id[0]

            asset_id = str(asset_id).strip()  # Always string compare

            # Identify the correct column name
            possible_cols = ['asset_id', 'asset id']
            for col in possible_cols:
                if col in df.columns:
                    asset_col = col
                    break
            else:
                st.error("No suitable 'Asset ID' column found in sheet.")
                st.stop()

            # Very important: convert both sides to string & strip
            df[asset_col] = df[asset_col].astype(str).str.strip()

            asset_data = df[df[asset_col] == asset_id]

            if not asset_data.empty:
                st.success(f"Details for Asset ID: {asset_id}")
                st.table(asset_data)
            else:
                st.error("No data found for this Asset ID. Please check again.")

        else:
            st.info("Please scan a QR code to view asset details.")

    except Exception as e:
        st.error(f"Error fetching or processing data: {e}")

else:
    st.error("Invalid username or password. Try again.")
