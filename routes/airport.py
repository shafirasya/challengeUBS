import json
import logging

from flask import request, jsonify
from routes import app


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


logger = logging.getLogger(__name__)


@app.route('/airport', methods=['POST'])
def evaluateAirport():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    results = []
    for item in data:
        arrangedCheckIn = arrangeCheckIn(item)
        results.append(arrangedCheckIn)
    return json.dumps(results)
