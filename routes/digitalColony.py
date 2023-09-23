'''from functools import lru_cache
import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


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
    return json.dumps(results)
    # return jsonify(results)


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

    return str(finalcolonyWeight)

def calculateWeightOverGeneration(item):
    generations = item['generations']
    colony = item['colony']

    # Convert colony to a list of digits
    colony_digits = list(map(int, str(colony)))

    for _ in range(generations):
        current_gen_weight = sum(colony_digits)

        # Initialize a new colony list
        new_colony = [colony_digits[0]]

        # Iterate over pairs of digits in the colony
        for i in range(len(colony_digits) - 1):
            digit1, digit2 = colony_digits[i], colony_digits[i + 1]

            # Calculate the signature of the pair
            diff = digit1 - digit2
            signature = abs(diff) % 10 if diff != 0 else 0

            # Calculate the sum of weight and signature
            digit_sum = current_gen_weight + signature

            # Append the last digit of the sum to the new colony
            new_colony.extend(divmod(digit_sum, 10))
            new_colony.append(digit2)

        # Update the colony digits with the new colony
        colony_digits = new_colony

    # Calculate the weight of the final colony
    final_colony_weight = sum(colony_digits)

    return str(final_colony_weight)'''

# more optimized version

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

sample_data = [{'generations': 10, 'colony': '3258'}, {'generations': 50, 'colony': '1789'}]

#results = []
'''for item in sample_data:
    weight = calculateWeightOverGeneration(item)
    results.append(weight)'''


print(calculateWeightOverGeneration(sample_data))