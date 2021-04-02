import pandas as pd 

import matplotlib.pyplot as plt
import numpy as np

# run behzad's code whcih can generate a csv file 
# then we get that file 

# extract data from csv file 
def hasflow(inputflow_Data, column_name):
    buff = []
    for flow in inputflow_Data[column_name]:
        # print(flow)
        if flow > 0: 
            buff.append(1) 
        else: 
            buff.append(0)
    return buff

if __name__ == '__main__':
    data = pd.read_csv(open('OJC/OJC_Rain_Flow_Heathmont_Apr19_Apr20_dry.csv', 'rb'))
    # print(data)
    # print(type(data))


    # data = data[data["Flow"] != 0 ]

    # print(data)

    datasketch = hasflow(data, "Flow")
    # print(datasketch)
    code = np.array(datasketch)

    pixel_per_bar = 4
    dpi = 100

    fig = plt.figure(figsize=(len(code) * pixel_per_bar / dpi, 2), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])  # span the whole figure
    ax.set_axis_off()
    ax.imshow(code.reshape(1, -1), cmap='binary', aspect='auto',
            interpolation='nearest')
    plt.show()
# data.to_csv(r'yanni.csv')



