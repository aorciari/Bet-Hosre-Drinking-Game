import random
import time

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

def get_player_bets(num_players, horse_names):
    player_bets = {}

    for i in range(1, num_players + 1):
        player_name = input(f"Enter name for Player {i}: ")
        valid_horses = '\n'.join(f"{index + 1}. {horse}" for index, horse in enumerate(horse_names))
        bet_horse_index = int(input(f"{player_name}, choose a horse to bet on (enter the corresponding number):\n{valid_horses}\n")) - 1

        if bet_horse_index < 0 or bet_horse_index >= len(horse_names):
            print("Invalid horse selection. Try again.")
            return get_player_bets(num_players, horse_names)

        bet_horse = horse_names[bet_horse_index]

        # Ask the player for the number of drinks to bet
        bet_drinks = int(input(f"How many drinks do you want to bet, {player_name}? "))
        player_bets[player_name] = {'horse': bet_horse, 'drinks': bet_drinks}

    return player_bets

def race(num_players):
    print("Welcome to the Horse Race Game!")

    # Generate random names for the horses
    horse_names = generate_random_horse_names(4)

    # Shuffle the horses to randomize the race
    random.shuffle(horse_names)

    print("\nHorses in the race:")
    for index, horse in enumerate(horse_names):
        print(f"{index + 1}. {horse}")

    player_bets = get_player_bets(num_players, horse_names)

    print("\nAnd they're off!")

    # Initialize horse positions
    horse_positions = {horse: 0 for horse in horse_names}

    # Simulate the race
    while max(horse_positions.values()) < 16:
        time.sleep(1.5)  # Add a delay for visualization
        print("\nRace Progress:")
        for horse in horse_names:
            progress = '#' * horse_positions[horse]
            print(f"{horse}: {progress} ({horse_positions[horse]})")

            # Randomly update each horse's position
            horse_positions[horse] += random.choice([0, 1])

    # Determine the winner
    winning_horse = max(horse_positions, key=horse_positions.get)
    print("\nRace Results:")
    print(f"The winning horse is: {winning_horse}")

    print("\nBetting Results:")
    for player, bet_info in player_bets.items():
        if bet_info['horse'] == winning_horse:
            drinks_won = bet_info['drinks'] * 2
            print(f"{player} wins the bet on {winning_horse} and gets {drinks_won} drinks!")
        else:
            drinks_lost = bet_info['drinks']
            print(f"{player} loses the bet and takes {drinks_lost} drinks. Better luck next time!")

if __name__ == "__main__":
    num_players = int(input("Enter the number of players: "))
    race(num_players)
