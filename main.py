import tkinter as t
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sqlDB import Database
import datetime as dt
import pymysql as py

def create_database():
    connection = py.connect(host='localhost', user='root', password='12345')
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ExpenseTracker")
    connection.close()

# Create the database if it doesn't exist
create_database()

# Database Object
data = Database(db='ExpenseTracker')

if data.conn is None:
    print("Failed to connect to the database.")
    exit(1)

count = 0
selected_rowid = 0

def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())
    refreshData()

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, "end")
    transaction_date.delete(0, 'end')

def fetchRecords():
    f = data.fetchRecord('SELECT id, item_name, item_price, purchase_date FROM expense_record')
    global count
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData)

def fetch_records(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass

def update_record():
    global selected_rowid

    selected = tv.focus()

    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(selected_rowid, namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)

    clearEntries()
    refreshData()

def totalBalance():
    f = data.fetchRecord("SELECT SUM(item_price) FROM expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance', f"Total Expense: {j} \nBalance Remaining: {5000 - j}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetchRecords()

def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

ws = Tk()
ws.title('Expense Tracker')
ws.geometry('600x400')

f = ('Times new roman', 14)
amtvar = IntVar()
dopvar = StringVar()
namevar = StringVar()

f2 = Frame(ws)
f2.pack()

f1 = Frame(ws, padx=10, pady=10)
f1.pack(expand=True, fill=BOTH)

Label(f1, text='ITEM NAME', font=f).grid(row=0, column=0, sticky=W)
Label(f1, text='ITEM PRICE', font=f).grid(row=1, column=0, sticky=W)
Label(f1, text='PURCHASE DATE', font=f).grid(row=2, column=0, sticky=W)

item_name = Entry(f1, font=f)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

cur_date = Button(f1, text='Current Date', font=f, bg='#04C4D9', command=setDate, width=15)
submit_btn = Button(f1, text='Save Record', font=f, command=saveRecord, bg='#42602D', fg='white')
clr_btn = Button(f1, text='Clear Entry', font=f, command=clearEntries, bg='#D9B036', fg='white')
quit_btn = Button(f1, text='Exit', font=f, command=ws.quit, bg='#D33532', fg='white')
total_bal = Button(f1, text='Total Balance', font=f, bg='#486966', fg='white', command=totalBalance)
total_spent = Button(f1, text='Total Spent', font=f, fg='white', command=totalBalance)
update_btn = Button(f1, text='Update', bg='#C2BB00', command=update_record, fg='white', font=f)
del_btn = Button(f1, text='Delete', bg='#BD2A2E', fg='white', command=deleteRow, font=f)

cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))

tv = ttk.Treeview(f2, selectmode='browse', columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side="left")

tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

ws.mainloop()
