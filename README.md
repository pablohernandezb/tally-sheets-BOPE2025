# 2025 Bolivian Presidential Election Tally Sheets Scraper

Small Python script to download Bolivian "mesa" tally-sheet images from the OEP website and save them locally for research and analysis.

## Summary

This repository contains a Python script that:
- Reads mesa codes from a CSV (downloaded from the OEP official counting site)
- Calls the OEP API for each mesa (voting table)
- Extracts the Base64 image from the response and writes a JPEG into a local output folder

Main entrypoint: [`scrape_BO2025.scrape_tally_sheets_from_csv`](scrape_BO2025.py)

## Files of interest

- [scrape_BO2025.py](scrape_BO2025.py) — main script and configuration (constants: [`scrape_BO2025.API_URL`](scrape_BO2025.py), [`scrape_BO2025.CSV_FILE_NAME`](scrape_BO2025.py), [`scrape_BO2025.MESA_CODE_COLUMN`](scrape_BO2025.py), [`scrape_BO2025.OUTPUT_DIR`](scrape_BO2025.py), [`scrape_BO2025.DELAY`](scrape_BO2025.py), [`scrape_BO2025.HEADERS`](scrape_BO2025.py))
- [EG2025_20251022_171643_4736661743343535732.csv](EG2025_20251022_171643_4736661743343535732.csv) — CSV used by default
- [EG2025_20251021_193642_3711355707836044874.csv](EG2025_20251021_193642_3711355707836044874.csv) — earlier CSV from first totalization report
- [oep_tally_sheets/](oep_tally_sheets/) — output directory (created automatically)
- [oep_tally_sheets (sample)/](oep_tally_sheets (sample)/) — sample outputs (not included here, it will be generated once you run the script)
- [Resultados Elecciones Nacionales 2025.html](Resultados Elecciones Nacionales 2025.html)
- [Resultados Elecciones Nacionales 2025_files/index-coEzeASW.css](Resultados Elecciones Nacionales 2025_files/index-coEzeASW.css)
- [response.js](response.js) — JSON response file from the API with the tally sheet image and results from a given voting table

## Requirements

- Python 3.8+
- Dependencies in the script:
  - requests
  - pandas

Install quickly:
```bash
pip install requests pandas
```

## Configuration

Open [scrape_BO2025.py](scrape_BO2025.py) and edit the constants at the top as needed:
- [`scrape_BO2025.API_URL`](scrape_BO2025.py) — API endpoint
- [`scrape_BO2025.CSV_FILE_NAME`](scrape_BO2025.py) — CSV to read mesa codes from
- [`scrape_BO2025.MESA_CODE_COLUMN`](scrape_BO2025.py) — CSV column name with mesa codes
- [`scrape_BO2025.OUTPUT_DIR`](scrape_BO2025.py) — where images will be written
- [`scrape_BO2025.DELAY`](scrape_BO2025.py) — delay between requests to avoid rate limits
- [`scrape_BO2025.HEADERS`](scrape_BO2025.py) — headers used for the POST request

The script expects the CSV to contain numeric mesa codes reachable by `int(code)`. See the implementation of [`scrape_BO2025.scrape_tally_sheets_from_csv`](scrape_BO2025.py) for details.

## Usage

Run from the repository root:

```bash
python scrape_BO2025.py
```

Typical output:
- The script reports how many total mesa codes were found and how many will be downloaded.
- Images are saved as `mesa_<CodigoMesa>.jpg` into the folder specified by [`scrape_BO2025.OUTPUT_DIR`](scrape_BO2025.py).

## Behavior & Edge cases

- The script skips already-downloaded files by scanning files named `mesa_*.jpg` in the output folder.
- If the API response lacks the expected Base64 image at `adjunto[0].valor`, the script logs a warning and moves on.
- Network errors and HTTP errors are caught and logged; inspect console output for details.

## Troubleshooting

- CSV not found: verify [`scrape_BO2025.CSV_FILE_NAME`](scrape_BO2025.py) points to an existing file (example: [EG2025_20251022_171643_4736661743343535732.csv](EG2025_20251022_171643_4736661743343535732.csv)).
- Permission errors writing files: ensure you have write access to [`scrape_BO2025.OUTPUT_DIR`](scrape_BO2025.py) or change it.
- Rate-limiting: increase [`scrape_BO2025.DELAY`](scrape_BO2025.py).

## Notes

- This repo intentionally stores outputs in [oep_tally_sheets/](oep_tally_sheets/) (ignored via [.gitignore](.gitignore)).
- Review [response.js](response.js) and [Resultados Elecciones Nacionales 2025.html](Resultados Elecciones Nacionales 2025.html) if you need to adapt parsing for different response shapes.