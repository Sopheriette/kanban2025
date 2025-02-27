import csv


def get_data_for_day(file_path, day):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        found = False
        for row in reader:
            if int(row['Day']) == day:
                print(row)
                found = True
        if not found:
            print(f"nav datas par dienu {day}")


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
