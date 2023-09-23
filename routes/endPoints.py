import logging
import socket
from routes import app
from flask import Flask, request, jsonify, json
from typing import Dict, List
from functools import lru_cache

from routes import app

logger = logging.getLogger(__name__)

@app.route('/lazy-developer', methods=['POST'])
def evaluateLazyDeveloper():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    classes = data['classes']
    statements = data['statements']
    result = getNextProbableWords(classes, statements)
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def getNextProbableWords(classes: List[Dict], statements: List[str]) -> Dict[str, List[str]]:
    result = {}
    cdict = {k: v for ci in classes for k, v in ci.items()}

    for x in statements:
        result[x] = []
        l = x.split('.')
        first_sub = l[0]
        second_sub = l[1] if len(l) > 1 else ""

        if first_sub in cdict:
            if isinstance(cdict[first_sub], dict) and second_sub != "":
                klist = cdict[first_sub].keys()
                for j in klist:
                    if j.find(second_sub) != -1 and not cdict[first_sub][j].startswith('List'):
                        result[x].append(j)
            else:
                klist = cdict[first_sub]
                for j in klist:
                    if j.find(second_sub) != -1:
                        result[x].append(j)

        result[x].sort()
        if result[x] == []:
            result[x] = ['']
        final = result[x]
        if len(final) > 5:
            result[x] = final[:5]

    return result





@app.route('/greedymonkey', methods=['POST'])
def evaluateGreedyMonkey():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    w = data['w']
    v = data['v']
    f = data['f']
    result = calculate_maximum_value(w, v, f)
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def calculate_maximum_value(weight_limit, value_limit, items):
    memo = {}

    def dynamic_programming(curr_weight, curr_value, index):
        if index == len(items):
            return 0

        if (curr_weight, curr_value, index) in memo:
            return memo[(curr_weight, curr_value, index)]

        max_value = 0
        if curr_weight + items[index][0] <= weight_limit and curr_value + items[index][1] <= value_limit:
            max_value = max(max_value, items[index][2] + dynamic_programming(curr_weight + items[index][0], curr_value + items[index][1], index + 1))
        max_value = max(max_value, dynamic_programming(curr_weight, curr_value, index + 1))

        memo[(curr_weight, curr_value, index)] = max_value
        return max_value

    return dynamic_programming(0, 0, 0)

@app.route("/railway-builder", methods=['POST'])
def railway_builder():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = combo(data)
    logging.info("My result :{}".format(res))
    return json.dumps(result)

def total_combo(railway_length, track_types, track_lengths):
    combinations = [[0] * (railway_length + 1) for _ in range(track_types + 1)]
    combinations[0][0] = 1

    for i in range(1, track_types + 1):
        combinations[i][0] = 1

        for j in range(1, railway_length + 1):
            if j < track_lengths[i - 1]:
                combinations[i][j] = combinations[i - 1][j]
            else:
                combinations[i][j] = combinations[i - 1][j] + combinations[i][j - track_lengths[i - 1]]

    return combinations[track_types][railway_length]

def combo(data):
    result = []
    for d in data:
        values = list(map(int, d.split(",")))
        railway_length = values[0]
        num_track_types = values[1]
        track_lengths = values[2:]
        result.append(total_combo(railway_length, num_track_types, track_lengths))
    return result

# Digital Colony Solutions


def calculateWeightOverGeneration(colony, generation):
    # Convert colony to a list of digits
    colony_digits = list(map(int, str(colony)))

    for gen in range(generation):
        currentGenWeight = sum(colony_digits)

        # Initialize a new colony list
        new_colony = []

        # Iterate over pairs of digits in the colony
        for i in range(len(colony_digits) - 1):
            digit1 = colony_digits[i]
            digit2 = colony_digits[i + 1]

            # Calculate the signature of the pair
            signature = 0
            if digit1 != digit2:
                diff = digit1 - digit2
                signature = 10 + diff if diff < 0 else diff

            # Calculate the sum of weight and signature
            digit_sum = currentGenWeight + signature

            # Append the last digit of the sum to the new colony
            if (i == 0):
                new_colony.append(digit1)
            new_colony.append(digit_sum % 10)
            new_colony.append(digit2)

        # Update the colony digits with the new colony
        colony_digits = new_colony

    # Calculate the weight of the final colony
    finalcolonyWeight = sum(colony_digits)

    print(finalcolonyWeight)

    return str(finalcolonyWeight)

