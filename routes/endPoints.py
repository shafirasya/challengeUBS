import json
import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

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
        if(i==0):
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
    #print('list: ', listPassengers)
    sortedPassengers = [passenger for passenger in listPassengers if passenger.askTimeToDeparture() <= cutoff_time]
    sortedPassengers = sorted(sortedPassengers, key=lambda passenger: passenger.departureTime)
    #print('listAfter: ', sortedPassengers)
    return sortedPassengers

def execute(passenger_data, cut_off_time):
  totalNumberOfRequests = 0
  passengers = []

  # Initialise list of passenger instances
  for i in range(len(passenger_data)):
    passengers.append(Passenger(passenger_data[i]))

  # Apply solution and re-shuffle with departure cut-off time
  prioritised_and_filtered_passengers = prioritizeQueue(passengers, cut_off_time)

  # Sum totalNumberOfRequests across all passengers
  for i in range(len(passengers)):
    totalNumberOfRequests += passengers[i].getNumberOfRequests()
  print("totalNumberOfRequests: " + str(totalNumberOfRequests))

  # Print sequence of sorted departure times
  print("Sequence of prioritised departure times:")
  prioritised_filtered_list = []
  for i in range(len(prioritised_and_filtered_passengers)):
    print(prioritised_and_filtered_passengers[i].departureTime, end=" ")
    prioritised_filtered_list.append(prioritised_and_filtered_passengers[i].departureTime)

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