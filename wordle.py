from collections import Counter
import math
from tqdm import tqdm
import unicodedata
import matplotlib.pyplot as plt

tr = 'fiveletter.txt'
en = "sgb-words.txt"

with open(tr, 'r', encoding='utf-8') as file:
    words = [kelime.strip() for kelime in file.readlines()]



def calculate_feedback(guess, answer):
    feedback = [''] * len(guess)
    answer_chars_used = [False] * len(answer)  # Track which characters in the answer are used

    # First pass: Handle 'green' (correct letter in the correct position)
    for i in range(len(guess)):
        if guess[i] == answer[i]:
            feedback[i] = 'green'
            answer_chars_used[i] = True

    # Second pass: Handle 'yellow' (correct letter in the wrong position)
    for i in range(len(guess)):
        if feedback[i] == '':  # If not already marked as 'green'
            for j in range(len(answer)):
                if guess[i] == answer[j] and not answer_chars_used[j]:
                    feedback[i] = 'yellow'
                    answer_chars_used[j] = True
                    break

    # Any remaining letters should be 'gray'
    for i in range(len(guess)):
        if feedback[i] == '':
            feedback[i] = 'gray'

    return feedback

letter_frequency = {}

# Calculate frequency of each letter in the word list
for word in words:
    for letter in word:
        if letter in letter_frequency:
            letter_frequency[letter] += 1
        else:
            letter_frequency[letter] = 1

# Sort the frequency list in descending order
sorted_letter_frequency = dict(sorted(letter_frequency.items(), key=lambda item: item[1], reverse=True))

sorted_letter_frequency

# Function to calculate entropy with a progress bar
def calculate_entropy(guess, word_list):
    feedback_counts = Counter()

    for word in word_list:
        feedback = tuple(calculate_feedback(guess, word))
        feedback_counts[feedback] += 1

        

    total_words = len(word_list)
    entropy = 0

    for feedback, count in feedback_counts.items():
        probability = count / total_words
        entropy -= probability * math.log2(probability)

    return entropy

# Function to find and display the top 10 guesses with a progress bar
def find_top_guesses(word_list):
    entropy_scores = []

    for word in tqdm(word_list, desc="Calculating Entropy", colour="blue"):  # Adding a progress bar
        entropy = calculate_entropy(word, word_list)
        entropy_scores.append((word, entropy))

    # Sort by entropy in descending order and get the top 10
    entropy_scores.sort(key=lambda x: x[1], reverse=True)
    top_10_guesses = entropy_scores[:10]

    return top_10_guesses

# Update the word list based on feedback
def update_word_list(guess, feedback, word_list):
    updated_list = []
    for word in word_list:
        if calculate_feedback(guess, word) == feedback:
            updated_list.append(word)
    return updated_list

# Interactive Wordle Solver with top 10 suggestions
def interactive_wordle_solver(word_list):
    step = 0
    word_list_c = word_list[:]
    top_10_guesses_c = find_top_guesses(word_list_c)
    game_is_done = False
    while True:
        step += 1
        if len(word_list_c) == len(word_list):
            top_10_guesses = top_10_guesses_c[:]
        else:
            top_10_guesses = find_top_guesses(word_list_c)
        print("\nTop 10 Suggested Guesses:", f"Step:{step}")
        for word, score in top_10_guesses:
            print(f"{word}: {score:.4f}")

        # User inputs their actual guess and feedback
        user_guess = input("\nEnter your guess: ").strip().lower()
        print(f"\nENTERED USER GUESS: {user_guess}")
        feedback = input("Enter feedback (g for green, y for yellow, x for gray): ").strip().lower()
        print(f"ENTERED USER FEEDBACK: {feedback}\n")

        # Convert feedback to a list format
        feedback_list = []
        for char in feedback:
            if char == 'g':
                feedback_list.append('green')
            elif char == 'y':
                feedback_list.append('yellow')
            else:
                feedback_list.append('gray')

        # Update the word list based on the feedback
        word_list_c = update_word_list(user_guess, feedback_list, word_list_c)

        # If only one word remains, suggest it as the final answer
        if len(word_list_c) == 1:
            print(f"\nThe answer is: {word_list_c[0]}")
            game_is_done = True
        elif not word_list_c:
            print("\nNo words left that match the feedback. Please check your input.")
            game_is_done = True
        
        if game_is_done:
            prompt = input("\nType q for quit, r for restart from beginning")
            
            if prompt == "q":
                break
            if prompt == "r":
                word_list_c = word_list[:]
                step = 0
                game_is_done = False

interactive_wordle_solver(words)

###### SIMULATION

def find_top_guesses_simulation(word_list):
    entropy_scores = []

    for word in word_list:  # Adding a progress bar
        entropy = calculate_entropy(word, word_list)
        entropy_scores.append((word, entropy))

    # Sort by entropy in descending order and get the top 10
    entropy_scores.sort(key=lambda x: x[1], reverse=True)
    top_10_guesses = entropy_scores[:10]

    return top_10_guesses

def simulate_solver_for_word(target_word, word_list):
    steps = 0
    current_word_list = word_list[:]
    
    while True:
        # best_guess = find_top_guesses(current_word_list)[0][0]
        # steps += 1
        if steps == 0:
            best_guess = word_list[0]
            steps += 1
        else:
            best_guess = find_top_guesses_simulation(current_word_list)[0][0]
            steps += 1
        
        if best_guess == target_word:
            return steps 
        
        feedback = calculate_feedback(best_guess, target_word)
        current_word_list = update_word_list(best_guess, feedback, current_word_list)

def calculate_steps_for_all_words(word_list):
    steps_dict = {}
    total = 0

    for word in tqdm(word_list, desc="Calculating Steps for Each Word", ncols=100):
        steps = simulate_solver_for_word(word, word_list)
        steps_dict[word] = steps
        

    return steps_dict, total/len(word_list)

# steps_dict, avg = calculate_steps_for_all_words(kelimeler)
# print("Steps",steps_dict,"Avg:" , avg)
