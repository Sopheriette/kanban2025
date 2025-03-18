from flask import Flask, render_template, request
import csv
import tkinter as tk
from tkinter import *

r = tk.Tk()
r.title('CO2 Programma')
r.configure(background='#A8DADC')
app = Flask(__name__)

months=['Janvāris', 'Februāris', 'Marts', 'Aprīlis', 'Maijs', 'Jūnijs', 'Jūlijs', 'Augusts', 'Septembris', 'Oktorbis', 'Novembris', 'Decembris']
days_in_month = {'Janvāris':31, 'Februāris':28, 'Marts':31, 'Aprīlis':30, 'Maijs':31, 'Jūnijs':30, 'Jūlijs':31, 'Augusts':31, 'Septembris':30, 'Oktorbis':31, 'Novembris':30, 'Decembris':31}
selected_month = None

def get_day_of_year(month, day):
    days_before_month = {
        'Janvāris': 0, 'Februāris': 31, 'Marts': 59, 'Aprīlis': 90,
        'Maijs': 120, 'Jūnijs': 151, 'Jūlijs': 181, 'Augusts': 212,
        'Septembris': 242, 'Oktobris': 273, 'Novembris': 303, 'Decembris': 334
    }
    return days_before_month[month] + day
    
def on_month_select(event):
    global selected_month
    selected_month_index = monthlist.curselection()
    if selected_month_index:
        selected_month = monthlist.get(selected_month_index)
        num_days = days_in_month[selected_month]
        mylist.delete(0, END)
        for i in range(1, num_days + 1):
            mylist.insert(END, f"{i} diena")
        mylist.pack(side=LEFT, fill=BOTH)
    else:
        answer.config(text="Vispirms izvēlējieties mēnesi!", fg='red')
        
def get_data_for_day(file_path, day):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['Day']) == day:
                return row
    return None

def select_day():
    global selected_month
    if not selected_month:
        answer.config(text="Vispirms izvēlējieties mēnesi!", fg='red')
        return
    selected_day_index = mylist.curselection()
    
    if not selected_day_index:  # If nothing is selected
        answer.config(text="Vispirms izvēlējieties dienu!", fg='red')
        return

    selected_day = int(mylist.get(selected_day_index[0]).split()[0])  # Get the selected day
    day_of_year = get_day_of_year(selected_month, selected_day)
    print(f"Dienuas numurs gadā: {day_of_year}")
    
    day_data = get_data_for_day(file_path, day_of_year)
    
    if day_data:
        co2_value = float(day_data['CO2'])
        if co2_value > 1000:
            answer.config(text=f"CO2 līmenis {selected_day}. dienā: {co2_value}\nLūdzu izvediniet istabu!", fg='red')
            button2.config(command=lambda: update_co2(co2_value))  # Pass the co2_value when the button is clicked
            button2.pack(anchor='e',padx=5, pady=5)
        else:
            answer.config(text=f"CO2 līmenis {selected_day}. dienā: {co2_value}", fg='green')
    else:
        answer.config(text="Nepadodas atrast datus par doto dienu!", fg='black')
def update_co2(co2_value):
    new_co2 = air_out(co2_value)
    answer.config(text=f"CO2 līmenis pēc ventilācijas: {new_co2}", fg='blue')
def air_out(co2_value):
    return co2_value - 500
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

frame=Frame(r,width=200,height=200,background="#457B9D")
frame.pack(padx=10,pady=10)

frame1 = Frame(frame, width=200, height=200)
frame1.pack(padx=10, pady=10,anchor='nw',side=LEFT,fill=X)
frame2 = Frame(frame, width=200, height=200)
frame2.pack(padx=10, pady=10,anchor='ne',side=LEFT,fill=X)
frame3 = Frame(frame, width=200, height=200,background='#457B9D')
frame3.pack(padx=10, pady=10,anchor='center')
frame4 = Frame(frame,width=200,height=600,background='#457B9D')
frame4.pack(padx=10,pady=10,anchor='center')

scrollbar1 = Scrollbar(frame1)
scrollbar1.pack(side=RIGHT, fill=Y)
monthlist = Listbox(frame1, yscrollcommand=scrollbar1.set,background="#1D3557",foreground="#F1FAEE",borderwidth=0, highlightthickness=0)
for m in months:
    monthlist.insert(END, m)
monthlist.pack(side=LEFT, fill=BOTH)
scrollbar1.config(command=monthlist.yview)
monthlist.bind("<ButtonRelease-1>", on_month_select)

scrollbar2 = Scrollbar(frame2)
scrollbar2.pack(side=RIGHT, fill=Y)
mylist = Listbox(frame2, yscrollcommand=scrollbar2.set,background="#1D3557",foreground="#F1FAEE",borderwidth=0, highlightthickness=0)
mylist.pack(side=LEFT, fill=BOTH)
scrollbar2.config(command=mylist.yview)

file_path = "CO2.csv"
selected_day_index = mylist.curselection()
co2_value=0
if not selected_day_index:
    print("No item selected!")
else:
    selected_day = int(mylist.get(selected_day_index).split()[0])
    day_of_year = get_day_of_year(selected_month, selected_day)
    day_data = get_data_for_day(file_path, day_of_year)
    co2_value = float(day_data['CO2'])
    print(f"Selected day: {selected_day}")

button = tk.Button(frame3, text='Izvelēties', width=25,background="#E63946",foreground="#F1FAEE",font='bold',command=select_day)
button.pack()
answer = tk.Label(frame4, text='', width=50, height=2, anchor='center')
answer.pack()
button2 = tk.Button(frame4, text='Parbaudīt vēlreiz', width=25, background="#E63946",foreground="#F1FAEE", anchor='center',font='bold', command=air_out(co2_value))

r.mainloop()
@app.route('/', methods=['GET', 'POST'])
def index():
    co2_value = None
    alert_message = None
    selected_month = request.form.get('month')
    selected_day = request.form.get('day')
    
    if selected_month and selected_day:
        day_of_year = get_day_of_year(selected_month, int(selected_day))
        day_data = get_data_for_day("CO2.csv", day_of_year)
        
        if day_data:
            co2_value = float(day_data['CO2'])
            if co2_value > 1000:
                alert_message = "Lūdzu izvediniet istabu!"
    
    return render_template('index.html', months=months, days_in_month=days_in_month, co2_value=co2_value, alert_message=alert_message)

if __name__ == '__main__':
    app.run(debug=True)