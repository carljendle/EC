import pandas as pd
from data_gen_utils import *

def main():
    dataframes = {}
    for country in countries:
        csv = []
        for day in days:
            for i in range(10):
                csv.append(generate_data(country, day, country_information, meat_information, relationships))

        dataframes[country] = pd.DataFrame(csv, columns = cols)

    update_budgets(dataframes, countries)

    for k in dataframes:
        dataframes[k].to_csv(str(k + ".csv"), index = False)

       
    
if __name__ == "__main__":
    main()


