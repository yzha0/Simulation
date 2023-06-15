import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from rng import RNG, Stream
'''
implementation of algorithm 9.3.3 in next-event simulation fashion
Author: Eric Zhao
'''
def get_Interarrival(k=1, times=None, S=None)->float:
    '''
        Updated version of algorithm 9.3.3. Instead of producinf an entire list of arrival times.
        You must implement a method that, on each call, will remember the last arrival
        and produce the next interarrival using the cumulative event rate function produced by the provided data.

    Parameters:
        k     = number of realizations
        times = empirical data
        S     = maximum time in seconds

    Return:
        single interarrival time

    '''
    get_Interarrival.last_arrival = getattr(get_Interarrival, 'last_arrival', 0)

    n = len(times)
    times = np.concatenate((0, times, S), axis=None)
    interarrival=0
    get_Interarrival.e = getattr(get_Interarrival, 'e', RNG.exponential(1, Stream.ARRIVAL))

    if get_Interarrival.e <= n / k:

        m = int(np.floor((n+1) * k * get_Interarrival.e/n))
        t = times[m]+(times[m+1] - times[m]) * (((n+1) * k * get_Interarrival.e/n) - m)
        interarrival = t - get_Interarrival.last_arrival
        get_Interarrival.last_arrival = t
        get_Interarrival.e += RNG.exponential(1, Stream.ARRIVAL)

    else:
        #start a new round of arrival process
        get_Interarrival.last_arrival = 0
        get_Interarrival.e = RNG.exponential(1, Stream.ARRIVAL)
        if get_Interarrival.e <= n / k:
            m = int(np.floor((n+1) * k * get_Interarrival.e/n))
            t = times[m]+(times[m+1] - times[m]) * (((n+1) * k * get_Interarrival.e/n) - m)
            interarrival = t - get_Interarrival.last_arrival
            get_Interarrival.last_arrival = t
            get_Interarrival.e += RNG.exponential(1, Stream.ARRIVAL)

    return interarrival







def get_events(arr):
    interarrivals=[]
    event=0
    events=[]
    n=len(arr)
    e= RNG.exponential(1, Stream.ARRIVAL)
    while e <=n:
        interval=get_Interarrival(1, times=arr, S= 17.5*3600)
        interarrivals.append(interval)
        e+=RNG.exponential(1, Stream.ARRIVAL)

    for k in interarrivals:
        event+=k
        events.append(event)
    return events


def main():
    arr=np.array(pd.read_csv("cleaned_arrival.txt"))
    plt.plot([], [], ' ')
    labels = ["07:30","09:00","10:30","12:00","13:30","15:00","16:30","18:00","19:30","21:00","22:30","00:00"]
    plt.xticks(np.arange(0, 18, 1.5)*3600, labels, rotation=45)
    plt.axis([0, 17.5*3600, 0, 1400])
    plt.xlabel("time")
    plt.ylabel("# arrivals")
    plt.title("non-homogeneous poisson arrival process")

    # plot the empirical CERF for the arrivals data

    plt.plot(arr, range(len(arr)), color='black', linewidth=2)

    # ...with five realizations superimposed

    colors = ["gray","red","blue","darkgreen","purple"]
    for i in range(len(colors)):
        events=get_events(arr)
        plt.plot(events, range(len(events)), color=colors[i], linewidth=1)


    plt.show()



#main()
