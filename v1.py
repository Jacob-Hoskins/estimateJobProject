
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from msilib.schema import ComboBox, ListBox
from multiprocessing.spawn import import_main_path
from bs4 import BeautifulSoup
from tkinter import *
import os
import time
from selenium import webdriver

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
            y=float(remove_item[1])
            prices.append(y)
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
        x += 1
    items_prices = getPrices()
    addAllPrices(items_prices)
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

def checkList():
    y=0
    for x in search_list:
        item = x.split(":")
        if 'Not Found' in item:
            del search_list[y]
        print(search_list)
        print(y)
    y+=1
    print(search_list)
    return search_list

#let user name the file and then update with the item in the list and save it
def saveList():
    #total = []
    f = open('Itemized.txt', 'w')
    checkList()
    total_price = getPrices()
    f.write("Item: \t")
    f.write("Price: \n")
    for x in search_list:
        item = x.split(":")
        f.write(item[0] + "-----")
        f.write("$" + item[1] + "\n\n")
        #total_price.append(item[1])

    total_price_items = sum(total_price)
    f.write("Total:\n$" + str(total_price_items))
    #f.write(search_list)
    f.write("\n*THIS IS AN ESTIMATE ITEM PRICES MAY CHANGE OR VARY FROM LOCATION TO LOCATION")

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

#switching pages
current_page = ["itemized"]

def itemizedPage():
    current_page.append("itemized")
    labor_frame.grid_forget()
    itemized.grid(row=0, column=0)
    return current_page

def laborCostPage():
    current_page.append("labor")
    itemized.grid_forget()
    labor_frame.grid(row=0, column=0)
    return current_page

#save labor file
def saveLaborFile():
    hours_list = []
    wages_list = []
    f = open("LaborCost.txt", 'w')
    f.write("Employee: \t\t")
    f.write("Wage: \t\t")
    f.write("Hours: \n")
    for x in employee_data:
        name = x["name"]
        wage = x["wage"]
        hours = x["hours"]
        f.write(name + "\t\t\t")
        f.write(wage + "\t\t\t")
        f.write(hours + "\n")
        hours_list.append(float(hours))
        wages_list.append(float(wage))

    total_hours = sum(hours_list)
    wages_total = sum(wages_list)
    total_labor = total_hours * wages_total

    f.write("\n\n\nTotal Hours: " + str(total_hours) + "\n")
    f.write("Total wages: $" + str(wages_total) + "\n")
    f.write("Total Labor Price: $" + str(total_labor) + "\n")
    f.write("*THIS IS AN ESTIMATE HOURS MAY BE AFFECTED BY TASK AT HAND")

def saveFile():
    print(current_page[-1])
    if current_page[-1] == 'labor':
        saveLaborFile()
    elif current_page[-1] == 'itemized':
        saveList()

websites = ['homedepot', 'lowes']
btn_color = '#04426E'
txt_color = 'white'
background_color = '#0b0c0b'
large_font = 32
btn_width = 7

app = Tk()
app.configure(bg=background_color)
app.title("Estimator")

#Pages
itemized = Frame(app, bg=background_color)
itemized.grid(row=0, column=0)

labor_frame = Frame(app, bg=background_color)

#bind buttons
app.bind('<Return>', AddToListKey)

#menu
menubar = Menu(app)
app.config(menu=menubar)

data = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=data)
data.add_command(label="Save file", command=saveFile)

file_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Pages", menu=file_menu)
file_menu.add_command(label="Itemized", command=itemizedPage)
file_menu.add_command(label="Labor", command=laborCostPage)
#file_menu.add_command(label="Item Estimate")

#TODO: add email at some point and add it back to the menu
"""
file_menu.add_command(label="Email")
"""
#ITEMIZED PAGE
button_frame = Frame(itemized, bg=background_color)
button_frame.grid(row=4, column=1)

#1st column
item_label = Label(itemized, text='item', bg=background_color, fg=txt_color, font=large_font)
item_label.grid(row=0, column=0)

itemInput = Entry(itemized)
itemInput.grid(row=1, column=0)

#Goes in frame
addBtn = Button(button_frame, text='Add', command=AddToList, bg=btn_color, fg=txt_color, width=btn_width)
addBtn.grid(row=0, column=0)

# STARTS MAIN PROCESS
searchBtn = Button(button_frame, text='Search', command=startSearch, bg=btn_color, fg=txt_color, width=btn_width)
searchBtn.grid(row=1, column=0)

clearBtn = Button(button_frame, text="Clear", command=clearList, bg=btn_color, fg=txt_color, width=btn_width)
clearBtn.grid(row=2, column=0)

quantityBtn = Button(button_frame, text="Quantity", command=updateWithQuantity, bg=btn_color, fg=txt_color)
quantityBtn.grid(row=3, column=0)

item_list = Listbox(itemized, font=large_font)
item_list.grid(row=4, column=0, pady=5)

totalPriceHeader = Label(itemized, text="Total: ", fg=txt_color, bg=background_color, font=large_font)
totalPriceHeader.grid(row=0, column=2)

