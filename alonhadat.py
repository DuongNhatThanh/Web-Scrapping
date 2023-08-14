import requests
from bs4 import BeautifulSoup
import pandas as pd
import glob
import os
import time
from datetime import date
from datetime import timedelta
import unidecode
import shutil
import random
# from fake_useragent import UserAgent

# ua = UserAgent()
today = date.today()
d1 = today.strftime("%d/%m/%Y")
d2 = (today - timedelta(days = 1)).strftime("%d/%m/%Y")

def page_authentication(url):
        # It sets the headers dictionary to mimic a user-agent for the request. 
        # The user-agent string provided in the code snippet is for a specific version of the Chrome browser on macOS. 
        # This helps to ensure that the request appears to be coming from a web browser rather than a bot.
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    if response.status_code < 200 or response.status_code > 299:
        raise Exception(f'Failed to load the page {url}')
    page_content = response.text
    webpage =  BeautifulSoup(page_content, 'html.parser')
    return webpage


def property_extractor(url):
    property_name = []
    property_area = []
    property_size = []
    property_direction = []
    property_road_width = []
    property_floors = []
    property_bedroom = []
    property_parking = []
    property_price = []
    property_location = []
    property_date = []
    property_thumb = []
    property_post_link = []
    webpages = url.find_all('div', {"class":'content-item'})
    for webpage in webpages:
        
            # extract title of property
        name_class = 'ct_title'
        prop_name = webpage.find_all('div', {"class":name_class})
        for tag in prop_name:
            property_name.append(tag.text)
            
            # extract area of property
        area_class = 'ct_dt'
        prop_area = webpage.find_all('div', {'class':area_class})
        if (prop_area) == []:
            property_area.append('No Information')
        else:
            for tag in prop_area:
                property_area.append(tag.text)
            
            # extract size of property
        size_class = 'ct_kt'
        prop_size = webpage.find_all('div', {'class':size_class})
        if (prop_size) == []:
            property_size.append('No Information')
        else:
            for tag in prop_size:
                property_size.append(tag.text)
            
            # extract direction of property
        direction_class = 'ct_direct'
        prop_direct = webpage.find_all('div', {'class':direction_class})
        if (prop_direct) == []:
            property_direction.append('No Information')
        else:
            for tag in prop_direct:
                if (tag.text == 'Hướng: _'):
                    property_direction.append('Hướng: No Information')
                else:
                    property_direction.append(tag.text)

            # extract road-width of property
        road_width_class = 'road-width'
        prop_road = webpage.find_all('span', {'class':road_width_class})
        if (prop_road) == []:
            property_road_width.append('No Information')
        else:
            for tag in prop_road:
                property_road_width.append(tag.text)

            # extract floors of property
        floors_class = 'floors'
        prop_floors = webpage.find_all('span', {'class':floors_class})
        if (prop_floors) == []:
            property_floors.append('No Information')
        else:
            for tag in prop_floors:
                property_floors.append(tag.text)
            
            # extract bedroom of property
        bedroom_class = 'bedroom'
        prop_bedroom = webpage.find_all('span', {'class':bedroom_class})
        if (prop_bedroom) == []:
            property_bedroom.append('No Information')
        else:
            for tag in prop_bedroom:
                property_bedroom.append(tag.text)
                
            # extract parking of property
        parking_class = 'parking'
        prop_paking = webpage.find_all('span', {'class':parking_class})
        if (prop_paking) == []:
            property_parking.append('No Information/ Không có chỗ để xe')
        else:
            for tag in prop_paking:
                property_parking.append(('Có ' + tag.text))
            
            # extract price of property
        price_class = 'ct_price'
        prop_price = webpage.find_all('div', {'class':price_class})
        if (prop_price) == []:
            property_price.append('No Information')
        else:
            for tag in prop_price:
                property_price.append(tag.text)

            # extract location of property
        location_class = 'ct_dis'
        prop_location = webpage.find_all('div', {'class':location_class})
        if (prop_location) == []:
            property_location.append('No Information')
        else:
            for tag in prop_location:
                property_location.append(tag.text)
            
            # extract the post's date of property
        date_class = 'ct_date'
        prop_date = webpage.find_all('div', {"class":date_class})
        for tag in prop_date:
            if (tag.text == 'Hôm nay'):
                property_date.append(str(d1))
            elif (tag.text == 'Hôm qua'):
                property_date.append(str(d2))
            else:
                property_date.append(tag.text)
                
            # extract thumbnail of property
        thumbnail_class = 'thumbnail'
        prop_thumb = webpage.find_all('div', {"class":thumbnail_class})
        for tag in prop_thumb:
            property_post_link.append(('https://alonhadat.com.vn' + tag.a.get('href')))
            property_thumb.append(('https://alonhadat.com.vn' + tag.img['src']))
        
        # make a dataframe
    property_dict = {
        'Title':property_name,
        'Area': property_area,
        'Sizes': property_size,
        'Direction': property_direction,
        'Floors': property_floors,
        'Bedrooms': property_bedroom,
        'Price': property_price,
        'Location': property_location,
        'Timestamp of the post': property_date,
        'Thumbnail': property_thumb,
        'Post Link': property_post_link
    }

    property_df = pd.DataFrame(property_dict)

    return property_df


def csv_maker(dataframe, foldername, filename):
    dataframe.to_csv(f"{foldername}\{filename}.csv", index=None)

def csv_merger(path):
    all_files = glob.glob(path + "/Pages" + "/*.csv")
    df_lst = []
    for filename in all_files:
        df = pd.read_csv(filename,index_col=None, header=0)
        df_lst.append(df)
    final_dataframe = pd.concat(df_lst, axis=0, ignore_index=True)
    final_dataframe.to_csv(f'{path}\PropertiesFinal.csv', index=None)
    shutil.rmtree(f'{path}\Pages', ignore_errors=True)  

    

# Main script
if __name__ == "__main__":
    os.makedirs('Properties-csv-files-07082023-alonhadat', exist_ok=True)
    options = ['can-ban', 'cho-thue']
    fol_names = ['For sale', 'For rent']
    min_page_no = 1
    max_page_no = 100
            
    for i in range(0, len(options)):
        option = options[i]
        fol_name = fol_names[i]
        os.makedirs(f'Properties-csv-files-07082023-alonhadat/{fol_name}', exist_ok=True)
        os.makedirs(f'Properties-csv-files-07082023-alonhadat/{fol_name}/Pages', exist_ok=True)

        for pg_number in range(min_page_no, max_page_no+1):
            pg_url = f'https://alonhadat.com.vn/nha-dat/{option}/trang--{pg_number}.html'
            folder = f'Properties-csv-files-07082023-alonhadat/{fol_name}/Pages'
            data = property_extractor(url=page_authentication(url=pg_url))
            if data.empty:
                break  # Exit loop if no data is found
            csv_maker(dataframe=data, foldername=folder, filename='page'+str(pg_number))
            time.sleep(random.randint(60, 90))
            
        # Merge all the CSV files in each folder into one file
        filepath = f'Properties-csv-files-07082023-alonhadat/{fol_name}'
        if os.listdir(path=f'{filepath}/Pages') != []:
            csv_merger(path=filepath)
        else: 
            shutil.rmtree(f'{filepath}/Pages', ignore_errors=True)
            with open(f'{filepath}/readme.txt', 'w') as f:
                f.write('There is no information about real estate on the website!')