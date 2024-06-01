from flask import Flask, render_template, jsonify, request
import random
import threading
import time
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

race_data = {
    'is_race_on': False,
    'horse_positions': {},
    'winner': None,
    'player_bets': [],
    'horse_names': [],
    'results': [],
    'double_bets': False
}

def generate_random_horse_names(num_horses):
    adjectives = ['Fast', 'Swift', 'Limp', 'Old', 'Veiny', 'Girthy', 'Black', 'Throbbing', 'Jolly', 'Moist']
    nouns = ['Stallion', 'Mare', 'Pony', 'Colt', 'Filly', 'Charger', 'Gelding', 'Steed', 'Courser']
    return [f"{random.choice(adjectives)} {random.choice(nouns)}" for _ in range(num_horses)]

@app.route('/')
def home():
    if not race_data['horse_names']:  # Only set horse names if they haven't been set
        race_data['horse_names'] = generate_random_horse_names(4)  # Default to 4 horses
    return render_template('index.html', horses=race_data['horse_names'])

@app.route('/start-race', methods=['POST'])
def start_race():
    if not race_data['is_race_on']:
        data = request.get_json()
        logging.debug(f"Start race data: {data}")
        race_data['double_bets'] = data.get('isDouble', False)
        race_data['player_bets'] = data['playerBets']
        threading.Thread(target=simulate_race).start()
        return jsonify(success=True)
    else:
        return jsonify({"error": "Race is already in progress"}), 400

@app.route('/set-horses', methods=['POST'])
def set_horses():
    data = request.get_json()
    logging.debug(f"Set horses data: {data}")
    num_horses = int(data.get('numHorses', 4))
    race_data['horse_names'] = generate_random_horse_names(num_horses)
    return jsonify(horse_names=race_data['horse_names'])

@app.route('/reset-race', methods=['POST'])
def reset_race():
    logging.debug("Reset race")
    race_data['is_race_on'] = False
    race_data['horse_positions'] = {}
    race_data['winner'] = None
    race_data['player_bets'] = []
    race_data['results'] = []
    race_data['horse_names'] = []  # Clear horse names on reset
    return jsonify(success=True)

@app.route('/race-status', methods=['GET'])
def race_status():
    logging.debug("Race status requested")
    return jsonify(race_data)

def simulate_race():
    race_data['is_race_on'] = True
    race_data['horse_positions'] = {horse: 0 for horse in race_data['horse_names']}
    while max(race_data['horse_positions'].values(), default=0) < 16:
        time.sleep(1)
        for horse in race_data['horse_names']:
            race_data['horse_positions'][horse] += random.choice([0, 1, 2])
        if max(race_data['horse_positions'].values(), default=0) >= 16:
            race_data['winner'] = max(race_data['horse_positions'], key=race_data['horse_positions'].get)
            break
    race_data['is_race_on'] = False
    race_data['results'] = calculate_betting_results(race_data['winner'])

def calculate_betting_results(winning_horse):
    results = []
    multiplier = 2 if race_data['double_bets'] else 1
    for bet in race_data['player_bets']:
        if bet['horse'] == winning_horse:
            results.append(f"{bet['name']} wins! Give out {int(bet['drinks']) * multiplier} drinks.")
        else:
            results.append(f"{bet['name']} loses. Take {bet['drinks']} drinks.")
    return results

if __name__ == "__main__":
    app.run(debug=True)