totalPriceNumber = Label(itemized, text="$0", fg=txt_color, bg=background_color, font=large_font)
totalPriceNumber.grid(row=1, column=2)

quantityEntryLabel = Label(itemized, text="Quantity", fg=txt_color, bg=background_color, font=large_font)
quantityEntryLabel.grid(row=2, column=0)

quantityEntry = Entry(itemized)
quantityEntry.grid(row=3, column=0)

#LABOR PAGE SPECS
employees = ["Employees"]
employee_data=[]
breakdown_clicked = StringVar()

#LABOR PAGE FUNCTIONS
def updateInfo():
    all_cost = []
    all_hours = []
    for x in employee_data:
        employee_name = x["name"]
        employee_wage = x["wage"]
        employee_hours = x["hours"]

        total_price = float(employee_hours) * float(employee_wage)

        all_cost.append(total_price)
        all_hours.append(float(employee_hours))

        sum_cost=sum(all_cost)
        update_total_cost_text = "Total cost: $" + str(sum_cost)
        total_cost_label.config(text=update_total_cost_text)

        sum_hours=sum(all_hours)
        update_total_hours_text = "Total hours: " + str(sum_hours)
        total_hours_label.config(text=update_total_hours_text)

def updateBreakdown(wage, hours):
    total_price = float(wage) * float(hours)
    updated_text = ("Total price: $" + str(total_price))
    total_price_label.config(text=updated_text)
    wage_updated_text = ("Wage: $" + str(wage))
    breakdown_wage_label.config(text=wage_updated_text)
    hours_updated_text = ("Hours: " + str(hours))
    breakdown_hours_label.config(text=hours_updated_text)

def displaySelected():
    name = breakdown_clicked.get()
    for x in employee_data:
        if x["name"] == name:
            wage = x["wage"]
            hours = x["hours"]
            updateBreakdown(wage, hours)

def updateDropdown():
    updateInfo()
    menu = breakdown_selection["menu"]
    menu.delete(0, "end")
    for string in employees:
        menu.add_command(label=string, command=lambda value=string: breakdown_clicked.set(value))

def saveEmployeeInfo(info):
    employee_data.append(info)
    employee_name = info["name"]
    employees.append(employee_name)
    updateDropdown()
    return employee_data, employees

def addEmployeeInfo():
    employee_name = employee_name_entry.get()
    employee_wage = employee_hourly_pay_entry.get()
    employee_hours = employee_estimated_hours_entry.get()

    employee_dict = {"name":employee_name, "wage":employee_wage, "hours":employee_hours}
    saveEmployeeInfo(employee_dict)


#LABOR PAGE

employee_name_label = Label(labor_frame, text="Name", fg=txt_color, bg=background_color, font=large_font)
employee_name_label.grid(row=0, column=0)

employee_name_entry = Entry(labor_frame)
employee_name_entry.grid(row=1, column=0)

employee_hourly_pay_label = Label(labor_frame, text="Hourly Wage", fg=txt_color, bg=background_color, font=large_font)
employee_hourly_pay_label.grid(row=2, column=0)

employee_hourly_pay_entry = Entry(labor_frame)
employee_hourly_pay_entry.grid(row=3, column=0)

employee_estimated_hours_label = Label(labor_frame, text="Estimated Hours", fg=txt_color, bg=background_color, font=large_font)
employee_estimated_hours_label.grid(row=4, column=0)

employee_estimated_hours_entry = Entry(labor_frame)
employee_estimated_hours_entry.grid(row=5, column=0)

save_employee_info = Button(labor_frame, text="Add", bg=btn_color, fg=txt_color, width=btn_width, command=addEmployeeInfo)
save_employee_info.grid(row=6, column=0)

select_employee_button = Button(labor_frame, text="Select", bg=btn_color, fg=txt_color, width=btn_width, command=displaySelected)
select_employee_button.grid(row=7, column=0)

total_hours_label = Label(labor_frame, text="Total hours:", bg=background_color, fg=txt_color, font=large_font)
total_hours_label.grid(row=0, column=1)

total_cost_label = Label(labor_frame, text="total cost:", bg=background_color, fg=txt_color, font=large_font)
total_cost_label.grid(row=1, column=1)

breakdown_label = Label(labor_frame, text="Breakdown", bg=background_color, fg=txt_color, font=large_font)
breakdown_label.grid(row=2, column=1)

breakdown_selection = OptionMenu(labor_frame, breakdown_clicked, *employees)
breakdown_selection.grid(row=3, column=1)
breakdown_selection.config(bg=background_color, fg=txt_color, highlightthickness=0)

breakdown_hours_label = Label(labor_frame, text="Hours:", bg=background_color, fg=txt_color, font=large_font)
breakdown_hours_label.grid(row=4, column=1)

breakdown_wage_label = Label(labor_frame, text="Wage: $", bg=background_color, fg=txt_color, font=large_font)
breakdown_wage_label.grid(row=5, column=1)

total_price_label = Label(labor_frame, text="Total price: $", bg=background_color, fg=txt_color, font=large_font)
total_price_label.grid(row=6, column=1)

app.mainloop()