from ticker.scrip_names import SCRIP_NAMES
from ticker import ticker_data as td
from ticker import update_database as ud

scanned_stocks = 0
total_stocks = len(SCRIP_NAMES)

print(f"[INFO] Starting stock scanner...Total stocks to scan: {total_stocks}")

scanner_output = []

for scrip in SCRIP_NAMES:
    
    scanned_stocks += 1
    stock_analysis = []

    print(f"[INFO] Scanning {SCRIP_NAMES.get(scrip)}...")
    
    try:    
        scrip_data = td.get_scrip_data(scrip)
        ud.update_local_database(scrip, scrip_data)

    except IndexError as i:
        print(f"[ERROR] Unable to fetch data for {scrip}. Skipping...")
        print(i)
    except TypeError as t:
        print(f"[Error] Some error occurred while fetching data for {scrip}. Skipping...")
        print(t)

    print(f"[SUCCESS] Scanned {SCRIP_NAMES.get(scrip)}, {total_stocks - scanned_stocks} remaining.")

