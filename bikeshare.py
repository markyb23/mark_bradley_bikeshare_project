import time
import pandas as pd
import numpy as np

"""
The following defines the valid inputs for city, month and day.
"""
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    # The following code requests user input for choice of city.
    while True:
        city = input('\nWhich city would you like to explore data for, Chicago, New York City or Washington?\n')
        city = city.lower()
        if city not in CITY_DATA:
            print('We do not have data for that city, please try again.')
            continue
        else:
            break

    # The following code requests user input for choice of month.
    while True:
        month = 'All'
        month_filter = input('\nWould you like to filter by month? (Y/N)\n')
        if month_filter.title() == 'Y':
            month = input('\nWhich month would you like to explore data for, January, February, March, April, May or June?\n')
            month = month.title()
        elif month_filter.title() =='N':
            break
        else:
            print('You have entered an invalid response. Please try again.')
            continue
        if month not in months:
            print('We do not have data for that month please try again.')
            continue
        else:
            break

    # The following code requests user input for choice of day.
    while True:
        day = 'All'
        day_filter = input('\nWould you like to filter by day? (Y/N)\n')
        if day_filter.title() == 'Y':
            day = input('\nWhich day of the week would you like to explore data for?\n')
            day = day.title()
        elif day_filter.title() =='N':
            break
        else:
            print('You have entered an invalid response. Please try again.')
            continue
        if day not in days:
            print('Your input is invalid, please try again.\n')
            continue
        else:
            break

    print('\nYou have chosen to explore data for:\nCity: {}\nMonth: {}\nDay: {}'.format(city.title(), month, day))
    print('-'*40)
    return city, month, day

    ##### This marks the end of the get_filters function #####

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

    # the code below gives a name to the 'unnamed' reference column #
    df.rename(columns = {'Unnamed: 0':'Reference'}, inplace = True)

    # the code below replaces NaN values in the 'Gender' column with the text 'Information not provided' #
    if 'Gender' in df:
        df['Gender'] = df['Gender'].fillna('No information provided')

    # convert the Start Time column to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'All':
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'All':

        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day]
    return df

    ##### This marks the end of the load_data function #####

def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # The following code displays the most common month
    if month == 'All':
        max_trips_month = df.groupby(['Month'])['Month'].count().max()
        popular_month = df['Month'].mode()[0]
        popular_month = months[popular_month -1]
        print('The most common month was {} with a total of {} trips.'.format(popular_month, max_trips_month))

    # The following code displays the most common day of week
    if day == 'All':
        max_trips_day = df.groupby(['Day of Week'])['Day of Week'].count().max()
        popular_day = df['Day of Week'].mode()[0]
        print('The most common day of the week was {} with a total of {} trips.'.format(popular_day, max_trips_day))

    # The following code displays the most common start hour
    df['Start Hour'] = pd.to_datetime(df['Start Time']).dt.hour
    max_trips_hour = df.groupby(['Start Hour'])['Start Hour'].count().max()
    popular_hour = df['Start Hour'].mode()[0]
    print('The most common start hour was {}:00 with a total of {} trips.'.format(popular_hour, max_trips_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    ##### This marks the end of the time_stats function #####

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # The following code displays most commonly used start station
    max_trips_start_station = df.groupby(['Start Station'])['Start Station'].count().max()
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common starting station was {} with a total of {} trips starting there.'.format(popular_start_station, max_trips_start_station))

    # The following code displays the most commonly used end station
    max_trips_end_station = df.groupby(['End Station'])['End Station'].count().max()
    popular_end_station = df['End Station'].mode()[0]
    print('The most common ending station was {} with a total of {} trips ending there.'.format(popular_end_station, max_trips_end_station))

    # The following code displays the most frequent combination of start station and end station trip
    df['Journey'] = df['Start Station'] +' and ended at ' + df['End Station']
    max_journeys = df.groupby(['Journey'])['Journey'].count().max()
    popular_journey = df['Journey'].mode()[0]
    print('The most common journey started at {}. This trip was taken on {} occasions.'.format(popular_journey, max_journeys))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    ##### This marks the end of the station_stats function #####

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # The following code displays the total travel time
    df['travel time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    total_travel_time = df['travel time'].sum()
    total_trips = df['travel time'].count()
    print('There were {} trips in total, resulting in a total travel time of {}.'.format(total_trips, total_travel_time))

    # The following code displays the mean travel time
    mean_travel_time = df['travel time'].mean()
    print('The average duration of each trip was {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    ##### This marks the end of the trip-duration_stats function #####

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # The following code displays counts of user types
    print('The make-up of the different types of user was as follows:\n')
    print(df.groupby(['User Type'])['User Type'].count())

    # The following code displays counts of gender
    try:
        df2 = df.groupby(['Gender'])['Gender'].count()
        print('\nThe make-up of the genders of the different users was as follows:\n')
        print(df2)

    except:
        print('\nNo information regarding the gender of users is available for your chosen city.')

    # The followng code displays earliest, most recent, and most common year of birth
    try:
        earliest_birth_year = df['Birth Year'].min()
        latest_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        no_birth_year = df['Birth Year'].isnull().sum().sum()
        print('\nThe earliest year in which any user was born is {}.'.format(earliest_birth_year))
        print('The most recent year in which any user was born is {}.'.format(latest_birth_year))
        print('The most common year in which users were born is {}.'.format(common_birth_year))
        print('The user\'s birth year is unavailable for {} trips.'.format(no_birth_year))

    except:
        print('No information regarding the birth years of users is availale for your chosen city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    ##### This marks the end of the user_stats function #####

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # The following asks the user if they would like to view the raw data #
        #while True:
        indices = [0, 1, 2, 3, 4]
        while True:
            view_data = input('\nWould you like to view some raw data? (Y/N)\n')
            if view_data.title() != 'Y':
                break
            elif view_data.title() == 'Y':
                print(df.iloc[indices])
                indices[0] += 5
                indices[1] += 5
                indices[2] += 5
                indices[3] += 5
                indices[4] += 5

        restart = input('\nWould you like to restart? (Y/N)\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
