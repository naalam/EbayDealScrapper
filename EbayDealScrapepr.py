from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

# Function to scrape eBay deals page
def scrape_ebay_deals():
    url = 'https://www.ebay.com/deals'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    items = soup.select('.dne-itemtile-detail')
    
    titles = []
    prices = []
    links = []

    for item in items:
        title = item.select_one('.ebayui-ellipsis-2')
        price = item.select_one('.first')
        link = item.select_one('[itemprop="url"]')

        titles.append(title.text if title else 'N/A')
        prices.append(price.text if price else 'N/A')
        links.append(link['href'] if link else 'N/A')

    df = pd.DataFrame({
        'title': titles,
        'price': prices,
        'links': links
    })

    filename = f"C:\\Users\\HASSA\\OneDrive\\Documents\\Scratch\\EbayDeal_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    df.to_excel(filename, index=False)
    return filename

# Function to scrape eBay product details
def scrape_product_details(filename):
    df = pd.read_excel(filename)
    proddescription = []
    itemcondition = []
    itemprice = []
    title = []

    for link in df['links']:
        if link == 'N/A':
            proddescription.append('N/A')
            itemcondition.append('N/A')
            itemprice.append('N/A')
            title.append('N/A')
            continue

        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        proddescription.append(soup.select_one('[class="ux-textspans ux-textspans--BOLD"]').text if soup.select_one('[class="ux-textspans ux-textspans--BOLD"]') else 'N/A')
        itemcondition.append(soup.select_one('ux-textspans').text if soup.select_one('ux-textspans') else 'N/A')
        itemprice.append(soup.select_one('[data-testid="x-price-primary"]').text if soup.select_one('[data-testid="x-price-primary"]') else 'N/A')
        title.append(soup.select_one('.ux-seller-section__item--directFromBrand')['title'] if soup.select_one('.ux-seller-section__item--directFromBrand') else 'N/A')

    df_details = pd.DataFrame({
        'proddescription': proddescription,
        'itemcondition': itemcondition,
        'itemprice': itemprice,
        'title': title
    })

    filename_details = f"C:\\Users\\HASSA\\OneDrive\\Documents\\Scratch\\EbayDeal_Detail_{datetime.now().strftime('%Y%m%d%H%M%S')}.xlsx"
    df_details.to_excel(filename_details, index=False)

if __name__ == "__main__":
    filename = scrape_ebay_deals()
    scrape_product_details(filename)
