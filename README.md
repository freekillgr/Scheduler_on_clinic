# Scheduler_on_clinic
A scheduler for doctors with factor like wish list or status .
     ach doctor's status (either available for all types of calls or only for closed calls)
    Each doctor's preferences ("wishes") for specific dates they'd prefer not to work
    A round-robin assignment to ensure all doctors are scheduled fairly
    A maximum number of days a doctor can be scheduled in a month

The code also generates a CSV file that saves the final schedule and another that stores the number of days each doctor worked.

Here are some key points about each part of the script:

    Reading CSV Files: The function read_csv_file() reads a given CSV file into a DataFrame, handling various types of errors like "File not found", "Empty file", and "Parse error".

    Initializations:
        schedule_file_path is the output file for the generated schedule.
        data and wishes DataFrames store the information read from doctor_data.csv and doctor_wishes.csv, respectively.
        The date range for the schedule is defined.
        Doctor names, counters, and other variables are initialized.

    Wishes Conversion: The wishes DataFrame is converted to a dictionary (doctor_wishes_dict) to make it easier to check against while generating the schedule.

    Generate Schedule: This is the core logic, where the schedule is generated based on the rules.
        It uses a round-robin index for both open and closed calls.
        The round-robin index ensures that each doctor is picked sequentially from the list of available doctors.
        The selected doctors are added to the schedule and their counters are updated.

    Saving and Displaying Results: Finally, the generated schedule and the monthly counters are saved to CSV files, and some of this information is printed to the console.

Guide to Using the Doctor Scheduling Script
Overview

The Doctor Scheduling Script is designed to create a month-long schedule for doctors working in a clinic. The script takes into account several parameters such as each doctor's availability, the type of call (open or closed), and any specific days the doctors wish to have off. The schedule is generated in a fair manner using a round-robin algorithm.
Input Data Requirements

You'll need two CSV files:

    doctor_data.csv: This file should have two columns:
        Doctor_Name: The names of the doctors.
        Status: Indicates whether a doctor is available for all calls (a) or just closed calls (n).

Doctor_Name,Status
Alice,a
Bob,n
Carol,a

doctor_wishes.csv: This file should also have two columns:

    Doctor_Name: The names of the doctors (should match the names in doctor_data.csv).
    Wish_Date: Dates that doctors wish to have off, formatted as YYYY-MM-DD.

Doctor_Name,Wish_Date
Alice,2023-09-10
Bob,2023-09-15
Carol,2023-09-20

How to Run the Script

    Place the doctor_data.csv and doctor_wishes.csv files in the same directory as the script.

    Run the script by executing it in a Python environment where the required libraries (pandas, os, datetime) are installed.

    After running the script, you will find a new file named clinic_schedule.csv generated in the same directory. This file contains the schedule for the month.

    You will also find a file named monthly_counters.csv which indicates how many days each doctor has been scheduled for.

Output Data
clinic_schedule.csv

    Date: The date for which the schedule has been generated, formatted as YYYY-MM-DD.
    Doctors: A list of doctor names who are scheduled for that day.

Date,Doctors
2023-09-01,"['Alice', 'Carol']"
2023-09-02,"['Bob']"
...

monthly_counters.csv

    Doctor_Name: The name of the doctor.
    Days_Worked: The number of days the doctor is scheduled for the month.

Doctor_Name,Days_Worked
Alice,10
Bob,9
Carol,10

Guide to Using the Doctor Scheduling Script
Overview

The Doctor Scheduling Script is designed to create a month-long schedule for doctors working in a clinic. The script takes into account several parameters such as each doctor's availability, the type of call (open or closed), and any specific days the doctors wish to have off. The schedule is generated in a fair manner using a round-robin algorithm.
Input Data Requirements

You'll need two CSV files:

    doctor_data.csv: This file should have two columns:
        Doctor_Name: The names of the doctors.
        Status: Indicates whether a doctor is available for all calls (a) or just closed calls (n).

    Example:

    css

Doctor_Name,Status
Alice,a
Bob,n
Carol,a

doctor_wishes.csv: This file should also have two columns:

    Doctor_Name: The names of the doctors (should match the names in doctor_data.csv).
    Wish_Date: Dates that doctors wish to have off, formatted as YYYY-MM-DD.

Example:

    Doctor_Name,Wish_Date
    Alice,2023-09-10
    Bob,2023-09-15
    Carol,2023-09-20

How to Run the Script

    Place the doctor_data.csv and doctor_wishes.csv files in the same directory as the script.

    Run the script by executing it in a Python environment where the required libraries (pandas, os, datetime) are installed.

    After running the script, you will find a new file named clinic_schedule.csv generated in the same directory. This file contains the schedule for the month.

    You will also find a file named monthly_counters.csv which indicates how many days each doctor has been scheduled for.

Output Data
clinic_schedule.csv

    Date: The date for which the schedule has been generated, formatted as YYYY-MM-DD.
    Doctors: A list of doctor names who are scheduled for that day.

Example:

css

Date,Doctors
2023-09-01,"['Alice', 'Carol']"
2023-09-02,"['Bob']"
...

monthly_counters.csv

    Doctor_Name: The name of the doctor.
    Days_Worked: The number of days the doctor is scheduled for the month.

Example:

Doctor_Name,Days_Worked
Alice,10
Bob,9
Carol,10

Notes

    The script uses a round-robin algorithm to distribute the workdays as evenly as possible among the doctors.

    Doctors will not be scheduled for two consecutive days to ensure they have time to rest.

    Doctors' wishes for days off are respected as much as possible.

That's it! Now you should have a fair and balanced schedule for your clinic.
