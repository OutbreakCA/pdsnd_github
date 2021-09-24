import time
import pandas as pd
import numpy as np


CITY_DATA = { 'Chicago': '/chicago.csv',
              'New York City':'/new_york_city.csv',
              'Washington''/washington.csv' }

weekday = ['Sunday',
      'Monday',
      'Tuesday',
      'Wednesday',
      'Thursday',
      'Friday',
      'Saturday']

'''
Only months January to June used in current data set,
other months included in case data set expanded later
'''
month_of_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

def make_mode(value):
    """
    Gets mode average from inputed value.

    Returns:
        mode of input value
    """
    mode_no = value.mode()[0]
    return mode_no

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please select a city from either Chicago, New York City or Washington: ').title()
        if city == "Chicago" or city == "New York City" or city == "Washington":
            break
        else:
            print("\nWhoops! Please select either Chicago, New York City or Washington.\n")
            continue
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Please select a month from January, February, March, April, May or June, alternatively select "all" to get all results: ').title()
        if  month == "January" or month == "February" or month == "March" or month == "April" or month == "May" or month == "June" or month == "All":
            break
        else:
            print("\nWhoops! Please select a month between January and June.\n")
            continue
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_select = input('Please select a day of the week to filter by, alternatively select "all" to get all results: ').title()
        if day_select == "All":
            day = day_select
            break

        elif day_select in weekday:
            day = weekday.index(day_select)
            break
        else:
            print("\nWhoops! Please select a weekday or 'all'\n")
            continue
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
    # load correct data file into the dataframe
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime for conversion
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day of week and hour of day from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour_of_day'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = month_of_year[(make_mode(df['month'])-1)]
    print("The most popular month to rent a bike was {}".format(popular_month))
    # display the most common day of week
    popular_day = weekday[(make_mode(df['day_of_week'])-1)]
    print("The most popular day to rent a bike was {}".format(popular_day))
    # display the most common start hour
    popular_hour = make_mode(df['hour_of_day'])
    print("The most common hour (24 hour format) to rent a bike was {}:00 to {}:00".format(popular_hour, (popular_hour + 1)))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_destination = make_mode(df['Start Station'])
    print("The most popular station to rent a bike was {}".format(popular_start_destination))
    # display most commonly used end station
    popular_end_destination = make_mode(df['End Station'])
    print("The most popular station to drop off a bike was {}".format(popular_end_destination))

    # display most frequent combination of start station and end station trip
    popular_journey = df.groupby('Start Station')['End Station'].value_counts().idxmax()
    print("The most popular journey was between {} and {}".format(popular_journey[0], popular_journey[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total time travelled was {}".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time was {}".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = dict(df['User Type'].value_counts())
    print("Here is a list of how many users we have had of each type:")
    for key, value in user_type_count.items():
        print(key, ": ", value)

    # Display counts of gender
    if 'Gender' in df:
        gender_count = dict(df['Gender'].value_counts())
        print("\nHere is a list of how many users we have of each gender:")
        for key, value in gender_count.items():
            print(key, ": ", value)
    else:
        print('\nWe\'d love to show you a breakdown of genders however no gender information was provided')

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        min_birth = int(df['Birth Year'].min())
        max_birth = int(df['Birth Year'].max())
        mode_birth = int(make_mode(df['Birth Year']))

        print("\nThe oldest rider we've had was born in {}".format(min_birth))
        print("The youngest rider we've had was born in {}".format(max_birth))
        print("The most common birth year our riders have is {}".format(mode_birth))
    else:
        print('\nWe\'d love to show you the age range of riders, however no birth date information was provided')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_raw_data(df):
    """
    Shows user 5 lines of raw data on request
    Asks user if they want to see more, exit's on any response
    but 'Yes' or if no more rows to display.

    """
    print("\n Here are 5 lines of raw data for you to look over \n")
    pd.set_option('display.max_columns', None)

    for i in range(0, len(df), 5):
        print(df.iloc[i:(i+5)])
        print('-'*40)
        get_more_rows = input("Would you like to see the next 5 rows? Enter Yes or No\n")
        if get_more_rows.title() != 'Yes':
            break
        elif i > (len(df)-5):
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        see_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
