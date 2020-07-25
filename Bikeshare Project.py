#Udacity project created to analyse data from three major cities
import time
import calendar #used to convert months from number to names for readability
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters(city, month, day):
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
        city = input("What city would you like to pull data from? New York City, Chicago, or Washington?:\n ").lower()
        if city not in CITY_DATA:
            print("\nI did not get that, please check your spelling and try again.\n")
            continue
        else:
            break

    while True:
        filter = input("How would you like to filter the data? Month, Day, Both, or None?: \n").lower()
        if filter == 'month':
            month = input("We have data from Janury to June, Which month would you like to evaluate?:\n").lower()
            day = 'all'
            break
        elif filter == 'day':
            day = input('What day would you like to evaluate? (Sunday, Monday, Tuesday, Wednesday, Thursday, Ffriday, Saturday)):\n').lower()
            month = 'all'
            break
        elif filter == 'both':
            month = input("Between January and June, which month would you like to evaluate?:\n").lower()
            day = input("What day would you like to evaluate?:\n").lower()
            break
        elif filter == 'none':
            month = 'all'
            day = 'all'
            break
        else:
            input("Sorry, I didn't get that. Please make sure to type: Month, Day, All, or None")
            break

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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) +1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most popular month to rent a bike is {}'.format(calendar.month_name[common_month]))

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most popular day of the week to rent a bike is {}'.format(common_day))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start = df['hour'].mode()[0]
    print('The most popular time of the day to rent a bike is {}'.format(common_start))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most popular station to rent a bike is {}'.format(common_start))

    # display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most popular station to return a bike is {}'.format(common_end))

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + df['End Station']
    common_combination = df['combination'].mode()[0]
    print('The most popular route (Start to End) is from {} to {}'.format(common_end,common_start))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    total_travel = total_travel/3600 # to convert to hours
    print('The total travel time is {} hours.'.format(total_travel))

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    mean_travel=mean_travel/60 #to convert to minutes
    print('The average trip durantion per trip is {} minutes.'.format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('\nThe user distribution between Subscribers, Customers and Dependent is\n{}'.format(user_types))

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print('\nThe riders distribution between Male and Female is\n {}'.format(gender))
    else:
        print("\nSorry, we seem to be missing the gender information for this city.\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth_Year' in df:
        earliest = df['Birth_Year'].min()
        print("The oldest riders were born in {}.".format(earliest))
        recent = df['Birth_Year'].max()
        print('The youngest riders were born in {}.'.format(recent))
        common_birth = df['Birth Year'].mode()[0]
        print('Most riders were born in the year {}.'.format(common_birth))
    else:
        print("\nSorry, we seem to be missing the birth year information for this city.\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

"""Display 5 lines of Raw data if desired by the user"""
def raw_data(df):
    raw_data = 0
    while True:
        raw = input("Do you want to see the raw data? Yes or No: \n").lower()
        if raw == 'yes':
            raw_data += 5
            print(df.iloc[raw_data : raw_data +5])
            continue
        elif raw == 'no':
            break
        else:
            print("\nSorry, I didn't get that. Please type Yes or No.: \n").lower()
            retun

def main():
    city = ""
    month = ""
    day = ""
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Please type Yes or No. \n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
