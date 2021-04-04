import pandas as pd 
import datetime
import numpy as np


def strtodatetime(string):
    return(datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S'))

def read_csv_file(filename):
    data = pd.read_csv(filename) 
    return data

# MEAN EVENT DURATION CALCULATION
def seperate_event(data, time, step):
    big_buff_time = []
    # for each event, data is stored in the small buff
    small_buff_time = []

    for i in range(len(data)-1): 
        # means continous
        if (strtodatetime(data[time][i + 1]) - strtodatetime(data[time][i])).total_seconds() == step:
            small_buff_time.append(data[time][i])

        # not continous
        else:
            small_buff_time.append(data[time][i])
            big_buff_time.append(small_buff_time)
            small_buff_time = []
    
    print (len(big_buff_time))
    return big_buff_time


def mean_event_duration(big_buff_time, step):

    total = 0

    for row in big_buff_time:
        total = total + (len(row) - 1) * step

    return total / len(big_buff_time) / 60



# MEAN EVENT INTENSITY CALCULATION
def seperate_intensity(data, time, rain, step):
    big_buff_rain = []
    
    # for each event, data is stored in the small buff
    small_buff_rain = []

    for i in range(len(data)-1): 
        # means continous
        if (strtodatetime(data[time][i + 1]) - strtodatetime(data[time][i])).total_seconds() == step:
            small_buff_rain.append(data[rain][i])

        # not continous
        else:
            small_buff_rain.append(data[rain][i])
            big_buff_rain.append(small_buff_rain)
            small_buff_rain = []

    return big_buff_rain

def mean_event_intensity(big_buff_rain, step):

    total = 0

    for row in big_buff_rain:
        total = total + sum(row)

    return total / len(big_buff_rain)

if __name__ == "__main__":
    # open the rawdata file 
    filename= "RG/RG_Rain_Flow_Basin_Apr19_Apr20_wet.csv"
    data = pd.read_csv(filename) 

    step = 360 #seconds

    
    # calculate mean event duration (min)
    print(mean_event_duration(seperate_event(data, "DateTime", step),step))

    # calculate mean event intensity (mm/hr)
    print(mean_event_intensity(seperate_intensity(data, "DateTime","Rain", step),step))