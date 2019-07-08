import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

city = ''
month = ''
day = ''
df = []


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    global city, month, day
    print("\nHello! Let\'s explore some US bikeshare data!\n")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you like to explore?\n").lower()
    while city not in ['chicago', 'new york city', 'washington']:
        print(
            "There is no data available for {}. Please enter another city (chicago, new york city or washington).\n".format(
                city))
        city = input("Which city would you like to explore?\n")
    else:
        print("\nGreat, let\'s have a look at {}!\n".format(city.title()))

    month = input(
        "Which month would you like to look at? If you want to look at all months, please select all.\n").lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        print("There is no data available for {}. Please enter another month (january to june).\n".format(
            month))
        month = input("Which month would you like to look at? If you want to look at all months, please select all.\n")
    else:
        if month == 'all':
            print('\nGreat, we will look for data in all months.')
        else:
            print('\nGreat, we will look for data in {}.\n'.format(month.title()))

    day = input(
        "Which day of the week would you like to look at? If you want to look at all days, please select all.\n").lower()
    while day not in ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
        print("There is no data available for {}. Please enter another day (monday to sunday).\n".format(
            day))
        day = input("Which month would you like to look at? If you want to look at all days, please select all.\n")
    else:
        if day == 'all':
            print("\nOkay, we will look for data for all days.")
        else:
            print("\nOkay, we will look for data from {}s.\n".format(day.title()))

    print('-' * 40)
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
    global df
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['start_hour'] = df['Start Time'].dt.hour

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
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
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[common_month - 1]

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    common_hour = df['start_hour'].mode()[0]
    print("Within {}, the most frequent time of travel was {}, on {}s at {} o'clock.\n".format(city.title(),
                                                                                               common_month.title(),
                                                                                               common_day.title(),
                                                                                               common_hour))
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_st_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    # display most frequent combination of start station and end station trip
    common_station = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False)
    idx_common_station = common_station.idxmax()

    print("Within {}, the most common start station was {} whereas the most common end station was {}.\n".format(
        city.title(), common_st_station, common_end_station))
    print("The most used combination of start and end station was {}.\n".format(
        str(idx_common_station[0] + " with " + idx_common_station[1])))
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tt_total = df['Trip Duration'].sum()
    tt_total_min = divmod(tt_total, 60)
    tt_total_h = divmod(tt_total_min[0], 60)
    tt_total_d = divmod(tt_total_h[0], 24)
    tt_total_fm = (
        "{}d {}h {}min {}sec".format(int(tt_total_d[0]), int(tt_total_d[1]), int(tt_total_h[1]), int(tt_total_min[1])))

    # display mean travel time
    tt_mean = df['Trip Duration'].mean()
    tt_mean_min = divmod(tt_mean, 60)
    tt_mean_h = divmod(tt_mean_min[0], 60)
    tt_mean_fm = ("{}h {}min {}sec".format(int(tt_mean_h[0]), int(tt_mean_h[1]), int(tt_mean_min[1])))

    print("Within {}, the total time that users traveled was {} whereas the mean time of one journey was {}.\n".format(
        city.title(), tt_total_fm, tt_mean_fm))
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("Users can be grouped into the following types:\n")
    print(user_types.to_string())

    # Display counts of gender
    if 'Gender' in df:
        user_gender = df['Gender'].value_counts()
        print("\nUsers are grouped into these genders:\n")
        print(user_gender.to_string())
    else:
        print("\nThere is no gender data available for {}.\n".format(city.title()))

    # Display earliest, most recent, and most common year of birth
    if 'Gender' in df:
        earliest_dob = df['Birth Year'].min()
        recent_dob = df['Birth Year'].max()
        common_dob = df['Birth Year'].value_counts()
        common_dob = common_dob.idxmax()
        print(
            "\nThe earliest date of birth of customers is {}, the most recent date is {} and the most common birth year is {}.\n".format(
                int(earliest_dob), int(recent_dob), int(common_dob)))

    else:
        print("\nThere is no year of birth data available for {}.\n".format(city.title()))

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_input(df):
    """Displays 5 lines of raw input upon request."""
    pd.set_option('display.max_columns', None)
    raw = input('\nWould you like see some raw input data? Enter yes or no.\n')
    raw_count = 5

    while raw.lower() == 'yes':
        print(df[:raw_count])
        raw_count += 5
        raw = input('\nWould you like see some more raw input data? Enter yes or no.\n')
        if raw.lower() != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_input(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
