import requests, pandas as pd
from bs4 import BeautifulSoup


#TODO: allow arguments so user can look up what they want ( NEED BATCH FILE)
#TODO: also find a way to center the column name pandas...


def get_todays_deals(url):
    
    #get url
    newEggpage = requests.get(url)
    #parse the page wtih beautiful soup
    soup = BeautifulSoup(newEggpage.content,'html.parser')
    
    #the deals are wrapped within a large container so we have to break it down to get to it (I know its confusing lol)
    deals = soup.find(class_='item-cells-wrap tile-cells five-cells')
    items = deals.find_all(class_='item-container items-grid-view show-item-stock')
    #used to remove special chars in the price list generated when getting the prices
    special_Chars = str.maketrans("", "", "\t\n\r–")

    #get the deals name
    dealsGroupName = [item.find(class_='item-title').get_text() for item in items]
    #get the prices
    prices = [item.find(class_='price-current').get_text().translate(special_Chars) for item in items]
    print_todaydeals_table(dealsGroupName, prices)

#same as above but for tomorrow deals
def print_tmr_deals(url):
    
    newEggpage = requests.get(url)
    soup = BeautifulSoup(newEggpage.content,'html.parser')
    deals = soup.find_all(class_='item-container items-grid-view')

    dealsGroupName = [item.find(class_='item-title').get_text() for item in deals]
    prices = 'TBD'
    print_tmrdeals_table(dealsGroupName,prices)
    


#function to todays deals using pandas and generate a excel file with it
def print_todaydeals_table(dealsGroupName,prices):
    
    daily_deals = pd.DataFrame(
        {
            'item': dealsGroupName,
            'price': prices
            
        } 
    )
    print(daily_deals)
    daily_deals.to_excel('DailyNeweggDeals.xlsx')

#function to organize tomorrows deals using pandas and generate a excel file with it
def print_tmrdeals_table(dealsGroupName, prices):
    
    tmr_deals = pd.DataFrame(
        {
            'item': dealsGroupName,
            'price': prices
            
        }

    )
    print(tmr_deals)
    tmr_deals.to_excel('TmrNeweggDeals.xlsx')



get_todays_deals('https://www.newegg.com/todays-deals')
print_tmr_deals('https://www.newegg.com/todays-deals')

