# function to get the rmse of classified data
def get_rmse(list1, list2):
    import pandas as pd
    import numpy as np
    import math
    # make sure lists are numeric
    n = len(list1)
    n_list2 = len(list2)
    list1 = list(pd.to_numeric(list1)) # human
    #for response in list(range(0, n_list2)):
    #    if list2[response].isdigit() == False:
    #       list2[response] = np.nan
    list2 = list(pd.to_numeric(list2)) # machine
    diff_sq = []
    sum_sq = 0
    if len(list1) == len(list2):
        for i in list(range(0, n)):
            diff = list1[i] - list2[i]
            diff_sq.append(diff*diff)
        sum_sq = sum(diff_sq)
    if len(list1) != len(list2):
        sum_sq = np.nan
    rmse = math.sqrt(sum_sq/n)
    return rmse