from msilib.schema import ComboBox, ListBox
from multiprocessing.spawn import import_main_path
from re import L, search
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import tkinter
#import customtkinter
import os
import time

# HOME DEPOT AVERAGE: 16S
# Time: 15.715083122253418
# Time: 34.86494517326355
# Time: 17.759044408798218
# Time: 10.43810510635376
# Time: 8.791106462478638
# Time: 15.088213443756104
# Time: 13.768413066864014

# LOWES AVERAGE: 7S
# Time: 7.04963755607605
# Time: 10.18962287902832
# Time: 6.374977350234985
# Time: 9.269612789154053
# Time: 6.529359340667725
# Time: 8.239041328430176
# Time: 6.88259220123291

'''
driver = 'chromedriver_win32 (1)/chromedriver.exe'

url = input('Where would you buy your supplies from:\n')
item = input('What do you want to buy:\n')
browser = webdriver.Chrome(driver)
start_time = time.time()
browser.get('http://www.{website}.com'.format(website = str(url)))


inputBox = browser.find_element(By.NAME, 'searchTerm').send_keys(item)
print('Time: {ftime}'.format(ftime = time.time() - start_time))
'''
# Global variables
search_list = []
large_font = 32

def addAllPrices(prices):
    pass

def getPrices():
    prices = []
    x = 0
    try:
        while x != len(search_list):
            remove_item = search_list[x].split(":")
            prices.append(remove_item[1])
            x += 1
        return prices
    except IndexError:
        return("None")

# This will turn the price and item into two different items on the UI List to make it easier for users to read
def seperateString(beautify):
    new_item = beautify.split(":")
    return new_item

def updateListUi(place, text):
    item_list.delete(place)
    updated_item = seperateString(text)
    item_list.insert(place, updated_item)

def priceString(string):
    try:
        print(string)
        # remove <
        li = str(string).split("<")
        first_digit = li[4]
        final_number = first_digit.split(">")
        fn = final_number[1]
        # print(fn)
        second_digit = li[6]
        sn = second_digit.split(">")
        # print(sn[1])
        output = (fn + '.' + sn[1])
        return output
    except IndexError:
        return("Not Found")

def readFilePrice(link):
    f = open("text.txt", 'r', encoding='utf-8')
    contents = f.read()
    soup = BeautifulSoup(contents, features='html.parser')
    quote = soup.find('div', attrs={'class': 'price-format__main-price'})

    # priceString(quote)
    return quote

# TODO: create function to loop through list for searching and then .config the list item with new price

# This function takes the price and item and groups them together to give to a function that will update the UI List
def updatePriceStr(vname, price):
    single_item = item_list.get(vname)
    # grab the list itself and use the vname (number) to find position and update the list.
    updated_item = search_list[vname] = single_item + ':' + price
    # print("Updated item: \n" + updated_item)
    # print("Item List: \n" + str(search_list))
    updateListUi(vname, search_list[vname])

def getPricePageHtml(pageLink):
    quote_page = pageLink
    page = os.system('cmd /c curl -o text.txt {url}'.format(url=quote_page))
    f = open('test.txt', "w")
    # readFilePrice(quote_page)
    return quote_page

def engine(search_item):
    driver = 'chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(driver, options=chrome_options)
    browser.get('http://www.{website}.com'.format(website=str('homedepot')))

    browser.find_element(By.CLASS_NAME, 'SearchBox__input').send_keys(search_item, Keys.ENTER)
    browser.find_element(By.CLASS_NAME, 'SearchBox__input').clear()
    webpage = browser.current_url
    return webpage

# Main starting point for program
def startSearch():
    start_time = time.time()
    x = 0
    # while x isnt equal to length of search_list get search_list[number] scrape data for value
    while x != len(search_list):
        item = search_list[x]
        webpage = engine(item)
        step2 = getPricePageHtml(webpage)
        step3 = readFilePrice(step2)
        #checks for price or none, error catching stage
        step4 = priceString(step3)
        # print(step4)
        updatePriceStr(x, step4)
        # add step4 (price of item) to page for user to see
        x += 1
    items_prices = getPrices()
    addAllPrices(items_prices)
    # print("Final list output: \n" + str(search_list))
    print('Time: {ftime}'.format(ftime=time.time() - start_time))

# below functions manipulate list/items
def addItem(Vname):
    Vname.insert(len(search_list), search_list[-1])

def AddToList():
    item = itemInput.get()
    search_list.append(item)
    # print(search_list)
    addItem(item_list)
    return search_list

def clearList():
    item_list.delete(0, len(search_list))
    x = 0
    for x in search_list:
        search_list.remove(x)
    print("New search list: \n" + str(search_list))


websites = ['homedepot', 'lowes']
btn_color = '#04426E'
txt_color = 'white'
background_color = '#0b0c0b'

app = tkinter.Tk()
app.configure(bg='black')

label = tkinter.Label(app, text='item', bg='black', fg=txt_color)
label.grid(row=0, column=0)

itemInput = tkinter.Entry(app)
itemInput.grid(row=1, column=0)

addBtn = tkinter.Button(app, text='Add', command=AddToList, bg=btn_color, fg=txt_color)
addBtn.grid(row=1, column=1)

# STARTS MAIN PROCESS
searchBtn = tkinter.Button(app, text='Search', command=startSearch, bg=btn_color, fg=txt_color)
searchBtn.grid(row=2, column=1)

clearBtn = tkinter.Button(app, text="Clear", command=clearList, bg=btn_color, fg=txt_color)
clearBtn.grid(row=3, column=1)

item_list = tkinter.Listbox(app, font=large_font)
item_list.grid(row=2, column=0)

"""customtkinter.set_appearance_mode("dark")

app = customtkinter.CTk()

label = customtkinter.CTkLabel(app, text='item')
label.grid(row=0, column=0)

itemInput = customtkinter.CTkEntry(app)
itemInput.grid(row=1, column=0)

addBtn = customtkinter.CTkButton(app, text='Add', command=AddToList)
addBtn.grid(row=1, column=1)

# STARTS MAIN PROCESS
searchBtn = customtkinter.CTkButton(app, text='Search', command=startSearch)
searchBtn.grid(row=2, column=1)

clearBtn = customtkinter.CTkButton(app, text="Clear", command=clearList)
clearBtn.grid(row=2, column=0)

item_list = tkinter.Listbox(app, font=large_font)
item_list.grid(row=2, column=2)"""

app.mainloop()