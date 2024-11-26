# Author: Isac Polasak
# CS 361
# Main Project: Quiz Program
# Description: Keeps track of the words a user skipped. It returns the list once the user requests it.

import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5556")

skipped_list = []

def add_word(skipped_list, word):
    """Adds the skipped word to the list of words that the user skipped."""
    skipped_list.append(word)


while True:
    # Keeps checking to see if it got sent a request.
    print("Receiving word...")
    request = socket.recv_json()
    if request == "list":
        print("Request received. Sending back list of words.")
        socket.send_json(skipped_list)
    else:
        print("Request received. Adding skipped word to list of words skipped.")
        add_word(skipped_list, request)
        response = "word skipped"
        socket.send_json(response)
