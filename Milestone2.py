# Isac Polasak"
# CS 361
# Milestone 1 project, part 1 version 1

import random
import time
import json
import os

class Project1:
    def __init__(self):
        self.word_dictionary = {
            "Alacrity": "Liveliness and eagerness.",
            "Alliteration": "When the first letter of a word is repeated more than once.",
            "Aberration": "A temporary change form the usual way of behaving.",
            "Respite": "A short period of rest.",
            "Quintessential": "Representing the most perfect or typical example of a quality or class",
            "Furtive": "Attempting to avoid notice or attention; secretive.",
            "Judicious": "Using or showing good judgement; wise; sensible.",
            "Impudent": "Rude; not showing respect for other people; impertinent.",
            "Brazen": "Obvious; without any attempt to be hidden.",
            "Unrequited": "Not returned.",
            "Cacophony": "Loud confusing disagreeable sounds often at loud volume.",
            "Acrimony": "Bitterness; ill feeling.",
            "Brusque": "Quick and rude in manner or speech.",
            "Deferential": "Showing deference; respectful.",
            "Erudite": "Containing a lot of knowledge that is known by very few people.",
            "Perilous": "Risk.",
            "Incandescent": "Emitting light as a result of being heated.",
            "Disparage": "To belittle; speak slightly of; to undervalue.",
            "Traipse": "To walk about without purpose or to walk about in a tired and reluctant way.",
            "Scintillating": "When something is sparkling or shining brightly."
        }
        self.high_score = 0


    def greeting(self):
        print("Welcome to the Ultimate Vocabulary Quiz!")
        return self.greetings_helper()

    def greetings_helper(self):
        """Makes it so that user doesn't get the welcome msg every time action is taken."""
        input_msg = input("""
        Type “word” to test your vocabulary. 
        Type “exit” to end this program. 
        Type “add” to add new words to the dictionary. 
        Type “tips” for some tips on this program.
        Type "HS" for your high score.
        What is your choice?: 
        """)

        if input_msg.lower() == "exit":
            self.program_close()
        if input_msg.lower() == "tips":
            self.tips()
        if input_msg.lower() == "add":
            self.add_word()
        if input_msg.lower() == "word":
            self.quiz()
        if input_msg.lower() == "hs":
            self.streak_request()

    def quiz(self):
        # Initialize a new quiz
        self.word, self.definition = random.choice(list(self.word_dictionary.items()))
        print("You can type 'Skip' to skip this word, or 'remove' to remove it from the list of words.")
        print(f"Your word is {self.word}.")

        # Create a list of 4 random definitions.
        self.list_of_defs = [self.definition]
        while len(self.list_of_defs) < 4:
            random_word, random_definition = random.choice(list(self.word_dictionary.items()))
            if random_definition not in self.list_of_defs:
                self.list_of_defs.append(random_definition)
        random.shuffle(self.list_of_defs)
        self.ask_question()

    def ask_question(self):
        print("Which of the following is its correct definition?")
        for index, defs in enumerate(self.list_of_defs):
            print(f"{index + 1}. {defs}")
        time.sleep(1)
        user_guess = input("What is your guess, 1, 2, 3, or 4?: ")
        self.check_answer(user_guess)

    def streak_send(self, score):
        """Automatically sends a new high score to the microservice.
           The microservice replaces HS if it's greater than current HS."""
        with open('request.json', 'w') as hiscore_file:
            # Dump in the new High Score as a request.json file with action: 0 (0 = update High Score)
            json.dump({"streak": score, "action": 0}, hiscore_file)
        return self.quiz()
    def streak_request(self):
        """Requests the streak from the Microservice."""
        print("Sending request to microservice...")
        with open('request.json', 'w') as hiscore_file:
            # Any number is fine for streak, but action = 1 (1 = return score as response.json)
            json.dump({"streak": 100, "action": 1}, hiscore_file)

        for _ in range(10):  # Poll for up to 10 seconds
            if os.path.exists('response.json'):
                break
            time.sleep(1)  # Wait 1 second before checking again
        else:
            print("Error: response.json was not created in time.")
            return

        # Open the response.json which will contain "{"high_score": xx}" where xx is the HS as an integer.
        with open('response.json', 'r') as hiscore_file:
            data = json.load(hiscore_file)
            # If the file is not empty, print the high score and delete the response file.
            if "high_score" in data:
                print(f'Your current high score is: {data["high_score"]}')
            else:
                print("Error: High score is not found")
            os.remove('response.json')
        return
    def check_answer(self, user_guess):
        """Checks if the user's guess is correct."""
        if user_guess.isdigit() and 1 <= int(user_guess) <= 4:
            if self.list_of_defs[int(user_guess) - 1] == self.definition:
                print("Congrats! You got the word right!")
                self.high_score += 1
                self.streak_send(self.high_score)
            else:
                print("Sorry, that's not correct. Try again.")
                self.high_score = 0
                self.ask_question()
                # Allows the user to try again without resetting definitions
        elif user_guess.lower() == "skip":
            print("You chose to skip this word.")
            time.sleep(1)
            self.quiz()
            # Starts a new quiz
        elif user_guess.lower() == "remove":
            self.remove_word(self.definition)
            # Removes the word from the dictionary.
        elif user_guess.lower() == "exit":
            self.program_close()
        else:
            print("Invalid input. Please enter a number between 1 and 4.")
            time.sleep(1)
            self.ask_question()
            # Prompts the user again for valid input

    def program_close(self):
        print("Thank you for using this program! Have a great day!")
        return
    def add_word(self):
        """Adds a word to the dictionary of words by asking first for the word then its definition."""
        print("First, type in the word you'd like to add, then its definition.")
        input_word = input("What is the word? ")
        if input_word in self.word_dictionary:
            print(f"{input_word} is already in the list of words.")
            return
        input_def = input("And its definition? ")
        time.sleep(1)
        self.word_dictionary[input_word] = input_def
        print(f"Congratulations! {input_word} has been added to the list of words.")
        time.sleep(1)
        self.greetings_helper()

    def remove_word(self, definition):
        """Removes a given word from the catalog of words."""
        print("Note: This action will permanently remove the word from the list of words.")
        user_choice = input("Are you sure you want to continue? Type 'Yes' for yes and 'No' for no: ")
        if user_choice.lower() == 'yes':
            word_to_remove = [key for key, value in self.word_dictionary.items() if value == definition]
            definition_final = definition
            self.word_dictionary.pop(word_to_remove[0])
            print("The word has been removed from the list of words.")
            final_choice = input("Do you regret that choice? Type 'Yes' to add the word back, or 'No' to leave it out: ")
            if final_choice.lower() == 'yes':
                self.word_dictionary[word_to_remove[0]] = definition_final
                print(f"{word_to_remove[0]} has been added back to the dictionary.")
            elif final_choice.lower() == 'no':
                print(f"You made your choice. {word_to_remove[0]} has been removed from the list of words.")
            else:
                print("Invalid choice.")
        elif user_choice.lower() == 'no':
            print("Good choice! Keep studying these words.")
        else:
            print("Invalid choice.")
        self.greetings_helper()
    def tips(self):
        """Prints some tips for the user."""
        print("""
        Tip 1: You can add words in your target language along with its English definition to help you learn new languages.
        Tip 2: You can add vocabulary for your GSCEs and other official exams to help you study for those.
        Tip 3: You can even use it as a practice multiple choice quiz for your classes.
        """)
        self.greetings_helper()

if __name__ == "__main__":
    project = Project1()  # Create an instance of Project1
    project.greeting()     # Call the greeting method to start the program
