import pandas as pd

#functionas
def depcheck(df,dict):
    for key in dict:
        df.loc[key,"deposits"] = dict[key]
    return df

#import dataframe of inflation percentages over time
from api_cleanup import monthly_infl_percentage
from user_input import deposits

#debug dataframe
#monthly_infl_percentage = pd.DataFrame({"year_month": ["2021-01","2021-02","2021-03"], "inflation_percentage_change": [0.1,0.5,-0.1]})
#monthly_infl_percentage = monthly_infl_percentage.set_index("year_month")
#deposits = {"2021-01":100,"2021-03":500}



#add column of deposits and corresponding to date rows
monthly_infl_percentage["deposits"] = [0 for i in range(len(monthly_infl_percentage))]


deposit_df = depcheck(monthly_infl_percentage,deposits)
deposit_df.reset_index(inplace = True)

#calculcate running total column of desposits adjusted by inflation, adding new deposits but not adjusting them when deposited
deposit_df["adjusted_total"] = [0 for i in range(len(deposit_df))]

for ind in deposit_df.index:
    if ind == 0:
        deposit_df.loc[ind, "adjusted_total"] = deposit_df.loc[ind,"deposits"]
    else:
        deposit_df.loc[ind, "adjusted_total"] = (100/(deposit_df.loc[ind,"inflation_percentage_change"]+100)*deposit_df.loc[ind-1,"adjusted_total"])+deposit_df.loc[ind,"deposits"]

#return final total

final_total = round(list(deposit_df["adjusted_total"])[-1],2)

print("Today, your deposits would be worth: ", str(final_total)," GBP")
print("If held as cash")