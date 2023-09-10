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

# Define the schedule file path
schedule_file_path = 'clinic_schedule.csv'

# Check if the schedule file already exists and delete it if it does
if os.path.exists(schedule_file_path):
    os.remove(schedule_file_path)

# Read the CSV files
data = read_csv_file('doctor_data.csv')
wishes = read_csv_file('doctor_wishes.csv')

# Define the start and end date for scheduling
start_date = datetime.strptime('2023-09-01', '%Y-%m-%d').date()
end_date = datetime.strptime('2023-09-30', '%Y-%m-%d').date()
delta = end_date - start_date
num_days = delta.days + 1

# Initialize variables
doctors = data['Doctor_Name'].tolist()
max_monthly_calls = num_days // len(doctors)
doctor_counters = {doctor: 0 for doctor in doctors}
monthly_counters = {doctor: 0 for doctor in doctors}
weekend_counters = {doctor: 0 for doctor in doctors}  # To keep track of weekend work
schedule = {}
previous_day_doctors = []
current_date = start_date
round_robin_index_open = 0
round_robin_index_closed = 0
round_robin_index_weekend = 0
call_type = 1

# Convert wishes to a dictionary of datetime objects
doctor_wishes_dict = {}
for index, row in wishes.iterrows():
    doc = row['Doctor_Name']
    date = datetime.strptime(row['Wish_Date'], '%Y-%m-%d').date()
    if doc in doctor_wishes_dict:
        doctor_wishes_dict[doc].append(date)
    else:
        doctor_wishes_dict[doc] = [date]

# Generate the schedule
for day in range(num_days):
    is_weekend = current_date.weekday() in [5, 6]
    num_doctors_needed = 3 if call_type == 0 else 1
    
    if call_type == 0:
        available_doctors_df = data[(~data['Doctor_Name'].isin(previous_day_doctors)) & (~data['Doctor_Name'].isin(doctor_wishes_dict.get(current_date, [])))]
    else:
        available_doctors_df = data[(data['Status'] == 'n') & (~data['Doctor_Name'].isin(previous_day_doctors)) & (~data['Doctor_Name'].isin(doctor_wishes_dict.get(current_date, [])))]

    available_doctors = available_doctors_df['Doctor_Name'].tolist()

    if len(available_doctors) >= num_doctors_needed:
        selected_doctors = []
        
        if is_weekend:
            for _ in range(num_doctors_needed):
                if round_robin_index_weekend >= len(available_doctors):
                    round_robin_index_weekend = 0
                selected_doctor = available_doctors[round_robin_index_weekend]
                selected_doctors.append(selected_doctor)
                round_robin_index_weekend += 1
        elif call_type == 0:
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
            if is_weekend:
                weekend_counters[selected_doctor] += 1  # Increment weekend counter
            if monthly_counters[selected_doctor] >= max_monthly_calls:
                available_doctors.remove(selected_doctor)
                
        schedule[current_date] = selected_doctors

    else:
        least_assigned_doctors = sorted(doctors, key=lambda x: (monthly_counters[x], weekend_counters[x]))[:num_doctors_needed]
        selected_doctors = least_assigned_doctors
        for selected_doctor in selected_doctors:
            doctor_counters[selected_doctor] = 1
            monthly_counters[selected_doctor] += 1
            if is_weekend:
                weekend_counters[selected_doctor] += 1  # Increment weekend counter

        schedule[current_date] = selected_doctors

    previous_day_doctors = selected_doctors
    current_date += timedelta(days=1)
    call_type = 1 - call_type

# Save the schedule and monthly counters to CSV files
schedule_df = pd.DataFrame(list(schedule.items()), columns=['Date', 'Doctors'])
schedule_df.to_csv(schedule_file_path, index=False)

monthly_counters_df = pd.DataFrame(list(monthly_counters.items()), columns=['Doctor_Name', 'Days_Worked'])
monthly_counters_df.to_csv('monthly_counters.csv', index=False)

# NEW: Save the weekend counters to a CSV file
weekend_counters_df = pd.DataFrame(list(weekend_counters.items()), columns=['Doctor_Name', 'Weekends_Worked'])
weekend_counters_df.to_csv('weekend_counters.csv', index=False)

# Display the schedule and monthly counters
for date, doctors in schedule.items():
    print(f"{date}: {', '.join(doctors)}")

print("Monthly counters for each doctor:")
for doctor, count in monthly_counters.items():
    print(f"{doctor}: {count} days, {weekend_counters[doctor]} weekends")
