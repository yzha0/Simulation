'''
DCS 307
hw 6: ssq implementation in py
author: Yuhao Zhao
last updated: Mar 9th
'''

import simulus
import random

class QueueStats:
    num_in_system = 0
    total_num_arrival = 0
    total_num_depart = 0
    sum_area_system = 0
    sum_area_queue = 0
    sum_area_server = 0
    time_last_event = 0


def getInterarrival() -> float:
    return random.expovariate(1.0)

def getService() -> float:
    return random.expovariate(10/9)

def completionOfService(queue_stats: QueueStats, show_output: bool = True) -> None:
    if show_output: print(f"Completion @ {sim.now}")

    skyline(queue_stats, show_output = True)
    queue_stats.num_in_system -= 1  #n(t) -=1
    queue_stats.total_num_depart += 1


    if queue_stats.num_in_system > 0:
        sim.sched(completionOfService, queue_stats, offset = getService())


def arrival(queue_stats: QueueStats, show_output: bool = True) -> None:
    if show_output: print(f"Arrival @ {sim.now}")

    skyline(queue_stats, show_output = True)
    queue_stats.num_in_system += 1   # like n(t) += 1
    queue_stats.total_num_arrival +=1


    if queue_stats.num_in_system == 1:
        service_time = getService()
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




random.seed(8675309)
sim = simulus.simulator()
queue_stats = QueueStats()
max_arrival=10000

sim.sched(arrival, queue_stats, until = sim.now + getInterarrival())


sim.run()



print(f"# Arrivals: {queue_stats.total_num_arrival}")
print(f"# Completions: {queue_stats.total_num_depart}")
print(f"# in system @ end: {queue_stats.num_in_system}")
print(f"TA in system: {queue_stats.sum_area_system/sim.now}")
print(f"TA in queue: {queue_stats.sum_area_queue/sim.now}")
print(f"utilization: {queue_stats.sum_area_server/sim.now}")


'''
ssq from simEd in R:
#1 run:
output$avgNumInSystem
[1] 8.113383
> output$avgNumInQueue
[1] 7.216595
> output$utilization
[1] 0.8967876

#2 run:
output$avgNumInSystem
[1] 11.03797
> output$avgNumInQueue
[1] 10.11472
> output$utilization
[1] 0.9232537

#3 run:
output$avgNumInSystem
[1] 8.02889
> output$avgNumInQueue
[1] 7.131802
> output$utilization
[1] 0.8970876

#4 run:
output$avgNumInSystem
[1] 10.38742
> output$avgNumInQueue
[1] 9.495108
> output$utilization
[1] 0.8923079

#5 run:
output$avgNumInSystem
[1] 8.039863
> output$avgNumInQueue
[1] 7.140181
> output$utilization
[1] 0.8996823

Python implementation using simulus:
#1 run:
TA in system: 9.315843047546263
TA in queue: 8.418016837358698
utilization: 0.8978262101875106

#2 run:
TA in system: 8.518312139648545
TA in queue: 7.614230296577887
utilization: 0.9040818430707087

#3 run:
TA in system: 11.089906610302187
TA in queue: 10.16956936258291
utilization: 0.9203372477192875

#4 run:
TA in system: 6.926376343559979
TA in queue: 6.042525548238475
utilization: 0.8838507953215147

#5 run:
TA in system: 11.948225251916202
TA in queue: 11.028304701517568
utilization: 0.919920550398703

'''
