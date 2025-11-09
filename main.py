from ticker.scrip_names import SCRIP_NAMES
from ticker import ticker_data as td
from ticker import update_database as ud

scanned_stocks = 0
total_stocks = len(SCRIP_NAMES)

scanner_output = []

for scrip in SCRIP_NAMES:
    
    scanned_stocks += 1
    stock_analysis = []

    try:    
        scrip_data = td.get_scrip_data(scrip)
        ud.update_local_database(scrip, scrip_data)

    except IndexError:
        print(f"Unable to fetch data for {scrip}. Skipping...")
        continue
    except TypeError:
        print(f"Some error occurred while fetching data for {scrip}. Skipping...")
        continue

    print(f"Scanned {SCRIP_NAMES.get(scrip)}, {total_stocks - scanned_stocks} remaining.")

