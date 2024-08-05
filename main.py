import requests 
import tkinter as tk
import time 
import statistics
import pandas as pd 
import re 
import matplotlib.pyplot as plt 
from bs4 import BeautifulSoup








def get_home_prices(zip_code): 
        headers = {
    'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}
        

        api_url = f"http://api.zippopotam.us/us/{zip_code}"
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        state_abbreviation = data['places'][0]['state abbreviation']  
        url = f"https://www.estately.com/{state_abbreviation}/{zip_code}/"
        url1 = f"https://homefinder.com/homes-for-sale/zip-code/{zip_code}"
        url2 = "https://www.homesandland.com/homes/{}/?property_type=residential&transaction_type=any&format=list&sort=featured&page={}/"
        url3 = "https://www.coldwellbanker.com/zip/{}/{}?page={}"


        
        r = requests.get(url , headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        price_elements = soup.find_all(class_='result-price margin-bottom-10')

        prices = [int(''.join(filter(str.isdigit, price_element.text))) for price_element in price_elements]
        sorted_pricess = sorted(prices)
        print(sorted_pricess)
        median_prices = statistics.median(sorted_pricess)



        #HomeFinder


        r1 = requests.get(url1, headers=headers)
        soup1 = BeautifulSoup(r1.text, 'html.parser')
        price1_elements = soup1.find_all(class_='h4 text-primary mb-0')

        prices1 = []

        for price1_element in price1_elements:
            price1_text = price1_element.get_text(strip=True)
            price1_value_match = re.search(r'[\d,]+(?:\.\d{1,2})?', price1_text)
            price1_value = int(price1_value_match.group().replace(',', ''))
            prices1.append(price1_value)
        sorted_price1 = sorted(prices1)
        median_price1 = statistics.median(sorted_price1)


        # HomeandLand Website

        prices2 = [] # creating an empty array to store the prices into 

        for page_number in range(1, 5 + 1):
            urll = url2.format(zip_code, page_number)

            r2 = requests.get(urll, headers=headers)
            soup2 = BeautifulSoup(r2.text, 'html.parser')
            price2 = soup2.find_all(class_='price')
            for price in price2:
                priceList = price.get_text().replace('$', '').replace(',', '').strip() # removing "$" and other misc characters 
                price_value2 = int(priceList)
                prices2.append(price_value2) # putting the prices into the array
                sorted_price2 = sorted(prices2) # sorting the prices from least to greatest
        median_price2 = statistics.median(sorted_price2) # getting the median price for the data in the array
        

            # ColdWellBanker homes

        prices3 = [] # creating array to store prices

        for page_numberr in range(1, 2 + 1): # page number iteration 
            url4 = url3.format(state_abbreviation, zip_code, page_numberr)

            r3 = requests.get(url4, headers=headers)
            soup3 = BeautifulSoup(r3.text, 'html.parser')
            price3 = [int(''.join(filter(str.isdigit, price.text.strip()))) for price in soup.find_all('h6', {'data-testid': 'price'})]
            for price in prices:
                print(price)
                prices3.append(price) # adding prices to the array
        sorted_prices = sorted(prices3)
        median_prices1 = statistics.median(sorted_prices) # getting the median of the data in the array

        plt.bar(range(len(sorted_prices)), sorted_prices)
        plt.xlabel('Home')
        plt.ylabel('Prices')
        plt.title("ColdWellBanker prices ")
        plt.show()

        plt.bar(range(len(sorted_price2)), sorted_price2)
        plt.xlabel('Home')
        plt.ylabel('Prices')
        plt.title("HomeandLand Prices")
        plt.show()

        plt.bar(range(len(sorted_price1)), sorted_price1)
        plt.xlabel('Home')
        plt.ylabel('Prices')
        plt.title('HomeFinder Prices')
        plt.show()

        plt.bar(range(len(sorted_pricess)), sorted_pricess)
        plt.xlabel('Home')
        plt.ylabel('Prices')
        plt.title('Estately Prices')
        plt.show()


        return f"Estately median price: {median_prices} | ColdWellBanker median price: {median_prices1} | HomeandLand median price: {median_price2} | HomeFinder median price: {median_price1}"




def scrape_prices(): # create function to use as the backend for the gui
     zip_code = zip_code_entry.get()
     prices = get_home_prices(zip_code)
     price_label.config(text=prices)

root = tk.Tk()

zip_code_label = tk.Label(root, text="Enter zip code:") # creating a label for people to enter their zip code
zip_code_label.pack()

zip_code_entry = tk.Entry(root) # storing the entered zip code to use it in the function 
zip_code_entry.pack()

scrape_button = tk.Button(root, text="Scrape Prices", command=scrape_prices) # giving the button a functionallity with the function made to get the prices
scrape_button.pack()

price_label = tk.Label(root, text="")
price_label.pack()

root.mainloop()
