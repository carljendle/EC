import random
import math
import numpy as np
from typing import List, Dict



def generate_data(country: str, day_nr: int, country_information: Dict,meat_weights: Dict, relationships: Dict) -> List:
    """
    Args in: The exporting country considered, the day of the export, the entire information of the countries,
    the entire information about the meats.

    Randomly selects a recieving country and meat type, adds information regarding the export occurence to a list.

    Returns: List of information regarding the export/import occurence.
    """
    volume_random = (0.5,1.5)
    return_list = []
    ci = country_information
    mi = meat_information
    sender = country
    #No domestic exports!
    reciever = random.choice(list(filter(lambda x: x != country, countries)))
    return_list.extend([sender, reciever])
    return_list.extend([v for k,v in ci[sender].items() if k != "Export" and k!= "Import"])
    return_list.extend([v for k,v in ci[reciever].items() if k != "Export" and k!= "Import"])

    meat_type = random.choice(list(meat_information.keys()))

    #Add periodicity (and randomness) to exports
    volume = random.uniform(*volume_random)*ci[sender]["Export"]*ci[reciever]["Import"]*mi[meat_type]["Frequency"]*(2 + np.sin(day_nr/60))
    toxicity = mi[meat_type]["Meat Toxicity"]
    price = mi[meat_type]["Meat Price"]
    relationship = relationships[(sender,reciever)]
    return_list.extend([meat_type, volume,price,toxicity, day_nr, relationship])

    budget_countries[reciever] += price*volume*relationship
    expected_revenues[sender] += price*volume*relationship

    return return_list

def update_budgets(dataframes: Dict, countries: List) -> None:
    """
    Update fake budgets and expected revenue based on imports and exports.

    Args in: Dictionary containing all dataframes, list of countries.

    Returns: None, modifies the dataframes based on exports and imports.
    """

    updated_budgets = {k:budget_countries[k]*np.random.uniform(0.8,2.0) for k in budget_countries}
    updated_revenues = {k:expected_revenues[k]*np.random.uniform(0.8,2.0) for k in expected_revenues}

    for country in countries:
        for i in dataframes[country].index:
            reciever = dataframes[country].at[i, "Reciever"]
            dataframes[country].at[i, "BudgetSender"] = int(updated_budgets[country])
            dataframes[country].at[i, "ExpRevSender"] = int(updated_revenues[country])
            dataframes[country].at[i, "BudgetReciever"] = int(updated_budgets[reciever])
            dataframes[country].at[i, "ExpRevReciever"] = int(updated_revenues[reciever])








#Country variables
exp_imp_min = 3
exp_imp_max = 100

min_pop = 10**5
max_pop = 10**7

budget_min = 10**5
budget_max = 10**7

ER_min = 10**5
ER_max = 10**7


#Meat variables
meat_min = 2
meat_max = 40

meat_toxicity_min = 3
meat_toxicity_max = 15

meat_price_min = 300
meat_price_max = 1500

meat_frequency_min = 0.5
meat_frequency_max = 2.0

#Time
days = list(np.arange(1,366))


#Randomly assigning some values to exports/imports budgets etc.
countries = ["China", "Sweden", "Bulgaria","Zimbabwe", "Georgia","Canada","Germany","Japan","Vietnam","Ecuador", "Egypt", "France", "Iceland"]
populations = np.random.randint(low = min_pop, high = max_pop, size = len(countries))
imports = np.random.uniform(low = exp_imp_min, high = exp_imp_max, size = len(countries))
exports = np.random.uniform(low = exp_imp_min, high = exp_imp_max, size = len(countries))
budgets = np.random.randint(low = budget_min, high = budget_max, size = len(countries))
exp_revenues = np.random.randint(low = ER_min, high = ER_max, size = len(countries))
budget_countries = {country:0 for country in countries}
expected_revenues = {country:0 for country in countries}

#Create dictionary containing information regarding countries
country_information = {k:{"Export":exp, "Import":imp, "Population":pop, "Budget": budg, "Expected Revenue": exp_rev}
 for k, exp, imp, pop, budg, exp_rev in zip(countries,exports, imports, populations, budgets, exp_revenues)}



#Randomly assigning some values to meats
meats = ["Crocodile", "Panda", "Komodo Dragon", "Elephant", "Condor", "Human"]
meat_prices = np.random.randint(low = meat_price_min, high = meat_price_max, size = len(meats))
meat_toxicity = np.random.uniform(low = meat_toxicity_min, high = meat_toxicity_max, size = len(meats))
meat_frequency = np.random.uniform(low = meat_frequency_min, high = meat_frequency_max, size = len(meats))

#Create dictionary containing information regarding meats
meat_information = {k:{"Meat Price": price, "Meat Toxicity": toxicity,"Frequency": freq} 
for k, price, toxicity, freq in zip(meats,meat_prices, meat_toxicity, meat_frequency)}




#Creating relationships for export/import price modifications
relationships = {(country1, country2):np.random.uniform(0.5,1) for country1 in countries for country2 in countries if country1 != country2}

cols = ["Sender", "Reciever", "PopSender",
 "BudgetSender", "ExpRevSender", "PopReciever", "BudgetReciever","ExpRevReciever",
 "Meat Type", "Volume","Meat Price", "Toxicity", "Day Number","Trade Discount"]

