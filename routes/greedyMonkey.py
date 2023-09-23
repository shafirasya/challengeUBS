def max_val(w, v, f):
    num = len(f)  # number of fruits in f
    # 3d array (dim: num of fruits x max weight x max volume)
    arr = [[[0] * (v + 1) for x in range(w + 1)] for y in range(num + 1)]
    # arr stores max fruit value for diff val of fruit, weight, and vol
    # initialise arr with 0s

    for i in range(num):  # iterate through fruits in f
        weight = f[i][0]  # get weight
        volume = f[i][1]  # get volume
        value = f[i][2]  # get value of fruit
        for j in range(1, w + 1):
            for k in range(1, v + 1):
                if weight <= j and volume <= k:  # current fruit's val of weight and volume less than j and k
                    arr[i + 1][j][k] = max(arr[i][j][k],
                                           arr[i][j - weight][k - volume] + value)
                else:
                    arr[i + 1][j][k] = arr[i][j][k]

    return arr[num][w][v]


@app.route('/greedymonkey', methods=['POST'])
def greedy_monkey():
    data = request.get_data()
    data = json.loads(data)
    print(data)
    max_weight = data["w"]
    max_volume = data["v"]
    fruits = data["f"]

    total = max_val(max_weight, max_volume, fruits)
    return jsonify(total), 200, {'Content-Type': 'text/plain'}
