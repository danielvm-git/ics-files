from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_flashscore_past():
    """
    Scrapes past football match data from the Flashscore website for Brazil's Serie B.

    This function uses Selenium to automate a web browser, navigate to the Flashscore 
    results page for Brazil's Serie B, and extract data for past matches. The extracted 
    data includes match date, match time, home team, away team, and the results for 
    both teams. The data is then saved to a CSV file.

    Steps:
    1. Setup a Firefox web driver and navigate to the Flashscore results page.
    2. Wait for the page to load.
    3. Click the "Mostrar mais jogos" button to load more games, if available.
    4. Extract game data from the loaded page.
    5. Save the extracted data to a CSV file.

    Returns:
        None

    Raises:
        Exception: If the "Mostrar mais jogos" button is not found or no more games to load.
    """
    # Setup Chrome and navigate to the webpage
    driver = webdriver.Firefox()
    driver.get("https://www.flashscore.com.br/futebol/brasil/serie-b/resultados/")

    # Wait for the page to load
    time.sleep(10)

    try:
        # Click the button to load more games, if it exists
        link = driver.find_element(By.LINK_TEXT, 'Mostrar mais jogos')
        while link:
            driver.execute_script("arguments[0].click();", link)
            time.sleep(3)  # Wait for the games to load
            driver.execute_script("arguments[0].click();", link)
    except Exception as e:
        print("No more games to load or button not found.")

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
        match_result_home = data_list[3]
        match_result_away = data_list[4]

        # Create a dictionary and append it to the game_data list
        game_dict = {'Match Date': match_date, 'Match Time': match_time, 'Home Team': team_home, 'Away Team': team_away, 'Result Home': match_result_home, 'Result Away': match_result_away}
        game_data.append(game_dict)

    # Close the driver
    driver.quit()

    # Create a DataFrame with the game data
    df = pd.DataFrame(game_data)

    # Save the DataFrame to a CSV file
    df.to_csv('out/games_played.csv', index=False)

    print('Game data extracted and saved to games_played.csv')

scrape_flashscore_past()