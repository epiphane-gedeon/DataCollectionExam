import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def dashboardCars():
    import sqlite3
    
    conn = sqlite3.connect("datas.sqlite")
    
    df_gaaraas=pd.read_sql(f"SELECT * FROM gaaraas",conn)
    
    st.write(df_gaaraas)
    
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    fig5, ax5 = plt.subplots()
    fig6, ax6 = plt.subplots()
    fig7, ax7 = plt.subplots()
    
    sns.histplot(
        df_gaaraas["price"] / 1_000_000,
        bins=20,
        kde=True,
        ax=ax
    )
    
    ax.set_title("Distribution of Car Prices")
    ax.set_xlabel("Price (millions)")
    ax.set_ylabel("Frequency")
    ax.ticklabel_format(style="plain", axis="x")
    
    
    sns.histplot(df_gaaraas["kilometers"] / 1_000, bins=20, kde=True,ax=ax2)
    ax2.set_title('Distribution of Car Kilometers')
    ax2.set_xlabel('Kilometers (thousand)')
    ax2.set_ylabel('Frequency')
    ax2.ticklabel_format(style='plain', axis='x')
    
    top_brands = df_gaaraas['brand'].value_counts().nlargest(10).index
    sns.countplot(y='brand', data=df_gaaraas, order=top_brands, palette='viridis',ax=ax3)
    ax3.set_title('Top 10 Car Brands')
    ax3.set_xlabel('Count')
    ax3.set_ylabel('Brand')

    
    sns.countplot(x='gear_box', data=df_gaaraas, palette='magma', ax=ax4)
    ax4.set_title('Distribution of Gear Box Types')
    ax4.set_xlabel('Gear Box Type')
    ax4.set_ylabel('Count')
    
    df_scater=df_gaaraas.copy()
    
    df_scater['price'] = df_scater['price']/1_000_000
    df_scater['kilometers'] = df_scater['kilometers']/1_000
    
    sns.scatterplot(x='kilometers', y='price', hue='gear_box', data=df_scater, palette='cividis', s=100, alpha=0.7, ax=ax5)
    ax5.set_title('Kilometers vs. Price (by Gear Box)')
    ax5.set_xlabel('Kilometers (thousand)')
    ax5.set_ylabel('Price (millions)')
    ax5.ticklabel_format(style='plain', axis='x')
    ax5.ticklabel_format(style='plain', axis='y')
    
    
    avg_price_by_year = (
        df_gaaraas.groupby('year')['price']
        .mean()
        .reset_index()
    )
    
    avg_price_by_year['price'] = avg_price_by_year['price'] / 1_000_000
    
    sns.barplot(x='year', y='price', data=avg_price_by_year, palette='cubehelix', ax=ax6)
    ax6.set_title('Average Price by Year of Manufacture (millions)')
    ax6.set_xlabel('Year')
    ax6.set_ylabel('Average Price')
    ax6.tick_params(axis='x', rotation=45)
    ax6.ticklabel_format(style='plain', axis='y')

    avg_price_by_brand = (
        df_gaaraas.groupby('brand')['price']
        .mean()
        .reset_index()
    )
    
    avg_price_by_brand['price'] = avg_price_by_brand['price'] / 1_000_000
    
    sns.barplot(y='brand', x='price', data=avg_price_by_brand, palette='viridis', ax=ax7)
    ax7.set_title('Average Price by Brand (millions)')
    ax7.set_xlabel('Average Price')
    ax7.set_ylabel('Brand')
    ax7.ticklabel_format(style='plain', axis='x')
    
    
    unique_models = df_gaaraas[["brand", "model"]].drop_duplicates(ignore_index=True)
    unique_brands = df_gaaraas["brand"].drop_duplicates(ignore_index=True)
    totalObservation = len(df_gaaraas)
    numberOfBrands = len(unique_brands)
    numberOfModels = len(unique_models)
    
    
    kpi1, kpi2, kpi3 = st.columns(3, border=True)
    
    kpi1.write("Total observations")
    kpi1.title(totalObservation, text_alignment="center")
    
    kpi2.write("Unique brands number")
    kpi2.title(numberOfBrands, text_alignment="center")
    
    kpi3.write("Unique models number")
    kpi3.title(numberOfModels, text_alignment="center")
    
    tab1, tab2 = st.columns(2)
    tab1.write("### Unique brands lists")    
    tab1.write(unique_brands)
    
    tab2.write("### Unique models lists with brands") 
    tab2.write(unique_models)
    
    col1, col2, col3 = st.columns(3)
    col1.pyplot(fig)
    col2.pyplot(fig2)
    col3.pyplot(fig3)
    
    col1.pyplot(fig4)
    col2.pyplot(fig5)
    col3.pyplot(fig6)

    st.pyplot(fig7)

