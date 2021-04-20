import numpy as np
import pandas as pd
from datetime import datetime
import csv


def create_mask(wet_dry, min_rain, min_flow, MIT, no_flow_time,
                timestep, rain, measured_flow):

    """ extract rain events and stitch them
    together for the rain, measured flow and modelled flow input series.

    Rainfall time series had a 6 minute time step
    MIT is minimum inter event time (minutes)
    """

    # read date time and rainfall time series data
    mask = np.zeros_like(rain, dtype=int)
    l = 1  # a counter

    # defining whether we are inside a rain event (is_in_event = 1) or not (is_in_event = 0)
    # at the start of iteration we are not inside a rain event, so:
    is_in_event = False

    # now iterate through rainfall data:
    for i in range(len(rain)):
        if not is_in_event:
            if float(rain[i]) > 0:
                is_in_event = True
                l += 1
                m = 0
                count = 0
                mask[i] = 1
        else:
            mask[i] = 1
            if float(rain[i]) >= min_rain:
                m = 0
            else:
                m += 1
                if float(measured_flow[i]) < float(min_flow):
                    count += 1
                    if count * timestep >= no_flow_time:
                        is_in_event = False
                elif m * timestep > MIT:
                    # e.g. MIT = 120 minutes, rainfall series time step = 6 minutes
                    is_in_event = False
    return mask


def convert_to_csv(mask, mask_date):
    dic = {"DateTime": [],"dry_or_wet": [], "Rain": [], "Flow" : []}

    for datetime, i in zip(mask_date, range(len(mask))):
        dic["DateTime"].append(datetime)
        dic["dry_or_wet"].append(mask[i])
        dic["Rain"].append(rain[i])
        dic["Flow"].append(measured_data[i])
        
    pd.DataFrame(dic).to_csv('RG_Dry_or_wet_Rain_Flow.csv', index=False)

if __name__ == "__main__":

    # Input parameters for masking of rain events
    wet_dry = "wet"         # "wet" - wet mode, "dry" - dry mode
    MIT = 1440              # Mean Interevent Time [minutes]
    min_rain = 2            # lower threshold for rainfall selection [mm/h]
    min_flow = 10         # lower threshold for flow in rainfall event (base flow) [L/s]
    no_flow_time = 720      # minutes - time of concentration
    warmup_period = 0       # Model warmup period for E calculation [min]
    timestep = 6

    rainfall_station = 'Heathmont'          # Heathmont or Basin
    input_data = 'RG/RG_Rain_Flow_'+rainfall_station+'_Apr19_Apr20'  # The input data file (must be a csv file)
    # print(input_data)
    colnames = ['Rain', 'Flow']         # Name of the column in the input file with the flow data in it
    timeseries_path = 'Martijn_UB_Flow_module/Input data/Rainfall/Rain_'+rainfall_station+'_Apr19_Apr20.txt'
    name_convention = input_data  # convention for the naming of Output file

    rainfall_offset = '0 min'          # offset between rainfall station location and measurement site:
                                        # "+" measurement ahead of model
                                        # "-" measurement lag behind model

    start_date = '04/01/2019'  # TODO -> User - Date formats are US: MM/DD/YYYY; HH:MM:SS
    start_time = '00:00:00'  # TODO -> User
    end_date = '04/08/2020'  # TODO -> User
    end_time = '10:00:00'  # TODO -> User, make increment of time step

    # Reading the input flow and rain data into a list of floats
    data = pd.read_csv(input_data + '.csv')
    # parse input file by dates, and end it based on SWMM end date in ub_to_swmm
    data['DateTime'] = pd.to_datetime(data['DateTime'], format="%d/%m/%Y %H:%M")
    data['DateTime'] = data['DateTime'] + pd.Timedelta(rainfall_offset)
    start = start_date + ' ' + start_time
    end = end_date + ' ' + end_time
    mask_date = (data['DateTime'] >= start) & (data['DateTime'] <= end)
    data = data.loc[mask_date]
    #########################################
    measured_data = data['Flow'].values                # the measured data to calibrate against
    rain = data['Rain'].values               # the measured data to calibrate against
    # Masking series to exclude dry periods
    mask = create_mask(wet_dry, min_rain, min_flow, MIT, no_flow_time,
                       timestep, rain, measured_data)
    # add mask as a new column to the data df
    data['mask'] = mask
    
    # print(mask_data[])

    if wet_dry == 'wet':
        masked_data = data[mask==1]
    else:
        masked_data = data[mask==0]

    csv_name = name_convention + "_" + wet_dry + ".csv"
    masked_data[['DateTime', 'Rain','Flow']].to_csv(csv_name)

    # convert the time series to csv
    convert_to_csv(mask, data['DateTime'])

# for i in range (len(mask)):
#     print (mask[i], rain[i], measured_data[i])
