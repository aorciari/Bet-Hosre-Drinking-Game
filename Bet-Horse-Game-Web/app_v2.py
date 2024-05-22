from flask import Flask, render_template, jsonify, request
import random
import threading
import time

app = Flask(__name__)

# Shared data structure to store race data, player bets, and race results
race_data = {
    'is_race_on': False,
    'horse_positions': {},
    'winner': None,
    'player_bets': [],
    'horse_names': []
}

def generate_random_horse_names(num_horses):
    adjectives = ['Fast', 'Swift', 'Limp', 'Old', 'Veiny', 'Girthy', 'Black', 'Throbbing', 'Jolly', 'Moist']
    nouns = ['Stallion', 'Mare', 'Pony', 'Colt', 'Filly', 'Charger', 'Gelding', 'Steed', 'Courser']
    horse_names = [f"{random.choice(adjectives)} {random.choice(nouns)}" for _ in range(num_horses)]
    return horse_names

def simulate_race():
    race_data['is_race_on'] = True
    race_data['horse_positions'] = {horse: 0 for horse in race_data['horse_names']}
    while max(race_data['horse_positions'].values()) < 16:
        time.sleep(1)  # Simulate time delay for each race step
        for horse in race_data['horse_names']:
            race_data['horse_positions'][horse] += random.choice([0, 1, 2])  # Randomly increase horse position
        race_data['winner'] = max(race_data['horse_positions'], key=race_data['horse_positions'].get)
    race_data['is_race_on'] = False

@app.route('/')
def home():
    # Generate horse names when the page is loaded
    race_data['horse_names'] = generate_random_horse_names(4)
    return render_template('index.html', horses=race_data['horse_names'])

@app.route('/start-race', methods=['POST'])
def start_race():
    if not race_data['is_race_on']:
        race_data['player_bets'] = request.json['playerBets']
        threading.Thread(target=simulate_race).start()  # Start the race in a separate thread
    return jsonify(success=True)

@app.route('/race-status', methods=['GET'])
def race_status():
    return jsonify(race_data)

if __name__ == "__main__":
    app.run(debug=True)
