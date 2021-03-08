import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
zz
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!!!!')
    # TO DO: get user input for city (chicago, new york city, w ashington). HINT: Use a while loop to handle invalid inputs
    while True:
        city_choose = input("Would you like to see data from Chicago, New York or Washington? \n")
        cities = ["new york", "chicago", "washington"]
        if city_choose.lower() in cities:
            city = city_choose.lower()
            break
        else:
            print("Please select a correct city \n")
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        filter_choose = input("Would you like to filter the data by month, day or not at all? Type \"none\" for no time filter\n")
        if filter_choose.lower() == "month":
            months = ['january', 'february', 'march', 'april', 'may', 'june']
            while True:
                choose_month = input("Which month? (from January to June) \n")
                if choose_month.lower() in months:
                    month = choose_month.lower()
                    day = "all"
                    break
                else:
                    print("you did not choose correctly. \n")
            break
        elif filter_choose.lower() == "day":
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            while True:
                choose_day = input("Which day?  \n")
                if choose_day.lower() in days:
                    day = choose_day.lower()
                    month = "all"
                    break
                else:
                    print("Write the day (\"monday\", \"tuesday\"), etc. \n")
            break
        elif filter_choose.lower() == "none":
            day = "all"
            month = "all"
            break
        else:
            print("Please choose month, day or none")

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("The following inputs will be computed:")
    print("city: {}, month: {}, day: {}".format(city, month, day))
    input("press ENTER \n")
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print("Most common month: {}".format(calendar.month_name[df['month'].mode()[0]]))

    # TO DO: display the most common day of week
    print("Most common day of week: {}".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    print("Most common hour of day: {}\n".format(df['hour'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press ENTER to see the station statistics")

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most common start station: {}, ({} times)".format(df['Start Station'].mode()[0], df['Start Station'].value_counts().max()))

    # TO DO: display most commonly used end station
    print("Most common End Station: {}, ({} times)".format(df['End Station'].mode()[0], df['End Station'].value_counts().max()))

    # TO DO: display most frequent combination of start station and end station trip
    #https://stackoverflow.com/questions/53037698/how-can-i-find-the-most-frequent-two-column-combination-in-a-dataframe-in-python
    combination = df.groupby(["Start Station", "End Station"]).size().sort_values(ascending=False)
    print("Most popular combination of start / end station:\n{}\n".format(combination.iloc[[0]].to_string()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press ENTER to see the total average and trip duration statistics")

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time: {}".format(df["Trip Duration"].sum()))

    # TO DO: display mean travel time
    print("Average duration of travel: {}\n".format(df["Trip Duration"].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    input("Press ENTER to see the user statistics")


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df["User Type"].value_counts()
    print("User Types:\n{}\n".format(user_type.to_string()))

    # TO DO: Display counts of gender
    if city == "chicago" or city == "new york":
        gender = df["Gender"].value_counts()
        print("Counts of each Gender: \n{}\n".format(gender.to_string()))
    if city == "washington":
        print("No information regarding gender for Washington")

    # TO DO: Display earliest, most recent, and most common year of birth
    if city == "chicago" or city == "new york":
        print("The youngest person to use the service was born in: {}".format(int(df["Birth Year"].max())))
        print("The oldest person to use the service was born in: {}".format(int(df["Birth Year"].min())))
        print("The most common year of birth is: {}".format(int(df["Birth Year"].mode())))
    if city == "washington":
        print("No information regarding year of birth for Washington")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def rawdata(df):
    """Displays 5 rows of data until the user chooses 'No' """
    row = 0
    while True:
        viewData = input("Would you like to see the raw data? Type 'Yes' or 'No'.")
        if viewData.lower() == "yes":
            print(df.iloc[[row, row + 1, row + 2, row+ 3, row + 4]])
            row += 5
        elif viewData.lower() == "no":
            break
        else:
            print("please type yes or no")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        rawdata(df)

        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'yes':
                print("Let´s compute again!")
                break
            elif restart.lower() == 'no':
                print("Goodbye!!")
                break
            else:
                print("please type yes or no")
        if restart.lower() == "no":
            break

if __name__ == "__main__":
    main()
