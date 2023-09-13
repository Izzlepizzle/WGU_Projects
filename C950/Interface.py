from datetime import datetime, time, date, timedelta

# The interface class
# Used for getting user input and storing it into an easily accessible object
class interface:
    def __init__(self):
        self.id = 0
        self.time = datetime.today()
        self.format = "%H:%M:%S"

    # sets the id attribute with a user inputted integer
    # Throws an error if its not an int
    def set_id(self):
        try:
            self.id = int(input("Please enter a package id:  "))
        except:
            print("Invalid Input")

    # Sets the time attribute with a user inputted time
    # Throws an error if the string cannot be converted to a time
    def set_time(self):
        string = input("Please enter a time from 8:00am to 6:00pm in 00:00:00 format:  ")
        try:
            # Converts the string to a date time object
            self.time = datetime.strptime(string, self.format)
            self.time = datetime.combine(date.today(), self.time.time())
        except Exception as e:
            print("Invalid Input.")
            print(e)

