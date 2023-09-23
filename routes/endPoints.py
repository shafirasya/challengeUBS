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
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def combo(data):
    combinations = []

    for d in data:
        values = d.split(', ')
        railway_length = int(values[0])
        num_track_pieces = int(values[1])
        track_lengths = [int(x) for x in values[2:]]
        @lru_cache(maxsize=None)
        def count_combinations(curr_length, idx):
            if idx == num_track_pieces:
                if curr_length == railway_length:
                    return 1
                else:
                    return 0
            total_combinations = 0
            if curr_length + track_lengths[idx] <= railway_length:
                total_combinations += count_combinations(curr_length + track_lengths[idx], idx)
            total_combinations += count_combinations(curr_length, idx + 1)
            return total_combinations
        combinations.append(count_combinations(0, 0))
    return combinations


@app.route('/calendar-scheduling', methods=['POST'])
def calendar_scheduling():
    data = request.get_json()
    results = schedule_lessons(data)
    return jsonify(results)
    

def schedule_lessons(lessonList):
    lesson_requests = lessonList
    # Sort the lesson requests in descending order of potential earnings
    lesson_requests.sort(key=lambda x: x['potentialEarnings'], reverse=True)
    # Initialize the schedule dictionary
    schedule = {}
    # Initialize the total earnings
    total_earnings = 0
    # Map to track duration per day
    durationPerDay = {}
    # Iterate over the lesson requests
    for lesson_request in lesson_requests:
        lesson_id = lesson_request['lessonRequestId']
        duration = lesson_request['duration']
        earnings = lesson_request['potentialEarnings']
        available_days = lesson_request['availableDays']
        # If duration already exceed, exclude
        if duration > 12:
            continue
        # Find the first available day with enough hours for the lesson
        scheduled_day = None
        for day in available_days:
            if day not in schedule:
                schedule[day] = []
                durationPerDay[day] = 0
            if durationPerDay[day] + duration <= 12:
                scheduled_day = day
                break      
        # Schedule the lesson if an available day is found
        if scheduled_day is not None:
            schedule[scheduled_day].append(lesson_id)
            durationPerDay[scheduled_day] += duration
            total_earnings += earnings
    # Return the schedule and total earnings as the response
    return schedule


# Digital Colony Solutions
def calculateWeightOverGeneration(data):
    results = []
    for item in data:
        generations = item['generations']
        colony = item['colony']

        pair = [[i - j if i >= j else i + 10 - j for j in range(10)] for i in range(10)]

        cpair = [[0 for j in range(10)] for i in range(10)]
        s = [0 for i in range(10)]

        c = [int(i) for i in colony]

        for i in range(len(c) - 1):
            cpair[c[i]][c[i + 1]] += 1
        for i in range(len(c)):
            s[c[i]] += 1
        tot = 0
        for i in range(51):
            total = sum([s[j] * j for j in range(10)])
            if i == generations:
                tot = total
                break
            tmpair = [[0 for k in range(10)] for j in range(10)]
            mod = total % 10
            for j in range(10):
                for k in range(10):
                    if cpair[j][k] > 0:
                        gen = (pair[j][k] + mod) % 10
                        s[gen] += cpair[j][k]
                        tmpair[j][gen] += cpair[j][k]
                        tmpair[gen][k] += cpair[j][k]
            cpair = tmpair
        results.append(str(tot))
    return results


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

# Calendar Scheduling Solution

def schedule_lessons(lessonList):
    lesson_requests = lessonList
    
    # Sort the lesson requests in descending order of potential earnings
    lesson_requests.sort(key=lambda x: x['potentialEarnings'], reverse=True)
    
    # Initialize the schedule dictionary
    schedule = {}
    
    # Initialize the total earnings
    total_earnings = 0

    # Map to track duration per day
    durationPerDay = {}
    
    # Iterate over the lesson requests
    for lesson_request in lesson_requests:
        lesson_id = lesson_request['lessonRequestId']
        duration = lesson_request['duration']
        earnings = lesson_request['potentialEarnings']
        available_days = lesson_request['availableDays']

        # If duration already exceed, exclude
        if duration > 12:
            continue

        # Find the first available day with enough hours for the lesson
        scheduled_day = None
        for day in available_days:
            if day not in schedule:
                schedule[day] = []
                durationPerDay[day] = 0
            if durationPerDay[day] + duration <= 12:
                scheduled_day = day
                break
        
        # Schedule the lesson if an available day is found
        if scheduled_day is not None:
            schedule[scheduled_day].append(lesson_id)
            durationPerDay[scheduled_day] += duration
            total_earnings += earnings
    
    # Return the schedule and total earnings as the response
    return schedule

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
    logging.info("data sent for evaluation {}".format(data))

    results = calculateWeightOverGeneration(data)
    return json.dumps(results)


@app.route('/airport', methods=['POST'])
def airport_checkin():
    data = request.get_json()

    results = []
    for item in data:
        arrangedCheckIn = arrangeCheckIn(item)
        results.append(arrangedCheckIn)

    return json.dumps(results)

@app.route('/maze', methods=['POST'])
def maze():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = move(data)
    logging.info("My result :{}".format(result))
    return jsonify(result)

def move(data):
    global mp, dir, new_arr
    nearby = data['nearby']
    for i in range(4):
        if nearby[mp[(dir + i) % 4][0]][mp[(dir + i) % 4][1]] != 0:
            dir = (dir + i) % 4
            break
    action = new_arr[dir]
    return {"playerAction": action}