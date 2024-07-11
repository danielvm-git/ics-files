import pandas as pd
from ics import Calendar, Event
import arrow
import uuid
from dateutil import tz
from icalendar import Calendar, Event
from pytz import timezone

def csv_to_ics(games_played_csv_file, games_to_play_csv_file, ics_file):
    # Create a new Calendar
    cal = Calendar()
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(games_played_csv_file)
    print(df.columns)

    # Convert the 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Match Date'], format='%d.%m.%Y')

    # Filter the DataFrame to only include games where 'Ponte Preta' is the home or away team
    ponte_df1 = df[(df['Home Team'] == 'Ponte Preta') | (df['Away Team'] == 'Ponte Preta')]

    # Sort the DataFrame by date
    ponte_df1 = ponte_df1.sort_values('Date')

    # Add an event for each game
    for index, row in ponte_df1.iterrows():
        e = Event()
        print(f"{row['Home Team']} {row['Result Home']} vs {row['Result Away']} {row['Away Team']}")
        e.add('summary', f"{row['Home Team']} {row['Result Home']} vs {row['Result Away']} {row['Away Team']}")
        local_tz = timezone('Etc/GMT+3')  # Replace with your timezone
        start_time = arrow.get(f"{row['Date'].strftime('%d.%m.%Y')} {row['Match Time']}", 'DD.MM.YYYY HH:mm').replace(tzinfo=local_tz)
        e.add('dtstart', start_time.datetime)
        e.add('dtend', start_time.shift(hours=2).datetime)
        e.add('dtstamp', arrow.now().datetime)  # Add the current datetime as the DTSTAMP property
        e.add('uid', str(uuid.uuid4()))  # Generate a unique UID
        cal.add_component(e)

    # Read the games_to_play CSV file into a DataFrame
    df_games_to_play = pd.read_csv(games_to_play_csv_file)
    print(df_games_to_play.columns)

    # Convert the 'Date' column to datetime
    df_games_to_play['Date'] = pd.to_datetime(df_games_to_play['Match Date'], format='%d.%m.%Y')

    # Filter the DataFrame to only include games where 'Ponte Preta' is the home or away team
    ponte_df = df_games_to_play[(df_games_to_play['Home Team'] == 'Ponte Preta') | (df_games_to_play['Away Team'] == 'Ponte Preta')]

    # Sort the DataFrame by date
    ponte_df = ponte_df.sort_values('Date')

    # Add an event for each game
    for index, row in ponte_df.iterrows():
        e = Event()
        print(f"{row['Home Team']} vs {row['Away Team']}")
        e.add('summary', f"{row['Home Team']} vs {row['Away Team']}")
        local_tz = timezone('Etc/GMT+3')  # Replace with your timezone
        start_time = arrow.get(f"{row['Date'].strftime('%d.%m.%Y')} {row['Match Time']}", 'DD.MM.YYYY HH:mm').replace(tzinfo=local_tz)
        print(local_tz)
        print(start_time)
        e.add('dtstart', start_time.datetime)
        e.add('dtend', start_time.shift(hours=2).datetime)
        e.add('dtstamp', arrow.now().datetime)  # Add the current datetime as the DTSTAMP property
        e.add('uid', str(uuid.uuid4()))  # Generate a unique UID
        cal.add_component(e)

    # Write the calendar to an .ics file
    with open(ics_file, 'wb') as my_file:
        my_file.write(cal.to_ical())

    print(f'Calendar saved to {ics_file}')

csv_to_ics('games_played.csv', 'games_to_play.csv', 'calendar_ponte_preta_serie_b.ics')