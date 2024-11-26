# Author: Isac Polasak
# CS 361
# Main Project: Quiz Program
# Description: If the user's word is in the list of words,
# it returns the definition. Otherwise it returns an error message.

import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5557")

def looker_upper(word_to_find, word_list):
    definition = f"{word_to_find} was not found in the list of words."
    for word in word_list:
        if word.lower() == word_to_find.lower():
            actual_def = word_list[word]
            definition = f'The definition of {word_to_find} is "{actual_def}".'
            return definition
    return definition


while True:
    print("Receiving word and list of words...")
    request = socket.recv_json()
    print("Request received. Checking if word is in the list of words.")
    word_to_check, word_dictionary = request  # Separate the word and the list of words.
    definition = looker_upper(word_to_check, word_dictionary)
    socket.send_json(definition)
    print("Sending results back to main program.")
