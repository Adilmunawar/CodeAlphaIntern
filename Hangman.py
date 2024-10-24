import random
import time
import os

# Color codes for animations
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"

# Progressive hangman stages with more detailed animations
hangman_stages = [
    f"""
       {CYAN}------
       |    |
            |
            |
            |
            |
    ---------{RESET}
    """,
    f"""
       {CYAN}------
       |    |
       O    |
            |
            |
            |
    ---------{RESET}
    """,
    f"""
       {CYAN}------
       |    |
       O    |
       |    |
            |
            |
    ---------{RESET}
    """,
    f"""
       {CYAN}------
       |    |
       O    |
      /|    |
            |
            |
    ---------{RESET}
    """,
    f"""
       {CYAN}------
       |    |
       O    |
      /|\\   |
            |
            |
    ---------{RESET}
    """,
    f"""
       {CYAN}------
       |    |
       O    |
      /|\\   |
      /     |
            |
    ---------{RESET}
    """,
    f"""
       {CYAN}------
       |    |
       O    |
      /|\\   |
      / \\   |
            |
    ---------{RESET}
    """
]

# Clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Animated word reveal
def animated_word_reveal(word, correct=True):
    color = GREEN if correct else RED
    for letter in word:
        print(color + letter + RESET, end=' ', flush=True)
        time.sleep(0.3)
    print("\n")

# Display hangman with fancy animation
def display_hangman(attempts):
    clear_screen()
    print(f"{YELLOW}{BOLD}Hangman Game{RESET}")
    print(hangman_stages[attempts])

# Get random word from a difficulty level
def get_random_word(difficulty):
    word_categories = {
        "Easy": ['apple', 'banana', 'grape', 'orange'],
        "Medium": ['python', 'hangman', 'database', 'interface'],
        "Hard": ['programming', 'developer', 'cryptography', 'algorithms']
    }
    return random.choice(word_categories[difficulty])

# Hangman game logic with animations and enhanced features
def hangman():
    clear_screen()

    # Choose difficulty with validation
    print(f"{BLUE}{BOLD}Choose Difficulty:{RESET} Easy, Medium, Hard")
    while True:
        difficulty = input("Enter difficulty level: ").capitalize()
        if difficulty in ['Easy', 'Medium', 'Hard']:
            break
        else:
            print(f"{RED}Invalid choice, try again!{RESET}")

    word = get_random_word(difficulty)
    guessed_word = ['_'] * len(word)
    guessed_letters = []
    max_attempts = 6
    attempts = 0
    hint_used = False
    score = 0

    print(f"\n{BOLD}Word Length: {len(word)}{RESET}")
    print(f"{YELLOW}Start guessing the word!{RESET}")

    while attempts < max_attempts:
        display_hangman(attempts)

        # Print guessed word status
        print("\nCurrent Word: ", end='')
        print(' '.join(guessed_word))

        # Guess input from user
        guess = input("\nGuess a letter (or type 'hint' for a hint): ").lower()

        # Hint functionality
        if guess == 'hint' and not hint_used:
            hint_letter = random.choice([char for char in word if char not in guessed_letters])
            print(f"{GREEN}Hint: The word contains the letter '{hint_letter}'{RESET}")
            guessed_letters.append(hint_letter)
            hint_used = True
            continue
        elif guess == 'hint' and hint_used:
            print(f"{RED}Hint already used!{RESET}")
            continue

        # Check if the letter was already guessed
        if guess in guessed_letters:
            print(f"{RED}You've already guessed '{guess}'. Try again!{RESET}")
            continue
        
        guessed_letters.append(guess)

        # Letter found
        if guess in word:
            print(f"{GREEN}Great! '{guess}' is in the word!{RESET}")
            for i in range(len(word)):
                if word[i] == guess:
                    guessed_word[i] = guess
        else:
            print(f"{RED}Oops! '{guess}' is not in the word!{RESET}")
            attempts += 1
            print(f"{YELLOW}You have {max_attempts - attempts} attempts left.{RESET}")

        # Check if word is fully guessed
        if '_' not in guessed_word:
            animated_word_reveal(word)
            print(f"\n{GREEN}{BOLD}Congratulations! You guessed the word correctly!{RESET}")
            score += 100 - (attempts * 10)
            print(f"{YELLOW}Your score: {score}{RESET}")
            break
    else:
        # Game over scenario
        print(f"\n{RED}{BOLD}Game Over! You ran out of attempts!{RESET}")
        print(f"The correct word was: ", end='')
        animated_word_reveal(word, correct=False)

    # Replay option
    replay = input("\nDo you want to play again? (yes/no): ").lower()
    if replay == 'yes':
        hangman()

# Run the game
if __name__ == "__main__":
    hangman()
