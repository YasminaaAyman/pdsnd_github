import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_valid_input(input_word, input_type):
    #type 1 is city
    #type 2 is month
    #type 3 is day
    while True:
        user_input = input(input_word).lower()
        try:
            if user_input in ['chicago','new york city','washington'] and input_type == 1:
                break
            elif user_input in ['january', 'february', 'march', 'april', 'may', 'june','all'] and input_type == 2:
                break
            elif user_input in ['sunday','monday','tuesday','wednesday','thursday','friday','saturday','all'] and input_type == 3:
                break
            else:
                if input_type == 1:
                    print("Your input should be: chicago, new york city or washington")
                if input_type == 2:
                    print("Your input should be: january, february, march, april, may, june or all")
                if input_type == 3:
                    print("Your input should be: sunday, monday, tuesday, wednesday, thursday, friday, saturday or all")
        except ValueError:
            print("Sorry, your input is wrong")
    return user_input

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
    city = check_valid_input("Would you like to see data for chicago, New York City, or Washington?\n",1)

    # get user input for month (all, january, february, ... , june)
    month = check_valid_input("Which month - January, February, March, April, May, or June?\n",2)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = check_valid_input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n",3)


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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
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

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("Most common Month : ", most_common_month)

    # display the most common day of week
    most_common_day_of_week = df['day_of_week'].mode()[0]
    print("Most common day of week : ",most_common_day_of_week)

    # display the most common start hour
    most_common_start_hour = df['hour'].mode()[0]
    print("Most common hour of day : ",most_common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most commonly used start station : ",most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most commonly used end station : ",most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_frequent_combination_group = df.groupby(['Start Station','End Station'])
    most_frequent_combination = most_frequent_combination_group.size().sort_values(ascending=False).head(1)
    print("Most frequent combination of start station and end station trip : ",most_frequent_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total Travel Time : ",total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean Travel Time : ",mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type = df['User Type'].value_counts()
    print("User type : ",user_type)

    if city != 'washington':
        # Display counts of gender
        gender_stats = df['Gender'].value_counts()
        print("Gender stats : ",gender_stats)

        # Display earliest, most recent, and most common year of birth
        print("Birth year stats:\n")
        earliest_year = df['Birth Year'].min()
        print("Earliest Year : ",earliest_year)
        most_recent_year = df['Birth Year'].max()
        print("Most recent year : ",most_recent_year)
        most_common_year = df['Birth Year'].mode()[0]
        print("Most common year : ",most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        show_more = input("\n Do you want to show more data? Enter yes or no.\n")
        if show_more.lower() != 'yes':
            restart = input("\n Would you like to restart? Enter yes or no.\n")
            if restart.lower() != 'yes':
                break

        station_stats(df)
        show_more = input("\n Do you want to show more data? Enter yes or no.\n")
        if show_more.lower() != 'yes':
            restart = input("\n Would you like to restart? Enter yes or no.\n")
            if restart.lower() != 'yes':
                break

        trip_duration_stats(df)
        show_more = input("\n Do you want to show more data? Enter yes or no.\n")
        if show_more.lower() != 'yes':
            restart = input("\n Would you like to restart? Enter yes or no.\n")
            if restart.lower() != 'yes':
                break
            
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
