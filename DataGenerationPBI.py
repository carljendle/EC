import pandas as pd
from data_gen_utils import *



for country in countries:
    csv = []
    for day in days:
        for i in range(10):
            csv.append(generate_data(country, day, country_information, meat_information, relationships))
    df = pd.DataFrame(csv, columns = cols)
    df.to_csv(str(country + ".csv"), index = False)
    

