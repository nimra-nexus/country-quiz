import os
import random
import requests
from dotenv import load_dotenv

load_dotenv() 
API_KEY = os.getenv("API_KEY")
URL = "https://api.restcountries.com/countries/v5?limit=100&response_fields=names.common,capitals"


def get_countries():
    """Ask the API for countries and return a clean list of name + capital."""
    try:
        response = requests.get(
            URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        print("Could not get data. Check your internet connection and API key.")
        return []

    countries = []
    for item in data["data"]["objects"]:
        name = item["names"]["common"]
        capitals = item.get("capitals") or []
        if capitals:  # skip countries with no capital
            countries.append({"name": name, "capital": capitals[0]["name"]})
    return countries


def play_quiz(countries, rounds=5):
    """Ask capital questions and keep score."""
    rounds = min(rounds, len(countries))
    questions = random.sample(countries, rounds)  
    score = 0

    for number, country in enumerate(questions, start=1):
        answer = input(f"Q{number}: What is the capital of {country['name']}? ").strip()
        if answer.lower() == country["capital"].lower():
            print("Correct!\n")
            score += 1
        else:
            print(f"Wrong. The capital is {country['capital']}.\n")

    print(f"Final score: {score} out of {rounds}")


def main():
    print("Welcome to the Country Quiz!\n")
    countries = get_countries()
    if countries:
        play_quiz(countries)


main()