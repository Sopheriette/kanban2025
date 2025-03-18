from flask import Flask, render_template, request
import csv

app = Flask(__name__)

months = ['Janvaris', 'Februaris', 'Marts', 'Aprīlis', 'Maijs', 'Jūnijs', 'Jūlijs', 'Augusts', 'Septembris', 'Oktorbis', 'Novembris', 'Decembris']
days_in_month = {'Janvaris': 31, 'Februaris': 28, 'Marts': 31, 'Aprīlis': 30, 'Maijs': 31, 'Jūnijs': 30, 'Jūlijs': 31, 'Augusts': 31, 'Septembris': 30, 'Oktorbis': 31, 'Novembris': 30, 'Decembris': 31}

def get_day_of_year(month, day):
    days_before_month = {
        'Janvaris': 0, 'Februaris': 31, 'Marts': 59, 'Aprīlis': 90,
        'Maijs': 120, 'Jūnijs': 151, 'Jūlijs': 181, 'Augusts': 212,
        'Septembris': 242, 'Oktorbis': 273, 'Novembris': 303, 'Decembris': 334
    }
    return days_before_month[month] + day

def get_data_for_day(file_path, day):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if int(row['Day']) == day:
                return row
    return None
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
