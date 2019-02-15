import yaml


class StateScraper:
    def __init__(self):
        self.data = 'data/state_data.yml'

    def fetch_state_data(self, state):
        state_data = yaml.load(open(self.data, 'r'))
        return state_data[state]
