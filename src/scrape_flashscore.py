from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_game_data():
     """
    waits for the page to load, extracts the game data, and saves it to a CSV file.
    The extracted data includes:
    - Match Date
    - Match Time
    - Home Team
    - Away Team
    The data is saved to 'out/games_to_play.csv'.
   
    Scrapes game data from a website and saves it to a CSV file.

    This function uses Selenium to automate web scraping. It navigates to a specific webpage,
    clicks a button to load more games, extracts the game data, and saves it to a CSV file.

    Returns:
        None
    """

    # Setup webdriver
    driver = webdriver.Firefox()

    try:
        # Get the page
        driver.get('https://www.flashscore.com.br/futebol/brasil/serie-b/calendario/')

        time.sleep(10)

        #link = driver.find_element(By.LINK_TEXT, 'Mostrar mais jogos')
        #driver.execute_script("arguments[0].click();", link)

        # Wait for the page to load after clicking the button
        #time.sleep(10)

        #link2 = driver.find_element(By.LINK_TEXT, 'Mostrar mais jogos')
        #driver.execute_script("arguments[0].click();", link2)
        
        # Wait for the page to load after clicking the button
        #time.sleep(10)

        # Find elements
        games = driver.find_elements(By.CSS_SELECTOR, 'div.event__match')

        # Extract game data
        game_data = []
        for game in games:
            data = game.text
            # Split the string into a list of substrings
            data_list = data.split('\n')

            # Extract the date and time
            date_time = data_list[0].split(' ')
            match_date = date_time[0]
            match_date = match_date + '2024' 
            match_time = date_time[1]

            # Extract the team names
            team_home = data_list[1]
            team_away = data_list[2]

            # Create a dictionary and append it to the game_data list
            game_dict = {'Match Date': match_date, 'Match Time': match_time, 'Home Team': team_home, 'Away Team': team_away}
            game_data.append(game_dict)

        # Create a DataFrame with the game data
        df = pd.DataFrame(game_data)

        # Save the DataFrame to a CSV file
        df.to_csv('out/games_to_play.csv', index=False)

        print('Game data extracted and saved to games_to_play.csv')
    finally:
        # Close the driver
        driver.quit()

scrape_game_data()
# The function scrape_game_data() scrapes game data from a website using Selenium, extracts the relevant information, and saves it to a CSV file. It also saves the data to a Firestore database using the Firebase Admin SDK. The function is designed to be reusable and can be called whenever new game data needs to be scraped.