def dashboardBooks():
    import sqlite3
    
    conn = sqlite3.connect("datas.sqlite")
    
    df_books=pd.read_sql(f"SELECT * FROM books_to_scrap",conn)

    st.write(df_books)

    
    fig, ax = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()
    fig4, ax4 = plt.subplots()
    fig5, ax5 = plt.subplots()
    fig6, ax6 = plt.subplots()

    
    sns.histplot(df_books['price'], bins=10, kde=True, ax=ax)
    ax.set_title('Distribution of Book Prices')
    ax.set_xlabel('Price (£)')
    ax.set_ylabel('Frequency')

    sns.histplot(df_books['number_of_products'], bins=10, kde=True,ax=ax2)
    ax2.set_title('Distribution of Books Available in Stock')
    ax2.set_xlabel('Number of Products Available')
    ax2.set_ylabel('Frequency')

    sns.countplot(x='rating', data=df_books, palette='viridis', ax=ax3)
    ax3.set_title('Distribution of Book Ratings')
    ax3.set_xlabel('Star Rating (1-5)')
    ax3.set_ylabel('Count')

    sns.boxplot(x='rating', y='price', data=df_books, palette='magma', ax=ax4)
    ax4.set_title('Price Distribution by Rating')
    ax4.set_xlabel('Star Rating')
    ax4.set_ylabel('Price (£)')

    sns.countplot(x='product_type', data=df_books, palette='viridis', ax=ax5)
    ax5.set_title('Distribution of Product types')
    ax5.set_xlabel('Product type')
    ax5.set_ylabel('Count')

    avg_price_by_rating = df_books.groupby('rating')['price'].mean().reset_index()
    
    sns.barplot(x='rating', y='price', data=avg_price_by_rating, palette='cubehelix',ax=ax6)
    ax6.set_title('Average Price by Star Rating')
    ax6.set_xlabel('Star Rating')
    ax6.set_ylabel('Average Price (£)')

    totalObservation = len(df_books)
    meanBookPrice = df_books['price'].mean().round(2)
    stockPercentage = (df_books['availability'].eq("In stock").mean() * 100)
    
    
    kpi1, kpi2, kpi3 = st.columns(3, border=True)
    
    kpi1.write("Total observations")
    kpi1.title(totalObservation, text_alignment="center")
    
    kpi2.write("Average book price (£)")
    kpi2.title(meanBookPrice, text_alignment="center")
    
    kpi3.write("Percebtage In stock (%)")
    kpi3.title(stockPercentage, text_alignment="center")

    col1,col2,col3 = st.columns(3)

    col1.pyplot(fig)
    col2.pyplot(fig2)
    col3.pyplot(fig3)

    col1.pyplot(fig4)
    col2.pyplot(fig5)
    col3.pyplot(fig6)
    
    

st.set_page_config(page_title="Dashboard", layout="wide")

side= st.sidebar

choices = {
    0: "Books to scrape",
    1: "Gaaraas",
}

choice = side.selectbox(
    label="",
    options=list(choices.keys()),
    format_func=lambda x: choices[x]
)

st.write("# Dashboard")

if choice == 0 :
    dashboardBooks()
else :
    dashboardCars()