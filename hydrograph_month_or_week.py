import numpy as np
import pandas as pd 
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as dates

def read_csv_file(filename):
    data = pd.read_csv(filename) 
    return data

# get the month/week number for DateTime
def strtodatetime(string, week_or_month):
    if week_or_month == 'month':
        return(datetime.datetime.strptime(string, "%d/%m/%Y %H:%M")).month
    else:
        return(datetime.datetime.strptime(string, "%d/%m/%Y %H:%M")).isocalendar()[1]

# Create a big array to store the data for each month/week
def array_in_array(week_or_month, data, key, number):

    big_buff = []
    small_buff = []

    date_arr_big = []
    date_arr_small = [] 
    
    prev = data['DateTime'][0]
    small_buff.append(data[key][0])
    date_arr_small.append(prev)

    for i in range(1, len(data[key])):
        if (strtodatetime(data["DateTime"][i],week_or_month)-strtodatetime(prev, week_or_month) == 0):
            small_buff.append(data[key][i])

            date_arr_small.append(data["DateTime"][i])
        else:
            big_buff.append(small_buff)
            date_arr_big.append(date_arr_small)


            small_buff = []
            date_arr_small= [] 

            small_buff.append(data[key][i])
            date_arr_small.append(data["DateTime"][i])

        prev = data["DateTime"][i]

    dic = {"x_axis" : date_arr_big[number] , "y_axis" : big_buff[number]}

    return dic

# Sub plot function
def sub_plot(week_or_month, number):
    #####------- data -------#####
    flow = np.array(array_in_array(week_or_month,data,"Flow",number)["y_axis"])
    rain = np.array(array_in_array(week_or_month,data,"Rain",number)["y_axis"])
    # time = array_in_array("month",data,"DateTime")["x_axis"]
    
    #####------- primary chart -------#####
    # adjust the figure length to width ratio
    fig, ax = plt.subplots(figsize=(15, 5))

    # x axis to plot both runoff and precip. against
    x = np.linspace(0, len(flow), len(flow))
    ax.plot(x, flow, color="r")
    ax.set_xlabel('timestep', fontsize=12, color='black')
    ax.set_ylabel('flow(lps)', fontsize=12, color='black')

    # set y1 axis range
    ax.set_yticks([0, 500, 1000, 1500, 2000, 2500, 3000])
    ax.set_ylim(ymin=0)
    ax.set_xticklabels

    # plt.gcf().autofmt_xdate()

    #####------- twin chart -------#####
    ax2 = ax.twinx()
    ax2.bar(x, -rain, 1)
    y2_ticks = rain
    y2_ticklabels = [str(i) for i in y2_ticks]
    ax2.set_yticks(-1 * y2_ticks)
    ax2.set_yticklabels(y2_ticklabels)

    # set y2 axis range
    ax2.set_yticks([0, -20, -40, -60, -80, -100, -120])
    ax2.set_yticklabels([str(i) for i in range(0,130,20)])
    ax2.set_ylabel('rain(mm)', fontsize=12, color='black')

    return fig

if __name__ == "__main__":
    # month or week
    intput = "month" 
    # open the rawdata file 
    filename= "RG/RG_Rain_Flow_Basin_Apr19_Apr20.csv"
    data = pd.read_csv(filename)  

    if (input == "month"):
        for i in range(0,12,1):
            sub_plot("month",i)

            plt.savefig('hydrograph' + "_" +intput +str(i) + '.png' , dpi=400)    
    
    else:
        for i in range(0,54,1):
            sub_plot("week",i)

            plt.savefig('hydrograph' + "_" +intput +str(i) + '.png' , dpi=400)    

