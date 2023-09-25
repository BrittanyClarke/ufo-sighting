# UFO sighting tool. Pulls location, date of occurence, & details of sighting
import requests
import traceback
import re 
import pymongo
import certifi
from pymongo import MongoClient, InsertOne
from pymongo.server_api import ServerApi
import math
import re
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from bson.json_util import dumps

app = Flask(__name__, template_folder='templates')

# Main method. Renders HTML template with data pulled from UFO service.
@app.route("/")
def main():
    # Format yyyymm required by UFO datatables for pulling data
    year_month = str(datetime.now().year) + str(datetime.now().month).zfill(2)
    export_to_mongodb(pull_data(year_month))
    return render_template("ufo-sight-template.html", json_obj=import_from_mongodb())

# Filter by country
@app.route('/location', methods=['GET'])
def filter_by_country_route():
    # Format yyyymm required by UFO datatables for pulling data
    year_month = str(datetime.now().year) + str(datetime.now().month).zfill(2)
    export_to_mongodb(pull_data(year_month))
    args = request.args
    return render_template("ufo-sight-template.html", json_obj=import_from_mongodb("location", request.args["country"]))

# Filter by date
@app.route('/date', methods=['GET'])
def filter_by_date_route():
    # Format yyyymm required by UFO datatables for pulling data
    year_month = str(datetime.now().year) + str(datetime.now().month).zfill(2)
    export_to_mongodb(pull_data(year_month))
    args = request.args
    return render_template("ufo-sight-template.html", json_obj=import_from_mongodb("date", request.args["ddmmyyyy"]))


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
                        "_id": re.findall(r'id=(\d+)', json.loads(response)["data"][row][0])[0],
                        "occurred": datetime.strptime(json.loads(response)["data"][row][1], '%m/%d/%Y %H:%M'),
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
    return container_arr

# Export data to our DB
def export_to_mongodb(ufo_json_obj):
    uri = "mongodb+srv://admin:Ch0c01ate41!@ufocluster.slqyniu.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client.UfoCluster
    collection = db.ufoSightings

    # Log any errors to log.txt file when data cannot be inserted (i.e. duplicate entries)
    with open("log.txt", "w") as log:
        try:
            collection.insert_many(ufo_json_obj, ordered=False)
        except Exception:
            traceback.print_exc(file=log)
            pass 

    # Delete sighting entries older than 6 months
    delete_old_entries(collection)

# Import data from our DB
def import_from_mongodb(filter_type="none", filter=""):
    uri = "mongodb+srv://admin:Ch0c01ate41!@ufocluster.slqyniu.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
    db = client.UfoCluster
    collection = db.ufoSightings

    # Route is "/"
    if filter_type == "none":
        return dumps(list(collection.find().sort("occurred", -1)), indent=4)

    # Route is "/location/{country}"
    if filter_type == "location":
        # Filter by country user provides. Case insensitive.
        return dumps(list(collection.find({"location": {"$regex": filter, '$options' : 'i'}}).sort("occurred", -1)), indent=4)

    # Route is "/date/{ddmmyyyy}"
    if filter_type == "date":
        # Filter by date user provides.
        dt_obj = datetime(int(filter[4:8]), int(filter[0:2]), int(filter[2:4]))
        dt_obj_next_day = dt_obj
        dt_obj_next_day += relativedelta(days=1)
        return dumps(list(collection.find({"occurred": {"$gte": dt_obj, "$lt": dt_obj_next_day}}).sort("occurred", -1)), indent=4)


# Delete entries older than 6 months
def delete_old_entries(collection):

    # Calculate date that was six months ago
    six_months_ago = datetime.now() + relativedelta(months=-6)

    # Create a query object
    query = {"occurred": {"$lt": six_months_ago}}

    # Delete all documents that match the query object
    collection.delete_many(query)