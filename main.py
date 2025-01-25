"""Wen scraping app to get the premier league table."""
from requests import get
from bs4 import BeautifulSoup
import pandas as pd



def get_table(address: str):
    data = []
    res = get(address)
    soup = BeautifulSoup(res.text, 'html.parser')
    table_html = soup.find('table')
    teams = table_html.find_all('tbody')
    for row in teams:
        tr = row.find_all('tr')
        for td in tr:
            for content in td.find_all('td'):
                data.append(content.text)
    return data
            
                

def format_table(data: list[str]) -> dict:
    teams = []
    for i in range(0,200,11):
            teams.append({
                "position": data[i],
                "team": data[i+1],
                "played": data[i+2],
                "won": data[i+3],
                "drawn": data[i+4],
                "lost": data[i+5],
                "goals For": data[i+6],
                "goals Against": data[i+7],
                "goal difference": data[i+8],
                "points": data[i+9],
                "form": data[i+10]
             })
    return teams


if __name__ == "__main__":
    team_data = get_table('https://www.bbc.co.uk/sport/football/premier-league/table')
    teams_dict = format_table(team_data)
    print(pd.DataFrame(teams_dict))