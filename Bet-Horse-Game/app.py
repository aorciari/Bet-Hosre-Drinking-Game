from flask import Flask, render_template, request
import random
import time

app = Flask(__name__)

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/race', methods=['POST'])
def race():
    num_players = int(request.form['numPlayers'])
    horse_names = generate_random_horse_names(4)

    return render_template('race.html', num_players=num_players, horse_names=horse_names)




@app.route('/race_results', methods=['POST'])
def race_results():
    num_players = int(request.form['numPlayers'])
    horse_names = request.form.getlist('horse_names')  # Adjust this based on your form structure

    # Simulate the race
    horse_positions = {horse: 0 for horse in horse_names}
    horse_progresses = [0] * len(horse_names)

    while max(horse_positions.values()) < 15:
        time.sleep(1.5)  # Adjust the delay as needed

        for horse in horse_names:
            horse_positions[horse] += random.choice([0, 1])
            horse_progresses[horse_names.index(horse)] = horse_positions[horse]

    # Determine the winning horse
    winning_horse = max(horse_positions, key=horse_positions.get)

    # Retrieve player bets
    player_bets = {}
    for i in range(1, num_players + 1):
        player_name = request.form[f"player{i}"]
        bet_horse = request.form[f"horseBet{i}"]
        bet_drinks = int(request.form[f"drinkBet{i}"])
        player_bets[player_name] = {'horse': bet_horse, 'drinks': bet_drinks}

    return render_template('race_results.html', horse_progresses=horse_progresses, winning_horse=winning_horse, player_bets=player_bets)


if __name__ == "__main__":
    app.run(debug=True)
