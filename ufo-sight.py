# UFO sighting tool. Pulls location, date of occurence, & details of sighting
import requests 
import math
import re
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__, template_folder='templates')

@app.route("/")

# Main method. Renders HTML template with data pulled from UFO service.
def main():
    # Format yyyymm required by UFO datatables for pulling data
    year_month = str(datetime.now().year) + str(datetime.now().month).zfill(2)
    return render_template("ufo-sight-template.html", json_obj=pull_data(year_month))

# Calculate number of pages per month. Each page contains a maximum of 100 rows. 
def calculate_pages(table_entries):
    # Round up to ensure all data is accounted for
    return math.ceil(table_entries / 100)

# Pull data from UFO sighting website
def pull_data(year_month):
    container_arr = []
    loop_date = date.today()

    # Get URL Content
    r = requests.get("https://nuforc.org/subndx/?id=e" + year_month)

    # Parse HTML into BeautifulSoup object
    soup = BeautifulSoup(r.content, 'html.parser')

    # Retrieve nonce value
    nonce_tag = soup.find("input", { "id" : "wdtNonceFrontendEdit_1" })
    nonce = nonce_tag["value"]

    # Loop 7 times. Once for this month and 6 more for the past 6 months.
    for i in range(7):
        # Build the required HTTP request
        url = "https://nuforc.org/wp-admin/admin-ajax.php?action=get_wdtable&table_id=1&wdt_var1=YearMonth&wdt_var2=" + year_month
        payload = "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=Link&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=Occurred&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=City&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=State&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=Country&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=Shape&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=Summary&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=Reported&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=Posted&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=HasImage&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=0&length=100&search%5Bvalue%5D=&search%5Bregex%5D=false&wdtNonce=" + nonce
        headers = {
        'authority': 'nuforc.org',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': '_gid=GA1.2.585480384.1694407356; __stripe_mid=0b9cab2b-4959-478d-85e3-bd7d0d46ee44213e4a; _ga_HMLE0ZQPWX=GS1.1.1694635452.12.1.1694642262.0.0.0; _ga=GA1.2.2087832627.1694313774; _gat_gtag_UA_266387243_1=1',
        'origin': 'https://nuforc.org',
        'referer': 'https://nuforc.org/subndx/?id=' + year_month,
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("POST", url, headers=headers, data=payload).text

        # Attain number of entries for the month's table
        table_entries = int(json.loads(response)["recordsFiltered"])
        # Calculate number of pages within month's table
        pages = calculate_pages(table_entries)

        # Initialize page number & starting point
        page_num = 1
        start_point = 0

        # Loop through each month's pages
        while(page_num <= pages):
            # Loop through individual rows of each page
            for row in range(len(json.loads(response)["data"])):
                six_months_ago = datetime.now() + relativedelta(months=-6)
                # Construct JSON object for each row *if* the sighting has happened within the past 6 months only
                if six_months_ago <= datetime.strptime(json.loads(response)["data"][row][1], '%m/%d/%Y %H:%M') <= datetime.now():
                    container_arr.append({
                        "occurred": json.loads(response)["data"][row][1],
                        "location": str(json.loads(response)["data"][row][2]) + ", " + str(json.loads(response)["data"][row][3]) + ", " + str(json.loads(response)["data"][row][4]),
                        "shape": json.loads(response)["data"][row][5],
                        "summary": json.loads(response)["data"][row][6] 
                    })
            # Start point increments by 100 for each month's page
            start_point += 100
            # Update HTTP request
            payload = "draw=" + str(page_num) + "&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=Link&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=Occurred&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=City&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=State&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=Country&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=Shape&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=Summary&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=Reported&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=Posted&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=HasImage&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=" + str(start_point) + "&length=100&search%5Bvalue%5D=&search%5Bregex%5D=false&wdtNonce=" + nonce
            response = requests.request("POST", url, headers=headers, data=payload).text
            page_num += 1
        # Subtract a month
        loop_date -= relativedelta(months=1)
        year_month = str(loop_date.year) + str(loop_date.month).zfill(2)
        headers["referer"] = 'https://nuforc.org/subndx/?id=' + year_month
        url = "https://nuforc.org/wp-admin/admin-ajax.php?action=get_wdtable&table_id=1&wdt_var1=YearMonth&wdt_var2=" + year_month
    return json.dumps(container_arr, indent=4)