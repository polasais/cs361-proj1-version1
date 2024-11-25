import json
import os

input_file = "request.json"
output_file = "response.json"
high_score_file = "high_score.json"

if not os.path.exists(high_score_file):
    with open(high_score_file, "w") as file:
        json.dump({"high_score": 0}, file)

def read_request():
    """Read request from the input JSON file."""
    if os.path.exists(input_file):
        try:
            with open(input_file, "r") as file:
                data = file.read()
                if data.strip():  # check that file is not empty
                    return json.loads(data)
        except json.JSONDecodeError:
            print("Invalid JSON format in request.json")
    return None

def write_response(data):
    """Write response to the output JSON file."""
    with open(output_file, "w") as file:
        json.dump(data, file)

def update_high_score(streak):
    """Update high score if the streak is greater."""
    with open(high_score_file, "r+") as file:
        high_score_data = json.load(file)
        if streak > high_score_data["high_score"]:
            high_score_data["high_score"] = streak
            file.seek(0)
            file.truncate()
            json.dump(high_score_data, file)

def get_high_score():
    """Retrieve the high score."""
    with open(high_score_file, "r") as file:
        return json.load(file)["high_score"]

print("Microservice is running...")
while True:
    request = read_request()
    if request:
        action = request.get("action")
        streak = request.get("streak")

        if action == 1:
            high_score = get_high_score()
            print(f"Action: {action}, Writing high score to response.json: {high_score}")
            write_response({"high_score": high_score})
        elif action == 0:
            print(f"Action: {action}, Updating high score with streak: {streak}")
            update_high_score(streak)
        else:
            print(f"unexpected action")
        # delete the request file to process only once
        os.remove(input_file)