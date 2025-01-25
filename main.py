"""Wen scraping app to get the premier league table."""
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from flask import Flask, Response, request, jsonify

app = Flask(__name__)


def get_table_html(address: str):
    team_data = []
    res = get(address)
    soup = BeautifulSoup(res.text, 'html.parser')
    table_html = soup.find('table')
    teams = table_html.find_all('tbody')
    for row in teams:
        tr = row.find_all('tr')
        for td in tr:
            data = []
            for content in td.find_all('td'):
                data.append(content.text)
            team_data.append(data)
    return team_data


def format_table(teams_data: list[str]) -> dict:
    teams = []
    for data in teams_data:
            teams.append({
                "position": data[0],
                "name": data[1],
                "played": data[2],
                "won": data[3],
                "drawn": data[4],
                "lost": data[5],
                "goals For": data[6],
                "goals Against": data[7],
                "goal difference": data[8],
                "points": data[9],
                "form": data[10]
             })
    return teams


def create_form_dict(data: list[dict]) -> list[dict]:
    form = []
    for team in data:
        results = []
        for result in team['form'].split(' '):
            result = result.lower().replace('result', '')

            if len(result) > 1:
                if "win" in result.lower():
                    results.append("win")
                elif "loss" in result.lower():
                    results.append("loss")
                else:
                    results.append('draw')

        form.append({
              "name": team['name'],
              "game -1": results[-1],
              "game -2": results[-2],
              "game -3": results[-3],
              "game -4": results[-4],
              "game -5": results[-5],
              "game -6": results[-6]
         })
    return form


def create_dataframes() -> tuple[pd.DataFrame]:
    team_data = get_table_html('https://www.bbc.co.uk/sport/football/premier-league/table')
    teams_dict = format_table(team_data)
    form_dict = create_form_dict(teams_dict)
    return pd.DataFrame(teams_dict).drop(columns='form'), pd.DataFrame(form_dict)
    

@app.route("/", methods=["GET"])
def index():
    """Returns an API welcome messsage."""
    return jsonify({ "message": "Welcome to the Premier league API!" })


@app.route("/table", methods=["GET"])
def table():
    return table_df.to_html()


@app.route("/team/<team>", methods=["GET"])
def team(team):
    df = table_df[table_df["name"] == team]
    return df.to_html(index=False)


@app.route("/form/<team>", methods=["GET"])
def form(team):
    df = form_df[form_df["name"] == team]
    return df.to_html(index=False)

if __name__ == "__main__":
    table_df, form_df = create_dataframes()
    app.run(port=8080, debug=True)
