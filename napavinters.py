import requests, pandas as pd, re
from bs4 import BeautifulSoup


def napa_wineries(url):
    
    #get url
    napa_page = requests.get(url)
    #parse the page contents to get ready to scrap
    soup = BeautifulSoup(napa_page.content,'html.parser')
    
    #get the html class that contains all the wineries 
    win_body = soup.find_all(class_='span8')
    #the ugly chars is to strip off special characters gotten when scraping for the phones
    remove_special_chars = str.maketrans('', '', ' \r\n')

    #get company name
    company_name = [infos.find('a',href=True).get_text() for infos in win_body]
    
    #regex to scrap the phones 
    phone = [infos.find(text=re.compile(r'''
    \d\d\d
    (-|\s)*
    \d\d\d
    (-|\s)*
    \d\d\d\d
    ''',re.VERBOSE)) for infos in win_body]
    
    #this is used to remove None values and replace with an empty string, need to do this or else we can't strip off
    #special chars
    conv = lambda i : i or '' 
    phone = [conv(i) for i in phone]
    #this will remove the special chars from each strings in the phone lists
    phone = [s.translate(remove_special_chars) for s in phone]

    #get websites url
    website = []
    for link in soup.find_all('a',href= True,text='website'):
       website.append(link['href'])

    #we need to append an empty string at the end of the list because it scraped an additional winerie thats not part of the list. Have to do this so when putting the 
    #info into pandas, it wont generate list size doesnt match error
    website.append('')
    
    # use panda to organize the datas into columns when exporting to excel/csv
    print_napal_wineries(company_name, phone, website)

def print_napal_wineries(company_name, phone, website):

    napal_infos = pd.DataFrame(
    {
        'Company': company_name,
        'Phone': phone,
        'Website': website
        
    })
    #deletes the last element (refer to above)
    napal_infos = napal_infos.drop(index=549)
    #export to csv/excel
    napal_infos.to_csv("napal.csv")
    napal_infos.to_excel("napal.xlsx")

napa_wineries('https://napavintners.com/wineries/all_wineries.asp')


