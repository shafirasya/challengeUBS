from typing import Dict, List
import json
import logging

from flask import request

from routes import app

logger = logging.getLogger(__name__)


def getNextProbableWords(classes: List[Dict],
                         statements: List[str]) -> Dict[str, List[str]]:
    # Fill in your solution here and return the correct output based on the given input
    result = {}
    cdict = {k: v for ci in classes for k, v in ci.items()}
    for x in statements:
        result[x] = []
        l = x.split('.')
        first_sub = l[0]
        second_sub = l[1]
        if (first_sub in cdict.keys()):
            if type(cdict[first_sub]) == dict and second_sub != "":
                klist = cdict[first_sub].keys()
                for j in klist:
                    if (j.find(second_sub) != -1):
                        if (cdict[first_sub][j][:4] != 'List'):
                            result[x] += [j]
            else:
                klist = cdict[first_sub]
                for j in klist:
                    if (j.find(second_sub) != -1):
                        result[x] += [j]
        result[x].sort()
        if result[x] == []:
            result[x] = ['']
        final = result[x]
        if (len(final) > 5):
            result[x] = final[:5]
    # print(result)
    return result


@app.route('/lazy-developer', methods=['POST'])
def evaluateLazyDeveloper():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    classes = data['classes']
    statements = data['statements']
    result = getNextProbableWords(classes, statements)
    logging.info("My result :{}".format(result))
    return json.dumps(result)
