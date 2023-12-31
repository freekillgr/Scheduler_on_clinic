import os
import pandas as pd
from datetime import datetime, timedelta

def read_csv_file(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: {file_path} is empty.")
        exit(1)
    except pd.errors.ParserError:
        print(f"Error: Could not parse {file_path}.")
        exit(1)

def get_unavailable_dates(row):
    start_date = datetime.strptime(row['Wish_Start_Date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(row['Wish_End_Date'], '%Y-%m-%d').date()
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]

# Ask the user for input
start_date_input = input("Enter the start date (YYYY-MM-DD): ")
end_date_input = input("Enter the end date (YYYY-MM-DD): ")
call_type_input = input("Enter the call type to start with (0 for open, 1 for closed): ")
doctor_data_file_path = input("Enter the location of the doctor_data.csv file: ")
doctor_wishes_file_path = input("Enter the location of the doctor_wishes.csv file: ")
output_directory = input("Enter the directory where you want to save the output files: ")

# Validate user input and directory
try:
    start_date = datetime.strptime(start_date_input, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_input, '%Y-%m-%d').date()
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit(1)

if call_type_input not in ['0', '1']:
    print("Invalid call type. Please enter 0 for open or 1 for closed.")
    exit(1)

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

call_type = int(call_type_input)
schedule_file_path = os.path.join(output_directory, 'schedule.csv')
monthly_counter_file_path = os.path.join(output_directory, 'monthly_counters.csv')
weekend_counter_file_path = os.path.join(output_directory, 'weekend_counters.csv')

# Read the CSV files
data = read_csv_file(doctor_data_file_path)
wishes = read_csv_file(doctor_wishes_file_path)

# Convert wishes to a dictionary of datetime objects
doctor_wishes_dict = {}
for index, row in wishes.iterrows():
    doc = row['Doctor_Name']
    unavailable_dates = get_unavailable_dates(row)
    if doc in doctor_wishes_dict:
        doctor_wishes_dict[doc].extend(unavailable_dates)
    else:
        doctor_wishes_dict[doc] = unavailable_dates

# Define the start and end date for scheduling (now based on user input)
delta = end_date - start_date
num_days = delta.days + 1

# Initialize variables
doctors = data['Doctor_Name'].tolist()
max_monthly_calls = num_days // len(doctors)
doctor_counters = {doctor: 0 for doctor in doctors}
monthly_counters = {doctor: 0 for doctor in doctors}
weekend_counters = {doctor: 0 for doctor in doctors}
last_weekend_worked = {doctor: None for doctor in doctors}
schedule = {}
previous_day_doctors = []
current_date = start_date
round_robin_index_open = 0
round_robin_index_closed = 0

# Generate the schedule
for day in range(num_days):
    is_weekend = current_date.weekday() >= 5  # True if it's Saturday or Sunday

    num_doctors_needed = 3 if call_type == 0 else 1

    # Determine available doctors based on call type and other conditions
    if call_type == 0:
        available_doctors_df = data[(~data['Doctor_Name'].isin(previous_day_doctors)) & (~data['Doctor_Name'].isin(doctor_wishes_dict.get(current_date, [])))]
    else:
        available_doctors_df = data[(data['Status'] == 'n') & (~data['Doctor_Name'].isin(previous_day_doctors)) & (~data['Doctor_Name'].isin(doctor_wishes_dict.get(current_date, [])))]

    available_doctors = available_doctors_df['Doctor_Name'].tolist()

    # Filter out doctors who worked the last weekend, if it's a weekend
    if is_weekend:
        available_doctors = [doc for doc in available_doctors if last_weekend_worked[doc] != current_date - timedelta(days=7)]

    if len(available_doctors) >= num_doctors_needed:
        selected_doctors = []
        
        if call_type == 0:
            for _ in range(num_doctors_needed):
                if round_robin_index_open >= len(available_doctors):
                    round_robin_index_open = 0
                selected_doctor = available_doctors[round_robin_index_open]
                selected_doctors.append(selected_doctor)
                round_robin_index_open += 1
        else:
            for _ in range(num_doctors_needed):
                if round_robin_index_closed >= len(available_doctors):
                    round_robin_index_closed = 0
                selected_doctor = available_doctors[round_robin_index_closed]
                selected_doctors.append(selected_doctor)
                round_robin_index_closed += 1

        for selected_doctor in selected_doctors:
            doctor_counters[selected_doctor] = 1
            monthly_counters[selected_doctor] += 1
            if monthly_counters[selected_doctor] >= max_monthly_calls:
                available_doctors.remove(selected_doctor)

        # Update last_weekend_worked and weekend_counters if it's a weekend
        if is_weekend:
            for selected_doctor in selected_doctors:
                last_weekend_worked[selected_doctor] = current_date
                weekend_counters[selected_doctor] += 1
                
        schedule[current_date] = selected_doctors
    
    else:
        least_assigned_doctors = sorted(doctors, key=lambda x: monthly_counters[x])[:num_doctors_needed]
        selected_doctors = least_assigned_doctors
        for selected_doctor in selected_doctors:
            doctor_counters[selected_doctor] = 1
            monthly_counters[selected_doctor] += 1
        schedule[current_date] = selected_doctors

    # Update the list of doctors who worked on the previous day's call
    previous_day_doctors = selected_doctors

    # Move to the next day and toggle call type
    current_date += timedelta(days=1)
    call_type = 1 - call_type

# Save the schedule and monthly counters to CSV files
schedule_df = pd.DataFrame(list(schedule.items()), columns=['Date', 'Doctors'])
schedule_df.to_csv(schedule_file_path, index=False)

monthly_counters_df = pd.DataFrame(list(monthly_counters.items()), columns=['Doctor_Name', 'Days_Worked'])
monthly_counters_df.to_csv(monthly_counter_file_path, index=False)

# Save weekend counters to a CSV
weekend_counters_df = pd.DataFrame(list(weekend_counters.items()), columns=['Doctor_Name', 'Weekends_Worked'])
weekend_counters_df.to_csv(weekend_counter_file_path, index=False)

# Display the schedule, monthly counters, and weekend counters
for date, doctors in schedule.items():
    print(f"{date}: {', '.join(doctors)}")

print("Monthly counters for each doctor:")
for doctor, count in monthly_counters.items():
    print(f"{doctor}: {count} days")

print("Weekend counters for each doctor:")
for doctor, count in weekend_counters.items():
    print(f"{doctor}: {count} weekends")
