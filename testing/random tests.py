#Shoutout naar ChatGPT

""" from datetime import datetime, timedelta

def get_next_weekday(current_date, target_weekday):
    days_until_target = (target_weekday - current_date.weekday() + 7) % 7
    next_weekday = current_date + timedelta(days=days_until_target)
    return next_weekday

# Example: Find the date of the next Wednesday from the current date
current_date = datetime.now()
next_wednesday = get_next_weekday(current_date, target_weekday=2)  # 0=Monday, 1=Tuesday, ..., 6=Sunday

print("Next Wednesday:", next_wednesday.strftime("%Y-%m-%d")) """



""" days_of_week_dutch = ['maandag', 'woensdag', 'donderdag', 'dinsdag', 'vrijdag', 'zaterdag', 'zondag']

# Define a dictionary mapping Dutch day names to numerical values
dutch_to_numeric = {'maandag': 0, 'dinsdag': 1, 'woensdag': 2, 'donderdag': 3, 'vrijdag': 4, 'zaterdag': 5, 'zondag': 6}

# Define a custom key function to map Dutch days to numerical values
def custom_sort_key_dutch(day):
    return dutch_to_numeric[day]

# Sort the list using the custom key function
sorted_days_dutch = sorted(days_of_week_dutch, key=custom_sort_key_dutch)

print(sorted_days_dutch) """