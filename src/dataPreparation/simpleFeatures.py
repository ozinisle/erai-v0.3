
def getPriorHoliDaysStamps(df):
    import numpy as np
    priorHolidays = np.zeros(df.shape[0])

    count = 0

    lastValue = 0
    difference = 0

    for day in df:
        currentValue = day

        if count == 0:
            lastValue = currentValue

        if currentValue != lastValue:
            difference = currentValue-lastValue

        if difference == -365:
            difference = 0
        elif difference < 0:
            difference = 365+difference

        priorHolidays[count] = (difference-1, 0)[difference == 0]

        lastValue = currentValue
        count = count+1

    return priorHolidays.astype(np.int64)


def getFollowingHolidaysDaysStamp(df):
    import numpy as np
    import pandas as pd

    df_reverse = df[::-1]

    followingHoliDays = np.zeros(df_reverse.shape[0])

    count = 0
    lastValue = 0
    difference = 0

    for dayCount in df_reverse:
        currentValue = dayCount

        if count == 0:
            lastValue = currentValue

        if currentValue != lastValue:
            difference = lastValue-currentValue

        if difference == -365:
            difference = 0
        elif difference < 0:
            difference = 365+difference

        followingHoliDays[count] = (difference-1, 0)[difference == 0]

        lastValue = currentValue
        count = count+1

    return followingHoliDays.astype(np.int64)

