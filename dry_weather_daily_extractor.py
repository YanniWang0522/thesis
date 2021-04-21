import numpy as np
import pandas as pd 
import datetime

def read_csv_file(filename):
    data = pd.read_csv(filename) 
    return data

def strtodatetime(string):
    return(datetime.datetime.strptime(string, '%Y-%m-%d %H:%M:%S'))

def seperate_event(data, step):

    big_buff_time = []
    # for each event, data is stored in the small buff
    small_buff_time = {"DateTime":[], "Flow":[], "Rain": []}

    for i in range(0, len(data)-1): 
        # means continous
        if (strtodatetime(data["DateTime"][i + 1]) - strtodatetime(data["DateTime"][i])).total_seconds() == step:
            small_buff_time["DateTime"].append(data["DateTime"][i])
            small_buff_time["Flow"].append(data["Flow"][i])
            small_buff_time["Rain"].append(data["Rain"][i])

        # not continous
        else:
            small_buff_time["DateTime"].append(data["DateTime"][i])
            small_buff_time["Flow"].append(data["Flow"][i])
            small_buff_time["Rain"].append(data["Rain"][i])
            big_buff_time.append(small_buff_time)
            if (len(small_buff_time["DateTime"]) > 240):
                small_buff_time = {"DateTime":[], "Flow":[], "Rain": []}
    return big_buff_time

def convert_to_csv(data):
    csv_data = {}
    inital = 1 
    for element in data: 
        if (inital == 1):
            csv_data = element
            csv_data["Event"] = []
        csv_data["Event"] += [inital for i in range(0,len(element["DateTime"]))]
        for key in element.keys():
            csv_data[key] += element[key]
        inital += 1
    pd.DataFrame(csv_data).to_csv('RG_Dry_Weather_Heatmont.csv', index=False)

    return csv_data

def summary_table(data_s):

    csv_data = {"Dry Weather event" : [], "Start":[], "End" : [], "Length(min)": [], "Total Flow" :[]}
    count = 1

    for i in data_s:
        csv_data["Start"].append(i["DateTime"][0])    
        csv_data["End"].append(i["DateTime"][len(i["DateTime"]) - 1])
        csv_data["Length(min)"].append( (len(i["DateTime"]) - 1) * 6)
        csv_data["Total Flow"].append(round(sum(i["Flow"]) - 1, 2))
        csv_data["Dry Weather event"].append(count)

        count += 1

    pd.DataFrame(csv_data).to_csv('RG_Dry_Weather_Heatmont_summary.csv', index=False)


if __name__ == "__main__":
    filename= "RG/RG_Rain_Flow_Heathmont_Apr19_Apr20_dry.csv"
    data = pd.read_csv(filename) 

    step = 360
    dry_array = seperate_event(data, step)
    csv_data = convert_to_csv(dry_array)

    dry_array = seperate_event(data, step)
    summary_table(dry_array)
