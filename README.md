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
