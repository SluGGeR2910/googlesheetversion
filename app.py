import pandas as pd
import qrcode
from io import BytesIO
from fastapi.responses import StreamingResponse

# Initialize FastAPI
app = FastAPI()

# Load the Excel file
df = pd.read_excel('fixedassets.xlsx')

# Endpoint to generate asset details (with password protection)
@app.get("/asset/{asset_id}")
async def get_asset(asset_id: int, password: str):
    if password != "cbcmc":
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Fetch asset details from the Excel file
    asset = df[df['Asset_ID'] == asset_id]
    if asset.empty:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    return asset.to_dict(orient="records")[0]

# Endpoint to generate QR for a given asset_id
@app.get("/generate_qr/{asset_id}")
async def generate_qr(asset_id: int):
    asset = df[df['Asset_ID'] == asset_id]
    if asset.empty:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Create QR code that links to the asset details
    asset_url = f"http://localhost:8000/asset/{asset_id}?password=your_secure_password"
    qr = qrcode.make(asset_url)

    # Save QR to a byte stream
    byte_io = BytesIO()
    qr.save(byte_io, 'PNG')
    byte_io.seek(0)

    return StreamingResponse(byte_io, media_type="image/png")
