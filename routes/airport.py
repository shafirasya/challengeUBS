# import json
# import logging

# from flask import request, jsonify
# from routes import app


# Simple passenger class
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
        passenger for passenger in listPassengers if passenger.askTimeToDeparture() >= cutoff_time]
    sortedPassengers = sorted(
        sortedPassengers, key=lambda passenger: passenger.askTimeToDeparture())
    # print('listAfter: ', sortedPassengers)
    return sortedPassengers

# def prioritizeQueue(listPassengers, cut_off_time):
#     if len(listPassengers) <= 1:
#         if(listPassengers[0].askTimeToDeparture() < cut_off_time ):
#             return []
#         else:
#             return listPassengers

#     # Divide the array into two halves
#     mid = len(listPassengers) // 2
#     left_half = listPassengers[:mid]
#     right_half = listPassengers[mid:]

#     # Recursively sort the two halves
#     left_sorted = prioritizeQueue(left_half, cut_off_time)
#     right_sorted = prioritizeQueue(right_half, cut_off_time)

#     # Merge the sorted halves
#     return merge(left_sorted, right_sorted)

# def merge(left, right):
#     sortedPassengers = []
#     left_index = right_index = 0

#     # Compare elements from both halves and merge them in sorted order
#     while left_index < len(left) and right_index < len(right):
#         if left[left_index].askTimeToDeparture() <= right[right_index].askTimeToDeparture():
#             sortedPassengers.append(left[left_index])
#             left_index += 1
#         else:
#             sortedPassengers.append(right[right_index])
#             right_index += 1

#     # Append the remaining elements from the unfinished half
#     sortedPassengers.extend(left[left_index:])
#     sortedPassengers.extend(right[right_index:])

#     return sortedPassengers

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


# logger = logging.getLogger(__name__)


# @app.route('/airport', methods=['POST'])
# def evaluateAirport():
#     data = request.get_json()
#     logging.info("data sent for evaluation {}".format(data))
#     results = []
#     for item in data:
#         arrangedCheckIn = arrangeCheckIn(item)
#         results.append(arrangedCheckIn)
#     return json.dumps(results)

sample_data = [
    {
        "id": "fc5fdbc0-551d-4099-b7e6-f59e27b238dc", 
        "departureTimes": [1, 2, 3, 4, 5, 6], 
        "cutOffTime": 2 
    },
    {
        "id": "fc5fdbc0-551d-4099-b7e6-f59e27b238dd", 
        "departureTimes": [1, 2, 3, 4, 5, 6], 
        "cutOffTime": 1 
    },
    {
        "id": "fc5fdbc0-551d-4099-b7e6-f59e27b238de", 
        "departureTimes": [1, 2, 3, 4, 5, 6], 
        "cutOffTime": 3 
    },
    {
        "id": "fc5fdbc0-551d-4099-b7e6-f59e27b238df", 
        "departureTimes": [1, 2, 3, 4, 5, 6], 
        "cutOffTime": 4
    },
    {
        "id": "fc5fdbc0-551d-4099-b7e6-f59e27b238dg", 
        "departureTimes": [1, 2, 3, 4, 5, 6], 
        "cutOffTime": 10 
    }
]

results = []
for item in sample_data:
    arrangedCheckIn = arrangeCheckIn(item)
    results.append(arrangedCheckIn)

print(results)
