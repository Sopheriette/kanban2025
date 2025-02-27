import csv
import tkinter as tk
from tkinter import *

r = tk.Tk()
r.title('CO2 Programma')

months=['Janvaris', 'Februaris', 'Marts', 'Aprīlis', 'Maijs', 'Jūnijs', 'Jūlijs', 'Augusts', 'Septembris', 'Oktorbis', 'Novembris', 'Decembris']
days_in_month = {'Janvaris':31, 'Februaris':28, 'Marts':31, 'Aprīlis':30, 'Maijs':31, 'Jūnijs':30, 'Jūlijs':31, 'Augusts':31, 'Septembris':30, 'Oktorbis':31, 'Novembris':30, 'Decembris':31}
selected_month = None

def get_day_of_year(month, day):
    days_before_month = {
        'Janvāris': 0, 'Februāris': 31, 'Marts': 59, 'Aprīlis': 90,
        'Maijs': 120, 'Jūnijs': 151, 'Jūlijs': 181, 'Augusts': 212,
        'Septembris': 243, 'Oktobris': 273, 'Novembris': 304, 'Decembris': 334
    }
    return days_before_month[month] + day
def on_month_select(event):
    global selected_month
    selected_month_index = monthlist.curselection()
    if selected_month_index:  # Ensure a valid selection is made
        selected_month = monthlist.get(selected_month_index)
        num_days = days_in_month[selected_month]
        mylist.delete(0, END)
        for i in range(1, num_days + 1):
            mylist.insert(END, f"{i} diena")
        mylist.pack(side=LEFT, fill=BOTH)
    else:
        answer.config(text="Please select a month first!", fg='red')
def get_data_for_day(file_path, day):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['Day']) == day:
                return row
        return None
def select_day():
    global selected_month  # Access the global selected_month variable
    if not selected_month:
        answer.config(text="Please select a month first!", fg='red')
        return
    
    selected_day_index = mylist.curselection()
    if not selected_day_index:
        answer.config(text="Please select a day!", fg='red')
        return
    selected_day = int(mylist.get(selected_day_index).split()[0])
    
    day_of_year = get_day_of_year(selected_month, selected_day)
    print(f"Day number in the year: {day_of_year}")
    
    file_path = "CO2.csv"
    day_data = get_data_for_day(file_path, day_of_year)
    
    if day_data:
        co2_value = float(day_data['CO2'])
        if co2_value > 1000:
            answer.config(text=f"CO2 level for day {selected_day}: {co2_value} (High!)", fg='red')
        else:
            answer.config(text=f"CO2 level for day {selected_day}: {co2_value}", fg='green')
    else:
        answer.config(text="No data found for selected day", fg='black')
def get_high_co2_data(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        found = False
        for row in reader:
            if float(row['CO2']) > 400:
                print(row)
                found = True
        if not found:
            print("av datas par to kur co2 > 1000")
    if __name__ == "__main__":
        file_path = "CO2.csv"
        choice = input("izvelies darbibu: (1) informacija par dienu, (2) CO2 > 1000: ")
    if choice == "1":
        day = int(input("Dienas numurs: "))
        get_data_for_day(file_path, day)
    elif choice == "2":
        get_high_co2_data(file_path)
    else:
        print("nope")
#if __name__ == "__main__":
#    file_path = "CO2.csv"
#    choice = input("izvelies darbibu: (1) informacija par dienu, (2) CO2 > 1000: ")
#
#    if choice == "1":
#        day = int(input("Dienas numurs: "))
#        get_data_for_day(file_path, day)
#    elif choice == "2":
#        get_high_co2_data(file_path)
#    else:
#        print("nope")
frame1 = Frame(r, width=200, height=200)
frame1.pack(padx=10, pady=10)
frame2 = Frame(r, width=200, height=200)
frame2.pack(padx=10, pady=10)
frame3 = Frame(r, width=200, height=200)
frame3.pack(padx=10, pady=10)
frame4 = Frame(r,width=200,height=600)
frame4.pack(padx=10,pady=10)

scrollbar1 = Scrollbar(frame1)
scrollbar1.pack(side=RIGHT, fill=Y)
monthlist = Listbox(frame1, yscrollcommand=scrollbar1.set)
for m in months:
    monthlist.insert(END, m)
monthlist.pack(side=LEFT, fill=BOTH)
scrollbar1.config(command=monthlist.yview)
monthlist.bind("<ButtonRelease-1>", on_month_select)

scrollbar2 = Scrollbar(frame2)
scrollbar2.pack(side=RIGHT, fill=Y)
mylist = Listbox(frame2, yscrollcommand=scrollbar2.set)
mylist.pack(side=LEFT, fill=BOTH)
scrollbar2.config(command=mylist.yview)

button = tk.Button(frame3, text='Izvelēties', width=25,command=select_day)
button.pack()

answer = tk.Label(frame4, text='', width=50, height=2, anchor='w')
answer.pack()

r.mainloop()