from flask import Flask, render_template, jsonify
import random
import threading
import time

app = Flask(__name__)

# Shared data structure to store race progress and results
race_data = {
    'is_race_on': False,
    'horse_positions': {},
    'winner': None
}

def generate_random_horse_names(num_horses):
    adjectives = ['Fast', 'Swift', 'Limp', 'Old', 'Veiny', 'Girthy', 'Black', 'Throbbing', 'Jolly', 'Moist']
    nouns = ['Stallion', 'Cock', 'Mary', 'Yugank', 'Greg', 'Tip', 'Clam', 'Beers', 'Taylor']
    horse_names = []
    for _ in range(num_horses):
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        horse_name = f"{adjective} {noun}"
        horse_names.append(horse_name)
    return horse_names

def simulate_race():
    race_data['is_race_on'] = True
    horse_names = generate_random_horse_names(4)
    race_data['horse_positions'] = {horse: 0 for horse in horse_names}
    while max(race_data['horse_positions'].values()) < 16:
        time.sleep(1)  # Simulate time delay for each race step
        for horse in horse_names:
            race_data['horse_positions'][horse] += random.choice([0, 1, 2])  # Randomly increase horse position
        race_data['winner'] = max(race_data['horse_positions'], key=race_data['horse_positions'].get)
    race_data['is_race_on'] = False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start-race', methods=['POST'])
def start_race():
    if not race_data['is_race_on']:
        threading.Thread(target=simulate_race).start()  # Start the race in a separate thread
    return jsonify(success=True)

@app.route('/race-status', methods=['GET'])
def race_status():
    return jsonify(race_data)

if __name__ == "__main__":
    app.run(debug=True)
