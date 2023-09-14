# UFO sighting tool. Pulls location, date of occurence, & details of sighting

import requests 
import math
import re
import xmltojson
import json
from bs4 import BeautifulSoup
from datetime import date
from dateutil.relativedelta import relativedelta
from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route("/")
def main():
    #TODO: SEED DATABASE HERE!!!!!
    # seed_db()
    year_month = "202309"
    return render_template("ufo-sight-template.html", json_obj=pull_data(year_month))

def calculate_pages(table_entries):
    # 100 table entries per page
    return math.ceil(table_entries / 100)

def pull_data(year_month):
    container_arr = []
    json_obj = {}
    url = "https://nuforc.org/wp-admin/admin-ajax.php?action=get_wdtable&table_id=1&wdt_var1=YearMonth&wdt_var2=" + year_month
    payload = "draw=1&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=Link&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=Occurred&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=City&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=State&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=Country&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=Shape&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=Summary&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=Reported&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=Posted&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=HasImage&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=0&length=100&search%5Bvalue%5D=&search%5Bregex%5D=false&wdtNonce=8e2f2bcb05"
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
    print(json.loads(response)["data"][0])

    table_entries = int(json.loads(response)["recordsFiltered"])
    pages = calculate_pages(table_entries)

    page_num = 1
    start_point = 100

    # Loop through each page
    while(page_num < pages):
        for row in range(len(json.loads(response)["data"])):
            # Set each data point for the row
            container_arr.append({
                "date": json.loads(response)["data"][row][1],
                "location": str(json.loads(response)["data"][row][2]) + ", " + str(json.loads(response)["data"][row][3]) + ", " + str(json.loads(response)["data"][row][4]),
                "shape": json.loads(response)["data"][row][5],
                "summary": json.loads(response)["data"][row][6] 
            })
        payload = "draw=" + str(page_num) + "&columns%5B0%5D%5Bdata%5D=0&columns%5B0%5D%5Bname%5D=Link&columns%5B0%5D%5Bsearchable%5D=true&columns%5B0%5D%5Borderable%5D=false&columns%5B0%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B0%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B1%5D%5Bdata%5D=1&columns%5B1%5D%5Bname%5D=Occurred&columns%5B1%5D%5Bsearchable%5D=true&columns%5B1%5D%5Borderable%5D=true&columns%5B1%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B1%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B2%5D%5Bdata%5D=2&columns%5B2%5D%5Bname%5D=City&columns%5B2%5D%5Bsearchable%5D=true&columns%5B2%5D%5Borderable%5D=true&columns%5B2%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B2%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B3%5D%5Bdata%5D=3&columns%5B3%5D%5Bname%5D=State&columns%5B3%5D%5Bsearchable%5D=true&columns%5B3%5D%5Borderable%5D=true&columns%5B3%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B3%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B4%5D%5Bdata%5D=4&columns%5B4%5D%5Bname%5D=Country&columns%5B4%5D%5Bsearchable%5D=true&columns%5B4%5D%5Borderable%5D=true&columns%5B4%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B4%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B5%5D%5Bdata%5D=5&columns%5B5%5D%5Bname%5D=Shape&columns%5B5%5D%5Bsearchable%5D=true&columns%5B5%5D%5Borderable%5D=true&columns%5B5%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B5%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B6%5D%5Bdata%5D=6&columns%5B6%5D%5Bname%5D=Summary&columns%5B6%5D%5Bsearchable%5D=true&columns%5B6%5D%5Borderable%5D=true&columns%5B6%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B6%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B7%5D%5Bdata%5D=7&columns%5B7%5D%5Bname%5D=Reported&columns%5B7%5D%5Bsearchable%5D=true&columns%5B7%5D%5Borderable%5D=true&columns%5B7%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B7%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B8%5D%5Bdata%5D=8&columns%5B8%5D%5Bname%5D=Posted&columns%5B8%5D%5Bsearchable%5D=true&columns%5B8%5D%5Borderable%5D=true&columns%5B8%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B8%5D%5Bsearch%5D%5Bregex%5D=false&columns%5B9%5D%5Bdata%5D=9&columns%5B9%5D%5Bname%5D=HasImage&columns%5B9%5D%5Bsearchable%5D=true&columns%5B9%5D%5Borderable%5D=true&columns%5B9%5D%5Bsearch%5D%5Bvalue%5D=&columns%5B9%5D%5Bsearch%5D%5Bregex%5D=false&order%5B0%5D%5Bcolumn%5D=1&order%5B0%5D%5Bdir%5D=desc&start=" + str(start_point) + "&length=100&search%5Bvalue%5D=&search%5Bregex%5D=false&wdtNonce=8e2f2bcb05"
        response = requests.request("POST", url, headers=headers, data=payload).text
        page_num += 1
        start_point += 100
        #container_arr.append(response)
        #create_json_obj(response)
    return container_arr
    #return create_json_obj(response["data"])
    #return response
    


def seed_db():
    print("ayooo")
def get_json_obj():
    # Get current date
    curr_date = date.today()

    # # Get date from 6 months ago
    # six_months_ago = date.today() + relativedelta(months=-6)

    # Temporary variable for looping through past 6 months
    loop_date = curr_date

    # Loop through each month within the past 6 months
    #TODO: FIGURE OUT WHY THE GET REQUEST ONLY PULLING BACK ONE PART OF TABLE
    #TODO: CHANGE RANGE FROM (1) TO (7)
    id = 0
    json_obj = {}
    keys = ["dateOfOccurence", "location", "shape", "sightDetails"]

    for i in range(2):
        formatted_date = str(loop_date.year) + str(loop_date.month).zfill(2)
        url = "https://nuforc.org/subndx/?id=e" + formatted_date

        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        for tr in soup.find_all('tr', id=re.compile(r'table_1_row')):
            cols = tr.findAll('td')
            cols = [element.text.strip() for element in cols]
            cols = [cols[1], str(cols[2])+", "+str(cols[3])+", "+cols[4], cols[5], cols[6]]
            #print(cols)
            json_obj[id] = (dict(zip(keys, cols)))
            # for col in cols:
            #     # json_obj.push(cols)
            #     print("lol")
                # print(col)
            # with open('output.json', 'w') as f:
            #     tr_json = json.loads(tr)
            #     json.dump(tr_json, f)
            id+=1
        loop_date += relativedelta(months=-1)

        
        # Serializing json
    return json.dumps(json_obj, indent=4)
 
# Writing to sample.json
# with open("sample.json", "w") as outfile:
#     outfile.write(json_object)

#     loop_date += relativedelta(months=-1)

# If month falls within last 6 months, then pull data
# URL = "https://nuforc.org/databank/"
#https://nuforc.org/subndx/?id=e202309
# page = requests.get(URL)

# soup = BeautifulSoup(page.content, "html.parser")


# print(str(curr_year) + str(curr_month).zfill(2))

