import requests

class JokeGenerator:
    def __init__(self):
        self.api_url = 'https://v2.jokeapi.dev/joke/Any'

    def fetch_joke(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            joke_data = response.json()
            if joke_data['type'] == 'single':
                return joke_data['joke']
            else:
                return f"{joke_data['setup']} \n {joke_data['delivery']}"
        else:
            return "Could not fetch a joke at this time."

if __name__ == '__main__':
    generator = JokeGenerator()
    print(generator.fetch_joke())