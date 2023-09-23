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

  return str(finalcolonyWeight)