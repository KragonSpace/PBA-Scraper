import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLs
BASE_URL = "https://www.pba.ph"
TEAMS_URL = f"{BASE_URL}/teams"
PLAYERS_URL = f"{BASE_URL}/players"

# Headers to simulate a browser request
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Function to scrape team details
def scrape_teams():
    print("Scraping team details...")
    response = requests.get(TEAMS_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    teams_data = []

    # Find all team containers
    team_containers = soup.find_all("div", class_="team-page-box")

    for team in team_containers:
        logo_link = team.find("img")["src"]
        team_url = team.find("a")["href"]

        # Extract a team info
        team_info_response = requests.get(team_url, headers=HEADERS)
        team_info_soup = BeautifulSoup(team_info_response.text, "html.parser")

        # Find the container that includes team information
        team_info_container = team_info_soup.find("div", class_="team-personal-bar")

        # Extract the team name accurately
        team_name = team_info_container.find("h3").string.strip() if team_info_container else "N/A"

       # Function to extract sibling text safely
        def get_next_sibling_text(header_tag, sibling_tag="h5"):
            if header_tag:
                sibling = header_tag.find_next_sibling(sibling_tag)
                if sibling and sibling.string:
                    return sibling.string.strip()
            return "N/A"

        # Extract head coach and manager
        head_coach_header = team_info_container.find("h5", string="HEAD COACH") if team_info_container else None
        head_coach = get_next_sibling_text(head_coach_header)

        manager_header = team_info_container.find("h5", string="MANAGER") if team_info_container else None
        manager = get_next_sibling_text(manager_header)

        teams_data.append({
            "Team Name": team_name,
            "Head Coach": head_coach,
            "Manager": manager,
            "URL": team_url,
            "Logo Link": logo_link
        })

    print("Finished scraping teams.")
    return teams_data

# Function to scrape player details
def scrape_players():
    print("Scraping player details...")
    response = requests.get(PLAYERS_URL, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    
    players_data = []

    # Find all player containers
    player_containers = soup.find_all("div", class_="playersBox")

    for player in player_containers:
        player_url = BASE_URL + '/' + player.find("a")["href"]
        mugshot = player.find("img")["src"]

        # Extract a player profile
        player_profile_response = requests.get(player_url, headers=HEADERS)
        player_profile_soup = BeautifulSoup(player_profile_response.text, "html.parser")

        # Extract player's name safely
        player_name_tag = player_profile_soup.find("h3")
        player_name = player_name_tag.get_text(strip=True) if player_name_tag else "N/A"

        # Extract team name safely
        team_name_tag = player_profile_soup.find("p", class_="team-info")
        team_name = team_name_tag.get_text(strip=True) if team_name_tag else "N/A"

        # Extract player number and position safely
        common_info_tag = player_profile_soup.find("p", class_="common-info")
        if common_info_tag:
            common_info = common_info_tag.get_text(strip=True)
            parts = common_info.split('/')
            player_number = parts[0].strip() if len(parts) > 0 else "N/A"
            position = parts[-1].strip() if len(parts) > 1 else "N/A"
        else:
            player_number = "N/A"
            position = "N/A"

        players_data.append({
            "Team Name": team_name,
            "Player Name": player_name,
            "Number": player_number,
            "Position": position,
            "URL": player_url,
            "Mugshot": mugshot
        })

    print("Finished scraping players.")
    return players_data

# Main script
def main():
    # Scrape team and player data
    teams = scrape_teams()
    players = scrape_players()

    # Save to CSV
    print("Saving data to CSV files...")
    pd.DataFrame(teams).to_csv("teams.csv", index=False)
    pd.DataFrame(players).to_csv("players.csv", index=False)
    print("Data saved successfully as teams.csv and players.csv.")

if __name__ == "__main__":
    main()
