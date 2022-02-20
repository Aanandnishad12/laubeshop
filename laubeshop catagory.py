from bs4 import BeautifulSoup
import requests, urllib
import mysql.connector
import re
# from bs4 import BeautifulSoup 
# import re
import time
# import requests
import sys
# import time
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
# import time
# import mysql.connector
# import sys
import random
def anand():
    '''
    Table Structure
    CREATE TABLE `laubeshop_categories` (
    `category` varchar(255) DEFAULT NULL,
    `sub_category` varchar(255) DEFAULT NULL,
    `sub_sub_category` varchar(255) DEFAULT NULL,
    `url` text,
    `add_url` int(1) DEFAULT '0',
    `processed` int(1) DEFAULT '0',
    `checked` int(1) DEFAULT '0'
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1

    '''

    username = "dans@fcsus.com"
    password = "Construction1#"
    data_credentials = {'login_email': username, 'login_pass': password}

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    login_url = "https://laubeshop.com/login.php?action=check_login"
    requests_session = requests.Session()
    response = requests_session.post(login_url, headers=headers, data=data_credentials)

    # print(response.content)
    html = response.text


    soup = BeautifulSoup(html, 'html.parser')
    categories = soup.find('div', class_='category-menu')

    insert_data = []

    for li in categories.find_all('li', class_='navPages-item mobile'):
        sub_categories = li.find_all('li', class_='navPage-subMenu-item')

        anch_text = li.find('a').getText()

        if sub_categories:
            for sub_li in sub_categories:
                child_sub_categories = sub_li.find_all('li', class_='navPage-childList-item')
                if child_sub_categories:
                    for child_sub_li in child_sub_categories:
                        insert_data.append({'category': anch_text,
                                            'sub_category': sub_li.find('a').getText(),
                                            'sub_sub_category':  child_sub_li.find('a').getText(),
                                            'url': child_sub_li.find('a').get('href')})
                else:
                    insert_data.append({'category': anch_text,
                                        'sub_category': sub_li.find('a').getText(),
                                        'sub_sub_category': '',
                                        'url': sub_li.find('a').get('href')})
        else:
            insert_data.append({'category': anch_text,
                                'sub_category': '',
                                'sub_sub_category': '',
                                'url': li.find('a').get('href')})

    i = 0
    rows = []

    my_db = mysql.connector.connect(
        host="localhost",
    user="root",
    password="Anishad@123",
    database="abc"
    )
    my_cursor = my_db.cursor()
    my_cursor.execute('''CREATE TABLE if not exists `laubeshop_categories` (
    `category` varchar(255) DEFAULT NULL,
    `sub_category` varchar(255) DEFAULT NULL,
    `sub_sub_category` varchar(255) DEFAULT NULL,
    `url` text,
    `add_url` int(1) DEFAULT '0',
    `processed` int(1) DEFAULT '0',
    `checked` int(1) DEFAULT '0'
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1
    ''')

    for row in insert_data:
        if i == 0:
            i += 1
            continue
        all = row['sub_category'].find('All')
        if all != -1:
            continue
        category = re.sub('\s+',' ',row['category']).replace("'","\\'").strip()
        sub_category = re.sub('\s+',' ', row['sub_category']).replace("'","\\'").strip()
        sub_sub_category = re.sub('\s+',' ', row['sub_sub_category']).replace("'","\\'").strip()
        url = row['url'].replace("'","\\'")
        processor = 0
        sql = " SELECT * FROM `laubeshop_categories` WHERE url ='"+url+"' "
        my_cursor.execute(sql)
        my_cursor.fetchall()
        if my_cursor.rowcount == 0:
            rows.append(( category, sub_category, sub_sub_category, url, processor))


    if len(rows) > 0:
        ins_sql = " INSERT INTO laubeshop_categories(category,sub_category,sub_sub_category,url,processed) VALUES ( %s, %s, %s, %s, %s) "
        my_cursor.executemany(ins_sql, rows)
        my_db.commit()
        # print(my_cursor.rowcount, "was inserted")

def mail_send(s):
    fromaddr = "anandn@fcsus.com"
    toaddr = "nishadaman4438@gmail.com"
    msg = MIMEMultipart()
    # storing the senders email address  
    msg['From'] = fromaddr
    # storing the receivers email address 
    msg['To'] = toaddr
    # storing the subject 
    msg['Subject'] = "Differences between vnp & stock(qty) "
    # string to store the body of the mail
    body = s
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'Aman@123')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def main():
    try:
        anand()
        s = "script excution is sucessfull"
        mail_send(s)
        print(s)
    except:
        s = "script excution is unsucessfull"
        print(s)

if __name__ == "__main__":
    main()    