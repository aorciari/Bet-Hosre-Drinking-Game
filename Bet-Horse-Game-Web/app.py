from flask import Flask, render_template, jsonify, request
import random
import threading
import time

app = Flask(__name__)

race_data = {
    'is_race_on': False,
    'horse_positions': {},
    'winner': None,
    'player_bets': [],
    'horse_names': [],
    'results': []
}

def generate_random_horse_names(num_horses):
    adjectives = ['Fast', 'Swift', 'Limp', 'Old', 'Veiny', 'Girthy', 'Black', 'Throbbing', 'Jolly', 'Moist']
    nouns = ['Stallion', 'Mare', 'Pony', 'Colt', 'Filly', 'Charger', 'Gelding', 'Steed', 'Courser']
    return [f"{random.choice(adjectives)} {random.choice(nouns)}" for _ in range(num_horses)]

def calculate_betting_results(winning_horse):
    results = []
    for bet in race_data['player_bets']:
        if bet['horse'] == winning_horse:
            result = f"{bet['name']} wins! Give out {int(bet['drinks']) * 2} drinks."
        else:
            result = f"{bet['name']} loses. Take {bet['drinks']} drinks."
        results.append(result)
    return results

def simulate_race():
    race_data['is_race_on'] = True
    race_data['horse_positions'] = {horse: 0 for horse in race_data['horse_names']}
    while max(race_data['horse_positions'].values()) < 16:
        time.sleep(1)
        for horse in race_data['horse_names']:
            race_data['horse_positions'][horse] += random.choice([0, 1, 2])
        race_data['winner'] = max(race_data['horse_positions'], key=race_data['horse_positions'].get)
        race_data['results'] = calculate_betting_results(race_data['winner'])
    race_data['is_race_on'] = False

@app.route('/')
def home():
    race_data['horse_names'] = generate_random_horse_names(4)
    return render_template('index.html', horses=race_data['horse_names'])

@app.route('/start-race', methods=['POST'])
def start_race():
    if not race_data['is_race_on']:
        race_data['player_bets'] = request.json['playerBets']
        threading.Thread(target=simulate_race).start()
    return jsonify(success=True)

@app.route('/race-status', methods=['GET'])
def race_status():
    return jsonify(race_data)

@app.route('/reset-race', methods=['POST'])
def reset_race():
    race_data['is_race_on'] = False
    race_data['horse_positions'] = {}
    race_data['winner'] = None
    race_data['player_bets'] = []
    race_data['results'] = []
    race_data['horse_names'] = generate_random_horse_names(4)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True)
