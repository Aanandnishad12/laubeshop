

import re
from bs4 import BeautifulSoup
import requests, urllib
import mysql.connector
import itertools
import re
import json
import collections
import numpy as np
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def anand():
    new_prod = []
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
    my_cursor.execute("""CREATE TABLE if not exists `laubeshop_op` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `Product_Title` varchar(300) NOT NULL,
    `sku` varchar(200) NOT NULL,
    `parent_sku` varchar(200) DEFAULT NULL,
    `primary_sku` int(1) DEFAULT '1',
    `UPC` varchar(15) DEFAULT NULL,
    `EAN` varchar(12) DEFAULT NULL,
    `LMP_SKU` varchar(200) DEFAULT NULL,
    `mfg_id` varchar(30) DEFAULT NULL,
    `FF_Latency` varchar(10) DEFAULT NULL,
    `Amazon_ASIN` varchar(10) DEFAULT NULL,
    `is_change` binary(1) DEFAULT NULL,
    `notions_unit_of_sale` int(3) DEFAULT NULL,
    `previous_vnp` decimal(7,2) DEFAULT NULL,
    `fcsus_unit_of_sale` int(3) DEFAULT NULL,
    `vnp` decimal(7,2) DEFAULT NULL,
    `inward_freight` decimal(7,2) DEFAULT '0.00',
    `Product_Net_Weight_Oz` decimal(7,2) DEFAULT NULL,
    `previous_shipping_weight` decimal(7,2) DEFAULT '0.00',
    `shipping_weight` decimal(7,2) DEFAULT NULL,
    `product_introduce_date` varchar(255) DEFAULT NULL,
    `length` decimal(7,2) DEFAULT NULL,
    `width` decimal(7,2) DEFAULT NULL,
    `height` decimal(7,2) DEFAULT NULL,
    `product_discription` text,
    `price_update_override` int(1) DEFAULT '0',
    `wgt_update_override` int(1) DEFAULT '0',
    `Minimum_Advertised_Price` decimal(7,2) DEFAULT NULL,
    `frt_collect` varchar(1) DEFAULT 'N',
    `image1` varchar(500) DEFAULT NULL,
    `image2` varchar(500) DEFAULT NULL,
    `image3` varchar(500) DEFAULT NULL,
    `image4` varchar(500) DEFAULT NULL,
    `image5` varchar(500) DEFAULT NULL,
    `previous_qty_avb` int(1) DEFAULT '0',
    `qty_avb` int(1) DEFAULT '0',
    `stock` int(1) DEFAULT '0',
    `option_name` varchar(250) NOT NULL,
    `category` text,
    `sub_category` text,
    `Product_link` text,
    `discontinued` int(1) DEFAULT '0',
    `last_updated` varchar(255) DEFAULT NULL,
    `doba_categories` varchar(255) DEFAULT NULL,
    `doba_allowed` int(1) NOT NULL DEFAULT '1',
    KEY `id` (`id`)
    ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8
    """)
    # my_cursor.execute("ALTER TABLE andi.`laubeshop_op` CONVERT TO CHARACTER SET utf8")
    def check_key_exist(test_dict, key):
            if key not in test_dict:
                return False
            else:
                return True


    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext


    def get_dropdown_response(data_credential, hid2, nav_img, price):

        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        post_url = "https://laubeshop.com/remote/v1/product-attributes/" + str(hid2)
        #print(post_url)
        
        respnse = requests_session.post(post_url, headers=headers, data=data_credential)
        pd_soup = BeautifulSoup(respnse.text, 'html.parser')
        jsn_data = json.loads(respnse.text)
        price_tag = jsn_data['data']['price']['without_tax']['formatted']
        price_tag1 =price_tag.replace('$','')
        #print(price_tag1 )
    
        in_stock = jsn_data['data']['instock']
        sku_val = jsn_data['data']['sku']
        sku=('LB01'+sku_val).replace(' ','').replace('-','')
        img = jsn_data['data']['image']
        if img is not None:
            nav_imgs = jsn_data['data']['image']['data'].replace('{:size}', '500x659')
        else:
            nav_imgs = nav_img
        if price_tag1 is not None:
            price = price_tag1
        else:
            price = ''
        #print(price)
        return sku, in_stock, nav_imgs, price

    def get_price_from_size_option(html, produt_name, sku, price, nav_img, data_url, description, option_name):
        select = html.find(class_='productView-options').find_all(attrs={"class":"form-field", "data-product-attribute":"set-select"})
        select_radio_buttons = []
        #print(len(select),'++++')
        #print(select)
        for s in select:
            option=s.find_all("option")
            #print(option )
        attrarray=[]
        if len(select) == 1:
            sel1=select[0].find('select')
            option1=sel1.find_all("option")
            #print(option1)
            attributes1 =sel1.get('name')
            #print(attributes1)
            attrarray.append(attributes1)
            
        elif len(select) == 2:
            sel1=select[0].find('select')
            option1=sel1.find_all("option")
            #print(option1)
            attributes1 =sel1.get('name')
            #print(attributes1)
            attrarray.append(attributes1)
            sel2=select[1].find('select')
            option2=sel2.find_all("option")
            #print(option2)
            attributes2 =sel2.get('name')
            #print(attributes2)
            attrarray.append(attributes2)
            
        elif len(select) == 3:
            sel1=select[0].find('select')
            option1=sel1.find_all("option")
            #print(option1)
            attributes1 =sel1.get('name')
            #print(attributes1)
            attrarray.append(attributes1)
            sel2=select[1].find('select')
            option2=sel2.find_all("option")
            #print(option2)
            attributes2 =sel2.get('name')
            #print(attributes2)
            attrarray.append(attributes2)
            sel3=select[2].find('select')
            option3=sel3.find_all("option")
            #print(option3)
            attributes3 =sel3.get('name')
            #print(attributes3)
            attrarray.append(attributes3)

        else:
            select_radio_buttons = html.find(class_='productView-options').find_all(attrs={"class": "form-field", "data-product-attribute": "set-radio"})
            select_radio = html.find(class_='productView-options').find(class_='form-field').find_all('input', class_='form-radio')
            option = select_radio
            # print(option)

        hid1 = html.find(class_='productView-options').find('input', {'name': 'action'})['value']
        #print( hid1)
        hid2 = html.find(class_='productView-options').find('input', {'name': 'product_id'})['value']
        #print( hid2)
        main_select = []
        option_name = ''
        if len(select) >=1:
            for single_select in select:
                sub = []
                select = single_select.find('select')
                if select is not None:
                    for val in attrarray:
                        select_name = val 
                        #select_name=select_name.get('name')
                    #  print(select_name)
                        option = select.find_all("option")
                        
                        for opt in option:
                            #print(opt.get('value'))
                            sub.append({select_name: opt.get('value')})
                            option_name = opt.text

                    main_select.append(sub)
                    #print(main_select)
                for combination in itertools.product(*main_select):
                    option_name = ''
                    data_credential = ''
                    data_credential = {'action': hid1, 'product_id': hid2, 'qty[]': 1}
                    for each_comb in combination:
                        value = str(each_comb).find(": ''")
                        if value == -1:
                            for x in each_comb.values():
                                text = html.find('option', {'value':x}).text
                                option_name = option_name+"/"+text
                            data_credential.update(each_comb)
                    # print(data_credential)
                    sku, in_stock, nav_imgs, price = get_dropdown_response(data_credential, hid2, nav_img, price)
                    insert_or_update_product(produt_name, sku, price, nav_imgs, data_url, description, option_name, in_stock)
        elif len(select_radio_buttons) > 1:
            option_name = ''
            for single_select in select_radio_buttons:
                sub = []
                select = single_select.find_all('input', class_='form-radio')
                if select is not None:
                    # select_name = select.get('name')
                    option = select
                    for opt in option:
                        select_name = opt.get('name')
                        sub.append({select_name: opt.get('value')})
                        opt_name = single_select.find('label', {'for': str(opt.get('id'))}).text

                main_select.append(sub)


            for combination in itertools.product(*main_select):
                option_name = ''
                data_credential = ''
                data_credential = {'action': hid1, 'product_id': hid2, 'qty[]': 1}
                for each_comb in combination:
                    value = str(each_comb).find(": ''")
                    if value == -1:
                        for x in each_comb.values():
                            id = html.find('input', {'value':x}).get('id')
                            text = html.find('label',{'for': id}).text
                            option_name = option_name+"/"+text

                        data_credential.update(each_comb)
                # print(data_credential)
                sku, in_stock, nav_imgs, price = get_dropdown_response(data_credential, hid2, nav_img, price)
                insert_or_update_product(produt_name, sku, price, nav_imgs, data_url, description, option_name, in_stock)
        else:
            select_name=option[0].get('name')
            if option is not None:
                options =''
                option_name = ''
                    
            data_credential = {select_name: options, 'action': hid1, 'product_id': hid2, 'qty[]': 1}
            sku, in_stock, nav_imgs, price = get_dropdown_response(data_credential, hid2, nav_img, price)
            insert_or_update_product(produt_name, sku, price, nav_imgs, data_url, description, option_name, in_stock)
            i = 1
            for x in option:
                select_name = x.get('name')
                if len(select) == 1:
                    if i == 1:
                        i = i + 1
                        continue
                    options = x.get('value')
                    option_name = x.text
                else:
                    select_name = x.get('name')
                    options = x.get('value')
                    option_name = html.find('label', {'for': str(x.get('id'))}).text
                data_credential = {select_name: options, 'action': hid1, 'product_id': hid2, 'qty[]': 1}

                sku, in_stock, nav_imgs, price = get_dropdown_response(data_credential, hid2, nav_img, price)
                insert_or_update_product(produt_name, sku, price, nav_imgs, data_url, description, option_name, in_stock)


    def get_content_from_url(url):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
        resp = requests_session.post(url, headers=headers)
        p_html = resp.text
        p_soup = BeautifulSoup(p_html, 'html.parser')
        main = p_soup.find('div', class_='productView')
        return main


    def insert_or_update_product(produt_name, sku, price, nav_img, data_url, description, option_name, in_stock=0):
     
        if price=='' or produt_name=='':
            discontinued='1'
        else:
            discontinued='0'
        sql = " SELECT id, category, sub_category, processed FROM `laubeshop_products_url` WHERE url ='"+data_url+"'  "
        my_cursor.execute(sql)
        myresult = my_cursor.fetchall()
        # print(myresult) 
        if myresult is not None and myresult[0][3] == 0:
         
            sql = "UPDATE laubeshop_products_url SET processed = 1 WHERE id = '" + str(myresult[0][0]) + "'"
            my_cursor.execute(sql)
            my_db.commit()
        values = (produt_name, sku, price, nav_img, myresult[0][1], myresult[0][2], data_url, description.replace("'", "\\'"), option_name, in_stock,discontinued)

        sql = " SELECT * FROM `laubeshop_op` WHERE sku ='" + sku + "' "
        my_cursor.execute(sql)
        bosspetedge_op_res = my_cursor.fetchall()

        if my_cursor.rowcount == 0:
            new_prod.append(sku)
            # print(values) 
         
            sql = "INSERT INTO laubeshop_op ( Product_Title, sku, vnp,image1, category, sub_category, Product_link, product_discription, option_name, stock,discontinued) VALUES( %s, %s, %s,%s, %s,%s, %s, %s, %s, %s, %s)"
            my_cursor.execute(sql, values)
            my_db.commit()
        else:
            sql = "UPDATE laubeshop_op SET vnp = %s WHERE sku =%s"
            value = ( price, sku)
            my_cursor.execute(sql, value)
            my_db.commit()

    def get_product_info_from_html(html, data_url):
    # print(data_url)
        #print(html)
        processed = 1
        pro_tag = html.find( class_='productView-product')
        produt_name = pro_tag.find( class_='productView-title').getText().replace("'", "\\'").encode().decode('latin1').replace('â“‡',"").replace('Ã¢\x93\x87','')
        images = html.find( class_='main-image-container').find('li', class_='productView-images')
        description = str(html.find(class_='productView-description').find(id='tab-description').getText().encode().decode('latin1').replace('â“‡',"").replace('Ã‚\xa0','').replace('Ã¢\x80\x9c','"').replace('Ã‚Â½','1/2').replace('2Ã¢\x80\x9d','"').replace('Ã¢\x80\x99',"'").replace('Ã¢\x84Â¢','^TM').replace('Ã¢\x80\x9d','"').replace('Ã¢\x80Â¢','*').replace('Ã¢\x93\x87',''))
        price_tag = html.find(class_='productView-price')
        price = price_tag.find(class_='price price--withoutTax').getText().replace("$", "")
        sku_val = pro_tag.find(class_='productView-info').find( class_='productView-info-value').getText()
        sku=('LB01'+sku_val).replace(' ','').replace('-','')
        option_name = ''
        if images is not None:
            image = images.find('figure', class_='productView-image').get('href')
            
        else:
            image =''
        select = html.find(class_='productView-options').find_all(attrs={"class":"form-field", "data-product-attribute":"set-select"})
        radio = html.find(class_='productView-options').find_all(attrs={"class":"form-field", "data-product-attribute":"set-radio"})
        if select or radio:
            get_price_from_size_option(html, produt_name, sku, price, image, data_url, description, option_name)
        else:
            insert_or_update_product(produt_name, sku, price, image, data_url, description, option_name)

        return processed

    def get_products_from_html(data):
        product_info = get_content_from_url(data[4]+"/?setCurrencyId=1")
        if product_info is None:
            processed = 0
        else:
            processed = get_product_info_from_html(product_info,data[4])

    
    sql = " SELECT * FROM `laubeshop_products_url` where processed=0 "
    my_cursor.execute(sql)
    my_result = my_cursor.fetchall()
    if my_result != []:
        my_cursor = my_db.cursor()
        my_cursor.execute("UPDATE `laubeshop_op`  SET previous_vnp = vnp")
        my_cursor = my_db.cursor()
        my_cursor.execute('UPDATE `laubeshop_op`  SET previous_qty_avb = qty_avb')
    for cate_data in my_result:
        
        get_products_from_html(cate_data)
    my_cursor = my_db.cursor()
    my_cursor.execute("UPDATE `laubeshop_op`  SET qty_avb = stock") 
    my_db.commit()

    my_cursor = my_db.cursor()    
    my_cursor.execute("select sku,vnp,previous_vnp,previous_qty_avb,qty_avb from laubeshop_op")
    result = my_cursor.fetchall()
    with open('laubeshop_vnp.csv', 'w',  newline='') as outcsv:
            writer = csv.writer(outcsv)
            writer = csv.DictWriter(outcsv, fieldnames = ["sku", "vnp", "previous_vnp"])
            writer.writeheader()
            
    with open('laubeshop_stock.csv', 'w',  newline='') as stcsv:
            writers = csv.writer(stcsv)
            writers = csv.DictWriter(stcsv, fieldnames = ["sku", "previous quantity", "quantity available"])
            writers.writeheader()
    with open('laubeshop_new_prod.csv', 'w',  newline='') as skucsv:
            writers = csv.writer(skucsv)
            writers = csv.DictWriter(skucsv, fieldnames = ["new_prod"])
            writers.writeheader()
    for x in result:
        sku=x[0]
        vnp= x[1]
        pvnp= x[2]
        pqty=x[3]
        qty=x[4]
        if vnp!=pvnp:
            with open('laubeshop_vnp.csv', 'a', newline='') as vnpcsv:
                writer = csv.writer(vnpcsv)
                writer = csv.DictWriter(vnpcsv, fieldnames =[sku,vnp,pvnp])
                writer.writeheader()
        if pqty != qty:
            with open('laubeshop_stock.csv', 'a', newline='') as stockcsv:
                writers = csv.writer(stockcsv)
                writers = csv.DictWriter(stockcsv, fieldnames =[sku,pqty,qty])
                writers.writeheader()
    for i in new_prod:
        with open('laubeshop_new_prod.csv', 'a', newline='') as stockcsv:
            writers = csv.writer(stockcsv)
            writers = csv.DictWriter(stockcsv, fieldnames =[i])
            writers.writeheader()
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
    filename = "File_name_with_extension"
    attachment = open('./laubeshop_vnp.csv', "rb")
    
    parter1 = MIMEBase('application', 'octet-stream')
    parter1.set_payload((attachment).read())
    encoders.encode_base64(parter1)
    parter1.add_header('Content-Disposition', 'attachment', filename='laubeshop_vnp.csv')
    msg.attach(parter1)
    
    parter2 = MIMEBase('application', "octet-stream")
    parter2.set_payload(open('./laubeshop_stock.csv', "rb").read())
    encoders.encode_base64(parter2)
    parter2.add_header('Content-Disposition', 'attachment', filename='laubeshop_stock.csv')  
    msg.attach(parter2)

    parter3 = MIMEBase('application', "octet-stream")
    parter3.set_payload(open('./laubeshop_new_prod.csv', "rb").read())
    encoders.encode_base64(parter3)
    parter3.add_header('Content-Disposition', 'attachment', filename='laubeshop_new_prod.csv')  
    msg.attach(parter3)
    
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'Aman@123')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
anand()
def main():
    try:
        anand()
        s = "script excution is successfull"
        mail_send(s)
        print(s)
    except:
        s = "script excution is unsuccessfull"
        print(s)

if __name__ == "__main__":
    main()  

    