# Airport CheckIn Solutions


class Passenger:

    def __init__(self, departureTime):
        self.departureTime = departureTime
        self.numberOfRequests = 0

    def askTimeToDeparture(self):
        self.numberOfRequests += 1
        return self.departureTime

    def getNumberOfRequests(self):
        return self.numberOfRequests


def prioritizeQueue(listPassengers, cutoff_time):
    # print('list: ', listPassengers)
    sortedPassengers = [
        passenger for passenger in listPassengers if passenger.askTimeToDeparture() <= cutoff_time]
    sortedPassengers = sorted(
        sortedPassengers, key=lambda passenger: passenger.departureTime)
    # print('listAfter: ', sortedPassengers)
    return sortedPassengers


def execute(passenger_data, cut_off_time):
    totalNumberOfRequests = 0
    passengers = []

    # Initialise list of passenger instances
    for i in range(len(passenger_data)):
        passengers.append(Passenger(passenger_data[i]))

    # Apply solution and re-shuffle with departure cut-off time
    prioritised_and_filtered_passengers = prioritizeQueue(
        passengers, cut_off_time)

    # Sum totalNumberOfRequests across all passengers
    for i in range(len(passengers)):
        totalNumberOfRequests += passengers[i].getNumberOfRequests()
    print("totalNumberOfRequests: " + str(totalNumberOfRequests))

    # Print sequence of sorted departure times
    print("Sequence of prioritised departure times:")
    prioritised_filtered_list = []
    for i in range(len(prioritised_and_filtered_passengers)):
        print(prioritised_and_filtered_passengers[i].departureTime, end=" ")
        prioritised_filtered_list.append(
            prioritised_and_filtered_passengers[i].departureTime)

    print("\n")
    return {
        "total_number_of_requests": totalNumberOfRequests,
        "prioritised_filtered_list": prioritised_filtered_list
    }


def arrangeCheckIn(testCase):
    result = execute(testCase["departureTimes"], testCase["cutOffTime"])
    return {
        "id": testCase['id'],
        "sortedDepartureTimes": result['prioritised_filtered_list'],
        "numberOfRequests": result['total_number_of_requests']
    }


@app.route('/square', methods=['POST'])
def square():
    logging.info('entering square..')
    data = request.get_json()
    x = data.get('input')
    res = x*x
    return json.dumps(res)


@app.route('/digital-colony', methods=['POST'])
def digital_colony():
    logging.info('enter digital colony')
    data = request.get_json()
    print

    results = []
    for item in data:
        generations = item["generations"]
        colony = item["colony"]
        weight = calculateWeightOverGeneration(colony, generations)
        results.append(weight)

    return jsonify(results)


@app.route('/airport', methods=['POST'])
def airport_checkin():
    data = request.get_json()

    results = []
    for item in data:
        arrangedCheckIn = arrangeCheckIn(item)
        results.append(arrangedCheckIn)

    return jsonify(results)



@app.route('/maze', methods=['POST'])
def maze():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    where_move = move(data)
    return json.dumps(where_move)

def move(data):
    nearby = data.get("nearBy", [])
    is_previous_movement_valid = data.get("isPreviousMovementValid", False)

    # Define order of preference for directions
    directions = ["up", "right", "down", "left"]
    nearby_values = [
        nearby[0][1] if len(nearby) > 0 else None,  # Up
        nearby[1][2] if len(nearby) > 1 else None,  # Right
        nearby[2][1] if len(nearby) > 2 else None,  # Down
        nearby[1][0] if len(nearby) > 1 else None  # Left
    ]

    for direction, value in zip(directions, nearby_values):
        if value == 3:
            return direction

    for direction, value in zip(directions, nearby_values):
        if value == 1:
            return direction

    if not is_previous_movement_valid:
        return "respawn"

    return "stay"