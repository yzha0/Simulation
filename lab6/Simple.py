import simulus
import random

class QueueStats:
    num_in_system = 0;


def printMessage() -> None:
    print(f"Hello at time {sim.now}")

def getInterarrival() -> float:
    return random.expovariate(1.0)

def getService() ->float:
    
    return random.expovariate(10/9)

def cos(queue_stats : QueueStats) -> None:
    pass

def arrival(queue_stats: QueueStats) -> None:
    queue_stats.num_in_system +=1
    if queue_stats.num_in_system ==1:
        service_time = getService()
        sim.sched(cos, queue_stats, until = sim.now + service_time)
    sim.sched(arrival, queue_stats, offset = getInterarrival())

sim = simulus.simulator()
Queue_stats = QueueStats()

sim.sched(arrival, queue_stats, until = sim.now + getInterarrival())

max_time = 100
sim.run(max_time)
