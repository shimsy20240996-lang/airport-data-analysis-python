"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: 20240996
 4. Date: 2025/10/30
****************************************************************************
"""

from graphics import *   
import csv
import math


data_list = []   # data_list An empty list to load and hold data from csv file


def load_csv(CSV_chosen):
    """
    Load csv file by name into the global list "data_list".
    Clears data_list first so repeated runs don't accumulate data.
    """
    data_list.clear()
    try:
        with open(CSV_chosen, 'r') as file:
            csvreader = csv.reader(file)
            header = next(csvreader)
            for row in csvreader:
                data_list.append(row)
    except FileNotFoundError:
        raise



airports = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

destination_names = airports.copy()  

valid_airlines = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}

# ---------- Task A: Input Validation ----------
def get_city_code():
    valid_airports = list(airports.keys())

    while True:
        code = input("Please enter a three-letter city code: ").strip().upper()

        if len(code) != 3:
            print("Wrong code length - please enter a three-letter city code")

        elif code not in valid_airports:
            print("Unavailable city code - please enter a valid city code")

        else:
            return code



def get_year():
    while True:
        year = input("Please enter the year required in the format YYYY: ").strip()

        if not year.isdigit() or len(year) != 4:
            print("Wrong data type - please enter a four-digit year value")

        elif not (2000 <= int(year) <= 2025):
            print("Out of range - please enter a value from 2000 to 2025")

        else:
            return year



# ---------- Task B + C: Processing outcomes and saving results ----------
def process_outcomes(selected_data_file, full_name, year):
    
    total_flights = len(data_list)

   
    terminal_2_count = 0
    for row in data_list:
        if row[8] == "2":
            terminal_2_count += 1

    
    under_600 = 0
    for row in data_list:
        try:
            if int(row[5]) < 600:
                under_600 += 1
        except ValueError:
            pass  
    
    air_france_count = 0
    for row in data_list:
        airline = row[1][:2]
        if airline == "AF":
            air_france_count += 1

   
    temp_below_15 = 0
    for row in data_list:
        weather = row[10]
        try:
            temp_str = weather.split("°")[0]
            temp = int(temp_str)
            if temp < 15:
                temp_below_15 += 1
        except Exception:
            pass

   
    ba_count = 0
    for row in data_list:
        airline = row[1][:2]
        if airline == "BA":
            ba_count += 1

    ba_per_hour = round(ba_count / 12, 2) if total_flights >= 0 else 0
    ba_percentage = round((ba_count / total_flights) * 100, 2) if total_flights > 0 else 0.0

    
    delayed_af = 0
    for row in data_list:
        airline = row[1][:2]
        if airline == "AF":
            scheduled = row[2]
            actual = row[3]
            if actual != scheduled:
                delayed_af += 1

    af_delayed_percentage = round((delayed_af / air_france_count) * 100, 2) if air_france_count > 0 else 0.0

   
    rain_hours = 0
    for row in data_list:
        weather = row[10].lower()
        if "rain" in weather:
            rain_hours += 1

   
    dest_counts = {}
    for row in data_list:
        dest = row[4]
        dest_counts[dest] = dest_counts.get(dest, 0) + 1

    if dest_counts:
        min_value = min(dest_counts.values())
        least_common_codes = [code for code, count in dest_counts.items() if count == min_value]
        least_common_names = [destination_names.get(x, x) for x in least_common_codes]
    else:
        least_common_names = []

    # --------- Print results to shell ---------
    print("\n" + "*" * 75)
    print(f"File {selected_data_file} selected - Planes departing {full_name} {year}")
    print("*" * 75 + "\n")

    print(f"The total number of flights from this airport was {total_flights}")
    print(f"The total number of flights departing Terminal Two was {terminal_2_count}")
    print(f"The total number of departures on flights under 600 miles was {under_600}")
    print(f"There were {air_france_count} Air France flights from this airport")
    print(f"There were {temp_below_15} flights departing in temperatures below 15 degrees")
    print(f"There was an average of {ba_per_hour} British Airways flights per hour from this airport")
    print(f"British Airways planes made up {ba_percentage}% of all departures")
    print(f"{af_delayed_percentage}% of Air France departures were delayed")
    print(f"There were {rain_hours} hours in which rain fell")
    print(f"The least common destinations are {least_common_names}")

    # --------- Task C: Save results to results.txt (append) ---------
    with open("results.txt", "a") as file:
        file.write("\n" + "*" * 75 + "\n")
        file.write(f"File {selected_data_file} selected - Planes departing {full_name} {year}\n")
        file.write("*" * 75 + "\n")

        file.write(f"The total number of flights from this airport was {total_flights}\n")
        file.write(f"The total number of flights departing Terminal Two was {terminal_2_count}\n")
        file.write(f"The total number of departures on flights under 600 miles was {under_600}\n")
        file.write(f"There were {air_france_count} Air France flights from this airport\n")
        file.write(f"There were {temp_below_15} flights departing in temperatures below 15 degrees\n")
        file.write(f"There was an average of {ba_per_hour} British Airways flights per hour from this airport\n")
        file.write(f"British Airways planes made up {ba_percentage}% of all departures\n")
        file.write(f"{af_delayed_percentage}% of Air France departures were delayed\n")
        file.write(f"There were {rain_hours} hours in which rain fell\n")
        file.write(f"The least common destinations are {least_common_names}\n")
        file.write("\n")


# ---------- Task D: Histogram ----------
def get_airline_code():
    while True:
        airline_code = input("Enter a two-character Airline code to plot histogram: ").strip().upper()
        if airline_code not in valid_airlines:
            print("Unavailable Airline code please try again.")
            continue
        return airline_code


def plot_histogram(code, selected_data_file, full_name, year):
    airline_full = valid_airlines.get(code, code)

    # Count flights per hour
    hour_counts = [0] * 12
    for row in data_list:
        airline = row[1][:2]
        if airline == code:
            try:
                hour = int(row[2].split(":")[0])
                hour_counts[hour] += 1
            except Exception:
                pass

    max_value = max(hour_counts) if hour_counts else 0

   
    win = GraphWin(f"{airline_full} - {full_name} {year}", 900, 600)
    win.setBackground("white")

   
    title = Text(Point(450, 30), f"Departures by Hour - {airline_full} ({full_name} {year})")
    title.setSize(14)
    title.draw(win)

    
    start_x = 180
    start_y = 70
    bar_height = 30
    gap = 12

    
    for hour in range(12):
        count = hour_counts[hour]

       
        bar_max_width = 560
        bar_width = 0 if max_value == 0 else (count / max_value) * bar_max_width

       
        y1 = start_y + (hour * (bar_height + gap))
        y2 = y1 + bar_height

       
        rect = Rectangle(Point(start_x, y1), Point(start_x + bar_width, y2))
        rect.setFill("green")
        rect.setOutline("black")
        rect.draw(win)

      
        hour_label = Text(Point(90, y1 + bar_height / 2), f"{hour:02}:00")
        hour_label.draw(win)

        
        count_label = Text(Point(start_x + bar_width + 25, y1 + bar_height / 2), str(count))
        count_label.draw(win)

    
    close_msg = Text(Point(450, 570), "Click anywhere in the window to close")
    close_msg.setSize(12)
    close_msg.draw(win)

    win.getMouse()
    win.close()


# ---------- Task E: Main loop ----------
def main():
    while True:
        print("\n--- Plane Analysis System ---")
        
        airport_code = get_city_code()
        full_name = airports[airport_code]
        year = get_year()

        
        selected_data_file = f"{airport_code}{year}.csv"
        try:
            load_csv(selected_data_file)
        except FileNotFoundError:
            print(f"File {selected_data_file} not found in the same folder as this program.")
            print("Please make sure the correct CSV file is available and try again.\n")
            continue

        
        process_outcomes(selected_data_file, full_name, year)

      
        airline_code = get_airline_code()
        plot_histogram(airline_code, selected_data_file, full_name, year)

        
        while True:
            choice = input("\nDo you want to select a new data file? Y/N: ").strip().upper()
            if choice == "Y":
                break
            elif choice == "N":
                print("Thank you. End of run.")
                return
            else:
                print("Invalid input. Please enter Y or N.")

if __name__ == "__main__":
    main()
