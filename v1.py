from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from msilib.schema import ComboBox, ListBox
from multiprocessing.spawn import import_main_path
from bs4 import BeautifulSoup
from tkinter import *
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

def updateListAfterQ():
    x=0
    for y in search_list:
        item_list.delete(x)
        item = search_list[x]
        item.split(":")
        item_list.insert(x, item)

        x+=1

def addAfterQuantity():
    print(search_list)
    prices = []
    for x in search_list:
        test = x.split(":")
        prices.append(float(test[1]))
        total_price = sum(prices)

    totalPriceNumber.config(text="$" + str(round(total_price, 2)))
    updateListAfterQ()

def updatePriceWithQuantity(index):
    item_price = search_list[index]
    updated = item_price.split(":")
    return updated[1]

def addAllPrices(TheNumbersMason):
    total = []
    for x in TheNumbersMason:
        if x == 'Not Found':
            total.append(float(0))
        else:
            print(x)
            total.append(float(x))

    totalPriceNumber.config(text="$" + str(sum(total)))

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
        #print(string)
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

def AddToListKey(event):
    item = itemInput.get()
    search_list.append(item)
    # print(search_list)
    addItem(item_list)
    return search_list

def AddToList():
    item = itemInput.get()
    search_list.append(item)
    # print(search_list)
    addItem(item_list)
    return search_list

def clearList():
    x = len(search_list)
    item_list.delete(0, len(search_list))
    search_list.clear()

#let user name the file and then update with the item in the list and save it
def saveList():
    f = open('NewFile.txt', 'w')
    y = 0
    total_price = getPrices()
    f.write("Item: \t")
    f.write("Price: \n")
    for x in search_list:
        item = x.split(":")
        print(item)
        f.write(item[0] + "-----")
        f.write("$" + item[1] + "\n\n")
        f.write("Total:\n$" + total_price[0])
        y+=1
    #f.write(search_list)

#update listbox after quantity
def listQupdate(index, total_price):
    #grab item from list
    step1 = search_list[index]
    #split to grab number
    step2 = step1.split(':')
    #insert new number
    step2.insert(1, total_price)
    step3 = step2[2]
    step2.remove(step3)
    step4 = str(step2[0]) + ':' + str(step2[1])
    search_list[index] = step4
    #update total price
    addAfterQuantity()

    #return list

#quantity func
def updateWithQuantity():
    item_quantity = {}
    quantity = quantityEntry.get()

    #gets selected listbox item
    for i in item_list.curselection():
        #print(item_list.get(i))
        item_quantity[i] = quantity
        #print(item_quantity)
    get_index = item_quantity.keys()
    for x in get_index:
        item_price = updatePriceWithQuantity(x)
        q_price = (float(item_price) * float(quantity))
        item = x
    listQupdate(item, q_price)
    #update search list with new price after quantity

websites = ['homedepot', 'lowes']
btn_color = '#04426E'
txt_color = 'white'
background_color = '#0b0c0b'
large_font = 32
btn_width = 7

app = Tk()
app.configure(bg='black')
#bind buttons
app.bind('<Return>', AddToListKey)

button_frame = Frame(app, bg=background_color)
button_frame.grid(row=4, column=1)

#1st column
item_label = Label(app, text='item', bg='black', fg=txt_color, font=large_font)
item_label.grid(row=0, column=0)

itemInput = Entry(app)
itemInput.grid(row=1, column=0)

#Goes in frame
addBtn = Button(button_frame, text='Add', command=AddToList, bg=btn_color, fg=txt_color, width=btn_width)
addBtn.grid(row=0, column=0)

# STARTS MAIN PROCESS
searchBtn = Button(button_frame, text='Search', command=startSearch, bg=btn_color, fg=txt_color, width=btn_width)
searchBtn.grid(row=1, column=0)

clearBtn = Button(button_frame, text="Clear", command=clearList, bg=btn_color, fg=txt_color, width=btn_width)
clearBtn.grid(row=2, column=0)

saveListBtn = Button(button_frame, text="Save", command=saveList, bg= btn_color, fg=txt_color, width=btn_width)
saveListBtn.grid(row=3, column=0)

quantityBtn = Button(button_frame, text="Quantity", command=updateWithQuantity, bg=btn_color, fg=txt_color)
quantityBtn.grid(row=4, column=0)

item_list = Listbox(app, font=large_font)
item_list.grid(row=4, column=0, pady=5)

totalPriceHeader = Label(app, text="Total: ", fg=txt_color, bg=background_color, font=large_font)
totalPriceHeader.grid(row=0, column=2)

totalPriceNumber = Label(app, text="$0", fg=txt_color, bg=background_color, font=large_font)
totalPriceNumber.grid(row=1, column=2)

quantityEntryLabel = Label(app, text="Quantity", fg=txt_color, bg=background_color, font=large_font)
quantityEntryLabel.grid(row=2, column=0)

quantityEntry = Entry(app)
quantityEntry.grid(row=3, column=0)


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