import random
import tkinter as tk
from tkinter import messagebox
import time
import pygame  # For sound effects

# Initialize Pygame mixer for sound effects
pygame.mixer.init()

# Sound effects
correct_guess_sound = pygame.mixer.Sound("correct_guess.wav")
wrong_guess_sound = pygame.mixer.Sound("wrong_guess.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
win_sound = pygame.mixer.Sound("win_sound.wav")

# Categories and word lists
words = {
    "Easy": ["cat", "dog", "bird", "fish"],
    "Medium": ["elephant", "giraffe", "dolphin", "parrot"],
    "Hard": ["telescope", "neutron", "gladiator", "molecule"],
    "Expert": ["photosynthesis", "neurotransmitter", "infrastructure", "biotechnology"]
}

# Power-up and scoring system
score = 0
hints_used = 0
power_ups = {"extra_guess": 1, "reveal_letter": 1}

# Create main window
root = tk.Tk()
root.title("Advanced Hangman Game")
root.geometry("800x600")
root.config(bg="#2b2b2b")

# Global variables for game state
word = ""
guessed = set()
tries = 6
category = ""
difficulty = ""
timer_running = False

# Function to select a word based on difficulty level
def select_word(difficulty):
    return random.choice(words[difficulty]).lower()

# Function to display hangman based on incorrect guesses
def display_hangman(tries):
    stages = [
        "-------\n |     |\n O     |\n/|\\    |\n/ \\    |\n",
        "-------\n |     |\n O     |\n/|\\    |\n/      |\n",
        "-------\n |     |\n O     |\n/|\\    |\n       |\n",
        "-------\n |     |\n O     |\n/|     |\n       |\n",
        "-------\n |     |\n O     |\n |     |\n       |\n",
        "-------\n |     |\n O     |\n       |\n       |\n",
        "-------\n |     |\n       |\n       |\n       |\n"
    ]
    return stages[tries]

# Timer function
def start_timer():
    global timer_running
    if not timer_running:
        timer_running = True
        countdown(30)

def countdown(countdown_time):
    start_time = time.time()
    while time.time() - start_time < countdown_time:
        remaining_time = countdown_time - int(time.time() - start_time)
        time_label.config(text=f"Time left: {remaining_time} seconds")
        root.update()
        time.sleep(1)
    time_label.config(text="Time's up!")
    messagebox.showinfo("Time's up!", "You ran out of time!")
    reset_game()

# Function to handle power-ups
def use_power_up():
    global power_ups
    if power_ups["extra_guess"] > 0:
        power_ups["extra_guess"] -= 1
        return 1  # Grant extra guess
    elif power_ups["reveal_letter"] > 0:
        power_ups["reveal_letter"] -= 1
        return "hint"  # Grant a hint
    else:
        messagebox.showwarning("No Power-Ups Left", "No power-ups remaining!")
        return None

# Function to handle guess submission
def guess_letter(letter):
    global tries, guessed, word, score
    if letter in guessed:
        return

    guessed.add(letter)
    
    if letter in word:
        correct_guess_sound.play()  # Play correct guess sound
        update_display_word()
    else:
        wrong_guess_sound.play()  # Play wrong guess sound
        tries -= 1
        update_display_hangman()
        if tries == 0:
            game_over_sound.play()  # Play game over sound
            messagebox.showinfo("Game Over", f"Game Over! The word was '{word}'")
            reset_game()

def update_display_word():
    global word
    displayed_word = [letter if letter in guessed else "_" for letter in word]
    word_display.config(text=" ".join(displayed_word))
    
    if "_" not in displayed_word:
        win_sound.play()  # Play win sound
        messagebox.showinfo("Congratulations!", "You guessed the word correctly!")
        score += 10 - hints_used  # Adjusted score for hints used
        score_label.config(text=f"Score: {score}")
        reset_game()

def update_display_hangman():
    hangman_display.config(text=display_hangman(tries))

def reset_game():
    global word, guessed, tries, difficulty, category, hints_used
    guessed.clear()
    tries = 6
    hints_used = 0
    difficulty = ""
    category = ""
    word = ""
    word_display.config(text="_ " * 6)
    hangman_display.config(text="")
    time_label.config(text="Time left: 30 seconds")
    score_label.config(text=f"Score: {score}")
    start_button.config(state="normal")

# Start a new game
def start_game(selected_difficulty):
    global difficulty, word
    difficulty = selected_difficulty
    word = select_word(difficulty)
    update_display_word()
    update_display_hangman()
    start_timer()
    start_button.config(state="disabled")

# Hint and Power-up Handling
def use_hint():
    global hints_used
    hints_used += 1
    available_letters = [letter for letter in word if letter not in guessed]
    hint_letter = random.choice(available_letters)
    hint_label.config(text=f"Hint: A letter in the word is '{hint_letter}'")
    score_label.config(text=f"Score: {score - hints_used}")

# UI Components
title_label = tk.Label(root, text="Advanced Hangman Game", font=("Segoe UI", 32, "bold"), fg="#f4f4f4", bg="#2b2b2b")
title_label.pack(pady=20)

category_label = tk.Label(root, text="Choose Difficulty Level:", font=("Segoe UI", 18), fg="#f4f4f4", bg="#2b2b2b")
category_label.pack()

easy_button = tk.Button(root, text="Easy", font=("Segoe UI", 14), bg="#4CAF50", fg="white", command=lambda: start_game("Easy"))
easy_button.pack(pady=5, fill=tk.X)

medium_button = tk.Button(root, text="Medium", font=("Segoe UI", 14), bg="#2196F3", fg="white", command=lambda: start_game("Medium"))
medium_button.pack(pady=5, fill=tk.X)

hard_button = tk.Button(root, text="Hard", font=("Segoe UI", 14), bg="#FF9800", fg="white", command=lambda: start_game("Hard"))
hard_button.pack(pady=5, fill=tk.X)

expert_button = tk.Button(root, text="Expert", font=("Segoe UI", 14), bg="#F44336", fg="white", command=lambda: start_game("Expert"))
expert_button.pack(pady=5, fill=tk.X)

word_display = tk.Label(root, text="_ " * 6, font=("Segoe UI", 24, "bold"), fg="#FFC107", bg="#2b2b2b")
word_display.pack(pady=30)

hangman_display = tk.Label(root, text="", font=("Courier New", 16), fg="#f4f4f4", bg="#2b2b2b")
hangman_display.pack()

time_label = tk.Label(root, text="Time left: 30 seconds", font=("Segoe UI", 14), fg="#f4f4f4", bg="#2b2b2b")
time_label.pack(pady=10)

score_label = tk.Label(root, text=f"Score: {score}", font=("Segoe UI", 16), fg="#f4f4f4", bg="#2b2b2b")
score_label.pack()

hint_label = tk.Label(root, text="Hint: ", font=("Segoe UI", 12), fg="#FFC107", bg="#2b2b2b")
hint_label.pack()

# Create letter buttons dynamically with modern aesthetics
button_frame = tk.Frame(root, bg="#2b2b2b")
button_frame.pack(pady=30)

for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    button = tk.Button(button_frame, text=letter, width=3, height=2, font=("Arial", 14), bg="#424242", fg="white", command=lambda letter=letter: guess_letter(letter))
    button.pack(side=tk.LEFT, padx=5)

# Game Controls
start_button = tk.Button(root, text="Start New Game", font=("Segoe UI", 16), bg="#4CAF50", fg="white", command=lambda: start_game(difficulty))
start_button.pack(pady=20)

# Mainloop to run the game
root.mainloop()
