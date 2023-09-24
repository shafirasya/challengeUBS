import math

def calculate_radians(portfolio):
    total_investment = sum(portfolio)
    proportions = [investment / total_investment for investment in portfolio]

    min_proportion_radians = 0.00314159  # Minimum radians for instruments with small proportions
    min_proportion = 0.05/100
    total_radians = 2 * math.pi

    radians = []
    total_adjustment_diff = 0
    total_unadjusted_investment = 0
    for proportion in proportions:
        if proportion < min_proportion:
            radians.append(min_proportion_radians)
            total_adjustment_diff += (min_proportion_radians-proportion*total_radians)
        else:
            radians.append(proportion * total_radians)
            total_unadjusted_investment += (proportion * total_radians)

    #radians = [min_proportion_radians if proportion < min_proportion else proportion * total_radians for proportion in proportions]
    
     # Calculate radians for each instrument, adjusting for small proportions
    if(total_adjustment_diff):
        for radian in radians:
            if(radian > min_proportion_radians):
                radian -= (total_adjustment_diff * radian/total_unadjusted_investment)

    # Sort instruments and calculate boundaries
    #sorted_instruments = sorted(zip(portfolio, radians), key=lambda x: x[0]['investment'], reverse=True)
    radians.sort(reverse=True)
    boundaries = [0.0]
    accumulated_radians = 0.0

    for radian in radians:
        accumulated_radians += radian
        boundaries.append(round(accumulated_radians, 7))

    return boundaries

def processCalculationRadians(portfolio):
    listInvestmentAmount = [instrument['quantity']*instrument['price'] for instrument in portfolio]
    radianResult = calculate_radians(listInvestmentAmount)
    return {
        "instruments": radianResult
    }

# Example usage
sample_data = [
{
    "quantity": 110,
    "price": 10.0,
    "currency": "SGD",
    "sector": "ECommerce",
    "assetClass": "Equity",
    "region": "APAC"
},
{
    "quantity": 5,
    "price": 1.0,
    "currency": "USD",
    "sector": "Technology",
    "assetClass": "Equity",
    "region": "NORTH_AMERICA"
},
{
    "quantity": 39,
    "price": 5.0,
    "currency": "GBP",
    "sector": "Education",
    "assetClass": "Equity",
    "region": "EMEA"
},
{
    "quantity": 32,
    "price": 100.0,
    "currency": "Other",
    "sector": "Pharmaceutical",
    "assetClass": "Equity",
    "region": "APAC"
},
{
    "quantity": 200,
    "price": 30.0,
    "currency": "HKD",
    "sector": "Technology",
    "assetClass": "FixedIncome",
    "region": "APAC"
}]

result = processCalculationRadians(sample_data)
print(result)