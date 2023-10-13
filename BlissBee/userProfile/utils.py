from datetime import datetime

def calculate_age(dob):
    # Convert the DOB string to a datetime object
    dob_date = datetime.strptime(str(dob), '%Y-%m-%d')
    
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the difference in years
    age_in_years = current_date.year - dob_date.year
    
    # Check if the birthday has already occurred this year
    if (current_date.month, current_date.day) < (dob_date.month, dob_date.day):
        age_in_years -= 1
    
    return age_in_years
