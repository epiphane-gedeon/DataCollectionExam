from pandas.io.sql import DataFrame
import streamlit as st
import pandas as pd
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

# Settings
options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

st.set_page_config(page_title="DataCollection", layout="wide")
# Settings


st.write("# Data Collection")


side= st.sidebar
def csv_button(data_source : DataFrame, csv_name : str = "data.csv"):
    return st.download_button(
        label="Download as CSV",
        data=data_source.to_csv(index=False).encode("utf-8"),
        file_name=csv_name,
        mime="text/csv"
    )

def save_button(data_source : DataFrame, table_name : str) :
    st.button(
        label="Save",
        on_click=saveDfInSql,
        args=(data_source, table_name),
        type= "primary"
    )

def scrapeAndClearBooks(limit:int = 0) -> DataFrame:
    # Scraping
    
    df_test = pd.DataFrame()
    i = 1
    url = f'https://books.toscrape.com/catalogue/page-{i}.html'
    driver.get(url)
    containers = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod')
    
    while len(containers) > 0:
    
        if i > limit and limit > 0 :
            break
        
        url = f'https://books.toscrape.com/catalogue/page-{i}.html'
        driver.get(url)
        
        containers = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod')
        
        book_urls = []
        data_cont = []
        for container in containers:
            book_urls.append(container.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
            stock = container.find_element(By.CSS_SELECTOR, 'p.instock.availability').text
            
        for book_url in book_urls:
            driver.get(book_url)
            
            try :
                dic={
                    'title' : driver.find_element(By.CSS_SELECTOR, 'h1').text,
                    'price' : driver.find_element(By.CSS_SELECTOR, 'p.price_color').text,
                    'availability' : stock,
                    'number_of_products' : driver.find_element(By.CSS_SELECTOR, 'table.table.table-striped tr:nth-child(6) td:nth-child(2)').text,
                    'rating' : driver.find_element(By.CSS_SELECTOR, 'p.star-rating').get_attribute('class'),
                    'number_of_reviews' : driver.find_element(By.CSS_SELECTOR, 'table.table.table-striped tr:nth-child(7) td:nth-child(2)').text,
                    'description' : driver.find_element(By.CSS_SELECTOR, 'article.product_page > p:nth-of-type(1)').text,
                    'product_type' : driver.find_element(By.CSS_SELECTOR, 'table.table.table-striped tr:nth-child(2) td:nth-child(2)').text,
                    'tax' : driver.find_element(By.CSS_SELECTOR, 'table.table.table-striped tr:nth-child(5) td:nth-child(2)').text
                }
                data_cont.append(dic)
            except:
                pass
        df = pd.DataFrame(data_cont)
        df_test = pd.concat([df_test, df], axis = 0).reset_index(drop = True)
        
        i += 1
    # Scraping
    # Clearing

    df_test[['price', 'tax']] = df_test[['price', 'tax']].replace('£', '', regex=True).astype(float)

    df_test['number_of_products'] = df_test['number_of_products'].str.replace('In stock (', '').str.replace(' available)', '').astype(int)
    df_test['rating'] = df_test['rating'].str.replace('star-rating ', '')

    correspondance = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    
    df_test['rating'] = df_test['rating'].map(correspondance)

    # Clearing
    
    return df_test

def scrapeAndClearCars(limit:int = 0) -> DataFrame:
    df_gaaraas = pd.DataFrame()
    
    i = 1
    url = f'https://www.gaaraas.com/fr/users/dakar-auto?page={i}'
    driver.get(url)
    containers = driver.find_elements(By.CSS_SELECTOR, 'a.common-ad-card')
    
    # for i in range (1, 3) :
    while len(containers) > 0 :
    
        if i > limit and limit > 0 :
            break
    
        url = f'https://www.gaaraas.com/fr/users/dakar-auto?page={i}'
        driver.get(url)
    
        containers = driver.find_elements(By.CSS_SELECTOR, 'a.common-ad-card')
    
        data_cont = []
        for container in containers:
            car_info_text = container.find_element(By.CSS_SELECTOR, '.ad-specification .specification-section h4').text
        
            match = re.match(r'^(\d{4})\s+([^\s]+)(?:\s+(.*))?$', car_info_text)
    
            if match:
                year = match.group(1)
                brand = match.group(2)
                model = match.group(3) if match.group(3) is not None else ""
            else:
                year = car_info_text
                brand= car_info_text
                model = car_info_text
    
            try :
                dic={
                    'brand' : brand,
                    'model' : model,
                    'year' : year,
                    'price' : driver.find_element(By.CSS_SELECTOR, '.ad-vehicle-price .price-wrap .price').text,
                    'kilometers' : driver.find_element(By.CSS_SELECTOR, '.ad-vehicle-mileage .title .value').text,
                    'gear_box' : driver.find_element(By.CSS_SELECTOR, '.ad-vehicle-engine .transmission').text,
                    'seling_region' : driver.find_element(By.CSS_SELECTOR, '.ad-specification .specification-section .location').text,
                }
                data_cont.append(dic)
            except:
                pass
        df = pd.DataFrame(data_cont)
        df_gaaraas = pd.concat([df_gaaraas, df], axis = 0).reset_index(drop = True)
    
        i += 1

    df_gaaraas['price']= df_gaaraas['price'].str.replace(' ', '').astype(int)
    df_gaaraas['kilometers']= df_gaaraas['kilometers'].str.replace('KM','').str.replace(' ', '').astype(int)
    df_gaaraas['year'] = pd.to_numeric(df_gaaraas['year'], errors='coerce').astype(pd.Int64Dtype())
    df_gaaraas.dropna(inplace=True)
    
    return df_gaaraas

def saveDfInSql(df :DataFrame, table_name:str) :
    import sqlite3
    
    conn = sqlite3.connect("datas.sqlite")
    
    df.to_sql(
        name = table_name,
        con = conn,
        if_exists = "replace",
        index = False
    )
    
    conn.close()
    
    st.toast("Les données ont bien été enregistrées !")


choices = {
    0 : "What do you need ?",
    1: "Scrape datas with Selenium",
    2: "Download datas scraped with Web Scraper",
}

sources = {
    0 : "Whitch source ?",
    1: "Books to scrap",
    2: "Gaaraas"
}

choice = side.selectbox(
    label="",
    options=list(choices.keys()),
    format_func=lambda x: choices[x]
)

if choice == 1:
    source = side.selectbox(
        label="",
        options=list(sources.keys()),
        format_func=lambda x: sources[x]
    )
    limit = side.number_input(label="How many pages ? 1-100", min_value=1, max_value=100)
    if source==1:
        st.write("## Books to scrape")
        books = scrapeAndClearBooks(limit)
        st.write(books)

        col1, col2, _ = st.columns([1, 1, 8])
        
        with col1:
            csv_button(
                data_source=books,
                csv_name="books_to_scrape.csv"
            )
        
        with col2:
            save_button(
                data_source=books,
                table_name="books_to_scrap"
            )

    if source ==2:
        st.write("## Gaaraas")
        cars = scrapeAndClearCars(limit)
        st.write(cars)

        col1, col2, _ = st.columns([1, 1, 8])
        
        with col1:
            csv_button(
                data_source=cars,
                csv_name="gaaraas.csv"
            )
        
        with col2:
            save_button(
                data_source=cars,
                table_name="gaaraas"
            )
    
elif choice == 2:
    source = side.selectbox(
        label="",
        options=list(sources.keys()),
        format_func=lambda x: sources[x]
    )
    if source == 1:
        data_books = pd.read_csv("books_to_scrap.csv")
        st.write(data_books)
        st.download_button(
            label="Download as CSV",
            data=data_books.to_csv(index=False).encode("utf-8"),
            file_name="gaaraas.csv",
            mime="text/csv"
        )
    elif source == 2:
        data_gaaraas = pd.read_csv("gaaraas.csv")
        st.write(data_gaaraas)
        st.download_button(
            label="Download as CSV",
            data=data_gaaraas.to_csv(index=False).encode("utf-8"),
            file_name="gaaraas.csv",
            mime="text/csv"
        )
