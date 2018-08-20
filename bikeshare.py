import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington),
    while True:
        city = input('Which city do you want to look at? Enter chicago, new york city or washington: ')
        city = city.lower()
        if city == 'chicago' or city =='new york city' or city == 'washington':
            break;
        else:
            print('Please enter a valid response.')

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month do you want to look at? Choose from january to june, or enter \'all\': ')
        month = month.lower()
        if month == 'january' or month =='february' or month == 'march' or month == 'april' or month == 'may' or month == 'june' or month == 'all':
            break;
        else:
            print('Please enter a valid response.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day of week do you want to look at? Choose from monday to sunday, or enter \'all\': ')
        day = day.lower()
        if day == 'monday' or day =='tuesday' or day == 'wednesday' or day == 'thursday' or day == 'friday' or day == 'saturday' or day == 'sunday' or day == 'all':
            break;
        else:
            print('Please enter a valid response.')

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if necessary
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

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type:\n', df['User Type'].value_counts())

    # Display counts of gender, earliest, most recent, and most common year of birth for chicago and new york city
    if city == 'washington':
        print('There is no information on user gender or year of birth.')
    else:
        print('\nGender:\n', df['Gender'].value_counts())
        earlist_birth_year = df['Birth Year'].min()
        recent_birth_year = df['Birth Year'].max()
        common_birth_year = df['Birth Year'].mode()[0]
        print('\nOldest year of birth is', earlist_birth_year, '\nYoungest year of birth is', recent_birth_year, '\nMost common year of birth is', common_birth_year)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()

    # display the most common month for all users, subscribers and casual riders
    if month == 'all':
        print('Most common month is', df['month'].mode()[0])
        common_month_user = df.groupby('User Type')['month'].apply(lambda x: x.mode())
        print('Most common month for subscribers is {}, \nMost common month for casual riders is {}'.format(common_month_user['Subscriber'][0], common_month_user['Customer'][0]))

    # display the most common day of week for all users, subscribers and casual riders
    if day == 'all':
        print('\nMost common day of week is', df['day_of_week'].mode()[0])
        common_day_user = df.groupby('User Type')['day_of_week'].apply(lambda x: x.mode())
        print('Most common day of week for subscribers is {}, \nMost common day of week for casual riders is {}'.format(common_day_user['Subscriber'][0], common_day_user['Customer'][0]))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('\nMost common start hour is', common_start_hour)
    # display the most common start hour based on user types
    common_hour_user = df.groupby('User Type')['hour'].apply(lambda x: x.mode())
    print('Most Common start hour for subscribers is {}, \nMost Common start hour for casual riders is {}'.format(common_hour_user['Subscriber'][0], common_hour_user['Customer'][0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start and end station
    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    print('Most common start station is {}, \nMost common end station is {}'.format(common_start_station, common_end_station))

    # display most frequent combination of start station and end station trip
    df['Combined Station'] = df['Start Station'] + ' to ' + df['End Station']
    common_combined_station = df['Combined Station'].mode()[0]
    print('Most common combination of start and end station is', common_combined_station)

    # Display station statistics based on user types
    start_station_user = df.groupby('User Type')['Start Station'].apply(lambda x: x.mode())
    print('\nMost common start station for subscribers is\n {}, \nMost common start station for casual riders is\n {}'.format(start_station_user['Subscriber'][0], start_station_user['Customer'][0]))
    end_station_user = df.groupby('User Type')['End Station'].apply(lambda x: x.mode())
    print('\nMost common end station for subscribers is\n {}, \nMost common end station for casual riders is\n {}'.format(end_station_user['Subscriber'][0], end_station_user['Customer'][0]))
    combined_station_user = df.groupby('User Type')['Combined Station'].apply(lambda x: x.mode())
    print('\nMost common combined station for subscribers is\n {}, \nMost common combined station for casual riders is\n {}'.format(combined_station_user['Subscriber'][0], combined_station_user['Customer'][0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total and mean travel time
    total_travel_time = '{:.2f}'.format(df['Trip Duration'].sum()/60)
    mean_travel_time = '{:.2f}'.format(df['Trip Duration'].mean()/60)
    print('Total travel time is {} min and average travel time is {} min.'.format(total_travel_time, mean_travel_time))

    # Display average travel time based on user types
    avg_travel_time_user = df.groupby('User Type')['Trip Duration'].mean().reset_index()
    avg_time_sub = '{:.2f}'.format(avg_travel_time_user.loc[1, 'Trip Duration']/60)
    avg_time_casual = '{:.2f}'.format(avg_travel_time_user.loc[0, 'Trip Duration']/60)
    print('Average travel time for subscribers is {} min and for casual riders is {} min.'.format(avg_time_sub, avg_time_casual))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data_request():
    request = input('Would you like to see five lines of raw data for the city of interest? Enter yes or no.\n')
    x=0
    y=5
    if request == 'yes':
        print(df[x:y])
        request_again = input('Would you like to see five more lines? Enter yes or no.\n')
        while request_again == 'yes':
            x += 5
            y += 5
            print(df[x:y])
            request_again = input('Would you like to see five more lines? Enter yes or no.\n')
            if request_again == 'no':
                break

while True:
    city, month, day = get_filters()
    df = load_data(city, month, day)

    user_stats(df)
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    raw_data_request()

    restart = input('\nWould you like to restart? Enter yes or no.\n')
    if restart.lower() != 'yes':
        break
