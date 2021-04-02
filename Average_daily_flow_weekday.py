import pandas as pd 
from datetime import datetime
import plotly.express as px
import collections

# read csv data file via pandas by processing filename as parameter
def read_csv_file(filename):
    data = pd.read_csv(filename) 
    return data

# convert to dictionary
def convert_to_dic(average_data, weekday):
    average_csv = {"time":[], "average":[], "type" : []}

    for time in average_data: 
        if weekday == 1: 
            average_csv["type"].append("weekday") 
        elif weekday == 2:
            average_csv["type"].append("weekend")
        else:
            average_csv["type"].append("allday")

        average_csv["time"].append(time) 
        average_csv["average"].append(average_data[time]) 

    return average_csv

def isweekday(time_num, weekday_or_weekend):
    # allday = 0; weekday = 1; weekend = 2;
    if weekday_or_weekend == 0:
        return True
    # if the time_number<=4, it is weekday
    if weekday_or_weekend == 1: 
        if time_num <= 4:
            return True
        else:
            return False 
    # if the time_number>4, it is weekend
    else:
        if time_num > 4:
            return True
        else:
            return False

# calculate the average flow
def average_flow(data, weekday):
    buff_time = {}
    for time, flow in zip(data['DateTime'],data["Flow"]):
        # parameter 1: integer required; parameter 2: weekend required
        # extract the datatime into integer: from 0(Monday) - 6(Sunday)
        if isweekday(time.date().weekday(), weekday):
            if str(time.time()) not in buff_time:
                buff_time[str(time.time())] = {"count" : 1, "flow" : flow}
            else:
                buff_time[str(time.time())]["count"] += 1
                buff_time[str(time.time())]["flow"] += flow 
    average = {}
    for time in buff_time: 
        average[time] = buff_time[time]["flow"]/buff_time[time]["count"]

    average = collections.OrderedDict(sorted(average.items()))
    return average

def Merge(dict1, dict2):
    # requires both have the same key and array as value
    for key in dict1:            
        dict1[key] = dict1[key] + dict2[key]
    return dict1

if __name__ == "__main__":
    # open the rawdata file 
    filename= "OJC/OJC_Rain_Flow_Heathmont_Apr19_Apr20_dry.csv"
    data = pd.read_csv(filename) 
    # change the date string to datatime obj
    data['DateTime'] = pd.to_datetime(data['DateTime'], format="%Y/%m/%d %H:%M")

    # get weekday and weekend data
    weekday = convert_to_dic(average_flow(data, 1), 1)
    weekend = convert_to_dic(average_flow(data, 2), 2)
    allday = convert_to_dic(average_flow(data, 0), 0)

    # merge both dict
    merged_data = Merge(weekday, weekend)
    merged_data = Merge(merged_data, allday)

    merged_data = pd.DataFrame(data=merged_data)
    fig = px.line(merged_data, x="time", y="average", title='OJC Average diurnal flow rate', color="type")
    fig.update_layout(yaxis_title='Flow (lps)')
    fig.show()
