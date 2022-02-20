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

    my_db = mysql.connector.connect(
        host="localhost",
    user="root",
    password="Anishad@123",
    database="abc"
    )
    my_cursor = my_db.cursor()
    my_cursor.execute("""CREATE TABLE if not exists `laubeshop_products_url` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `category` varchar(255) DEFAULT NULL,
    `sub_category` varchar(255) DEFAULT NULL,
    `product_name` text,
    `url` text,
    `processed` int(11) DEFAULT '0',
    KEY `id` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8""")
    # my_cursor.execute("ALTER TABLE andi.`laubeshop_products_url` CONVERT TO CHARACTER SET utf8")
    def checkIfDuplicates_1(listOfElems, value):
        for list in listOfElems:
            if list['url'] == value:
                return True


    def get_content_from_url(url):
        li = ''
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        resp = requests_session.post(url, headers=headers)
        p_html = resp.text
        p_soup = BeautifulSoup(p_html, 'html.parser')
        main = p_soup.find('main', id='product-listing-container')
        # print(main)
        return main

    def get_products_from_html(html, data, p_data):
        for li in html:
            pro_tag = li.find( class_='card-title')
            result = checkIfDuplicates_1(p_data, pro_tag.find('a').get('href'))
            if result is None:
                p_data.append({'category': data[0],
                        'sub_category': data[1],
                        'sub_sub_category': data[2],
                        'product_name': pro_tag.find('a').getText(),
                        'url': pro_tag.find('a').get('href')})
        # print(p_data)
        return p_data

    def start_process_toGet_products(cate_data, get_product_lists, pagination_url=None):
        # if cate_data[3] == 'https://laubeshop.com/clipper-kits-groomer-vet/':
            # s =4
        if pagination_url is None:
            html_main_tag_content = get_content_from_url(cate_data[3])
        else:
            html_main_tag_content = get_content_from_url(pagination_url)

        pagination_html = html_main_tag_content.find(class_='pagination bottom')
        if pagination_html is not None:
            pagination_next_page_html = pagination_html.find(class_='pagination-item pagination-item--next')

        ul = html_main_tag_content.find('ul', class_='productGrid visible')

        if ul is not None:
            li = ul.find_all('li', class_='product')
            get_products_from_html(li, cate_data, get_product_lists)

            if pagination_next_page_html is not None:
                page_url = pagination_next_page_html.find('a').get('href')
                start_process_toGet_products(cate_data, get_product_lists, page_url)


    sql = " SELECT * FROM `laubeshop_categories` "
    my_cursor.execute(sql)
    my_result = my_cursor.fetchall()
    get_product_lists = []

    for cate_data in my_result:
        start_process_toGet_products(cate_data, get_product_lists)


    rows = []

    for row in get_product_lists:
        category = re.sub('\s+','',row['category']).replace("'","\\'")
        # print(category)
        sub_category = re.sub('\s+','', row['sub_category']).replace("'","\\'")
        # print(sub_category)
        sub_sub_category = re.sub('\s+','', row['sub_sub_category']).replace("'","\\'")
        # print(sub_sub_category)
        product_name = row['product_name'].replace("'","\\'")
        # print(product_name)
        url = row['url'].replace("'", "\\'")
        # print(url)
        processor = 0
        sql = " SELECT * FROM `laubeshop_products_url` WHERE url ='"+url+"' "
        my_cursor.execute(sql)
        my_cursor.fetchall()
        if my_cursor.rowcount == 0:
            rows.append(( category, sub_category,  product_name, url, 0))


    if len(rows) > 0:
        # print(rows)
        ins_sql = " INSERT INTO laubeshop_products_url ( category, sub_category, product_name, url, processed) VALUES ( %s, %s, %s, %s, %s) "
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