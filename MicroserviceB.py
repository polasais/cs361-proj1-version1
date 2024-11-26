# Author: Isac Polasak
# CS 361
# Main Project: Quiz Program
# Description: Given that the user is on the homepage of the main program, when they type "check”,
# then a prompt will come up for the word and a True or False will be returned if the word is in the list.
# This microservice performs the search for the word.

import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def word_checker(word_to_find, word_list):
    """Checks if the word is in the word list and returns the results back to the main program."""
    found = False
    for word in word_list:
        if word.lower() == word_to_find.lower():
            found = True
    return found


# loop to see if a request was sent from the main program.
while True:
    print("Receiving request...")
    word_lookup_request = socket.recv_json()
    word_to_find, word_list = word_lookup_request
    print("Request received. Checking if word is in the list of words.")
    word_lookup_response = word_checker(word_to_find, word_list)
    print("Sending results back to main program.")
    socket.send_json(word_lookup_response)