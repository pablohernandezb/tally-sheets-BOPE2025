import requests
import base64
import os
import json
import time
import pandas as pd

# --- CONFIGURATION ---

# The API endpoint for fetching a single mesa's results
API_URL = "https://computo.oep.org.bo/api/v1/resultados/mesa"

# The name of the CSV file containing all CodigoMesa values
CSV_FILE_NAME = "EG2025_20251022_171643_4736661743343535732.csv"

# The column name in the CSV that holds the codes
MESA_CODE_COLUMN = "CodigoMesa" 

OUTPUT_DIR = "oep_tally_sheets"
DELAY = 0.5 # Delay between requests (adjust if you encounter issues, e.g., to 1.0)

# Headers to mimic a browser request
HEADERS = {
    "accept": "application/json",
    "content-type": "application/json",
    # It's good practice to set a User-Agent
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# --- MAIN FUNCTION ---

def scrape_tally_sheets_from_csv():
    """Reads mesa codes from a CSV, checks for existing files, and scrapes the missing tally sheets."""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        # 1. Load all mesa codes from the CSV file
        df = pd.read_csv(CSV_FILE_NAME)
        
        if MESA_CODE_COLUMN not in df.columns:
            print(f"Error: CSV file is missing the required column: '{MESA_CODE_COLUMN}'")
            return

        # Get the list of unique mesa codes (as strings for easy comparison later)
        all_mesa_codes = [str(int(code)) for code in df[MESA_CODE_COLUMN].dropna().unique()]
        
    except FileNotFoundError:
        print(f"Error: The file '{CSV_FILE_NAME}' was not found.")
        print("Please ensure the CSV file is in the same directory as this script.")
        return
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return

    # 2. Check for existing files
    downloaded_codes = set()
    for filename in os.listdir(OUTPUT_DIR):
        if filename.startswith("mesa_") and filename.endswith(".jpg"):
            # Extract the code from the filename, e.g., "mesa_123456.jpg" -> "123456"
            code = filename.replace("mesa_", "").replace(".jpg", "")
            downloaded_codes.add(code)

    # 3. Filter the list: only keep codes that have NOT been downloaded
    mesa_codes_to_download = []
    for code in all_mesa_codes:
        if code not in downloaded_codes:
            mesa_codes_to_download.append(int(code)) # Convert back to integer for API call
    
    
    total_codes = len(all_mesa_codes)
    to_download = len(mesa_codes_to_download)
    already_downloaded = total_codes - to_download

    print(f"Found {total_codes} total mesa codes in the CSV.")
    print(f"Skipping {already_downloaded} files that already exist in '{OUTPUT_DIR}'.")
    print(f"Starting download for {to_download} missing files.")
    
    # 4. Start the download loop for the filtered list
    for i, codigo_mesa in enumerate(mesa_codes_to_download):
        
        print(f"[{i+1}/{to_download}] Processing Mesa {codigo_mesa}...", end=" ")
        
        # Prepare the POST data
        # Ensure the code is an integer type for the JSON payload, as required by the API.
        payload = json.dumps({"codigoMesa": int(codigo_mesa)})
        
        try:
            # Make the POST request
            response = requests.post(API_URL, headers=HEADERS, data=payload, timeout=10)
            response.raise_for_status() 
            
            data = response.json()
            
            # Extract the Base64 image string (path: adjunto[0].valor)
            base64_data = None
            if data.get('adjunto') and len(data['adjunto']) > 0:
                base64_data = data['adjunto'][0].get('valor')
            
            if not base64_data:
                print("⚠️ No Base64 image data found.")
                continue

            # Decode the Base64 string and save the image
            image_data = base64.b64decode(base64_data)
            file_path = os.path.join(OUTPUT_DIR, f"mesa_{codigo_mesa}.jpg")

            with open(file_path, 'wb') as f:
                f.write(image_data)

            print("✅ Saved successfully.")

        except requests.exceptions.HTTPError as e:
            print(f"❌ Request failed (HTTP Error {e.response.status_code}).")
        except requests.exceptions.RequestException:
            print(f"❌ Request failed (Connection/Timeout Error).")
        except json.JSONDecodeError:
            print("❌ Failed to decode JSON response.")
        except Exception as e:
            print(f"❌ An unexpected error occurred: {e}")
        
        # Wait to avoid overwhelming the server
        time.sleep(DELAY)

    print("\n\nScraping process finished.")

# --- EXECUTION ---
if __name__ == "__main__":
    scrape_tally_sheets_from_csv()