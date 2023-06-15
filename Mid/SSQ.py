'''
Mid-term Problem 3: Event-Driven Simulation
Author: Yuhao Zhao
Last edit: Mar 20th
'''
import pandas as pd
from enum import Enum
from numpy.random import MT19937, Generator
import numpy.typing
from RNG import RNG
import simulus
import random

#############################################################################
class Stream(Enum):
    ''' enumeration to identify different streams (one per stochastic component
        in the model) for the random number generator
    '''
    ARRIVAL    = 0 #interarrival time
    NOS        = 1 #number of service task
    TOT        = 2 #time of each service task

#############################################################################
class QueueStats:
    num_in_system    = 0
    total_num_arrival= 0
    total_num_depart = 0
    sum_area_system  = 0
    sum_area_queue   = 0
    sum_area_server  = 0
    time_last_event  = 0
    capability       = 0
    num_of_rejection = 0

#############################################################################
def getInterarrival() -> float:
    return RNG.exponential(1/0.5, Stream.ARRIVAL)

def getNofService() -> int:
    return 1+RNG.geometric(0.1, Stream.NOS)

def getService() -> float:
    return RNG.uniform(0.1, 0.2, Stream.TOT)
    #return RNG.uniform(0.1, 0.3, Stream.TOT)


def completionOfService(queue_stats: QueueStats, show_output: bool = True) -> None:
    if show_output: print(f"Completion @ {sim.now}")


    skyline(queue_stats, show_output = True)
    queue_stats.num_in_system -= 1  #n(t) -=1
    queue_stats.total_num_depart += 1


    if queue_stats.num_in_system > 0:
        sim.sched(completionOfService, queue_stats, offset = getService()*getNofService())


def arrival(queue_stats: QueueStats, show_output: bool = True) -> None:
    if show_output: print(f"Arrival @ {sim.now}")

    skyline(queue_stats, show_output = True)

    queue_stats.num_in_system += 1   # like n(t) += 1
    queue_stats.total_num_arrival += 1
    rejection(queue_stats, show_output = True)



    if queue_stats.num_in_system == 1:
        service_time = getService()*getNofService()
        sim.sched(completionOfService, queue_stats, until = sim.now + service_time)


    if queue_stats.total_num_arrival<max_arrival:
        sim.sched(arrival, queue_stats, offset = getInterarrival())

def skyline(queue_stats: QueueStats, show_output = True) -> None:

    if queue_stats.num_in_system==0:
        queue_stats.sum_area_system += 0
        queue_stats.sum_area_queue += 0
        queue_stats.sum_area_server += 0

    elif queue_stats.num_in_system>0:
        queue_stats.sum_area_system += (sim.now-queue_stats.time_last_event)*queue_stats.num_in_system
        queue_stats.sum_area_queue += (sim.now-queue_stats.time_last_event)*(queue_stats.num_in_system-1)
        queue_stats.sum_area_server += (sim.now-queue_stats.time_last_event)*1

    queue_stats.time_last_event = sim.now # update the time_last_event

def rejection(queue_stats: QueueStats, show_output: bool = True) -> None:

    if queue_stats.num_in_system-1 >= queue_stats.capability:

        queue_stats.num_of_rejection +=1
        queue_stats.num_in_system -=1
        #queue_stats.total_num_arrival -=1

'''
little's equation:

avg_Num_In_System=(max_n/t_end)*avg_sojourn_time
avg_sojourn_time= avg_Num_In_System*t_end/max_n= sum_area_system/max_n
'''

def sim_new(queue_stats: QueueStats, cap: int)->None:

    queue_stats.capability=cap

    sim.sched(arrival, queue_stats, until = sim.now + getInterarrival())


    sim.run()

    print(f"# Arrivals: {queue_stats.total_num_arrival}")
    print(f"# Completions: {queue_stats.total_num_depart}")
    #print(f"# in system @ end: {queue_stats.num_in_system}")
    print(f"TA in system: {queue_stats.sum_area_system/sim.now}")
    print(f"TA in queue: {queue_stats.sum_area_queue/sim.now}")
    print(f"utilization: {queue_stats.sum_area_server/sim.now}")
    print(f"average sojourn time: {queue_stats.sum_area_system/max_arrival}")
    print(f"probability of rejection: {queue_stats.num_of_rejection/max_arrival}")

    TA_in_system.append(queue_stats.sum_area_system/sim.now)
    TA_in_queue.append(queue_stats.sum_area_queue/sim.now)
    utilization.append(queue_stats.sum_area_server/sim.now)
    avg_sojourn_time.append(queue_stats.sum_area_system/max_arrival)
    p_of_rejection.append(queue_stats.num_of_rejection/max_arrival)


#############################################################################

TA_in_system     =[]
TA_in_queue      =[]
utilization      =[]
avg_sojourn_time =[]
p_of_rejection   =[]

random.seed(8675309)
#run simulations based on service node capacity 1-6
for i in range(1, 7):
    sim = simulus.simulator()
    queue_stats = QueueStats()
    max_arrival=1000000
    sim_new(queue_stats, i)

#consistency check(n_bar= q_bar+ x_bar)
print(f"TA in system: {TA_in_system}")
print(f"TA in queue: {TA_in_queue}")
print(f"utilization: {utilization}")
print(f"average sojourn time(service node capability from 1 to 6): {avg_sojourn_time}")
print(f"proportion of rejection(service node capability from 1 to 6): {p_of_rejection}")

#service model 1
dat1= {'avg sojourn time': avg_sojourn_time, 'p of rejection': p_of_rejection}
df1= pd.DataFrame(dat1)
df1.to_csv("table1.csv")

#service model 2
#dat2= {'avg sojourn time':avg_sojourn_time, 'p of rejection':p_of_rejection}
#df2= pd.DataFrame(dat2)
#df2.to_csv("table2.csv")
