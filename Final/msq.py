import simulus
import pandas as pd
from numpy.random import MT19937, Generator
from rng import RNG, Stream
import arrivals
'''
This program is an event-driven implementation of a multiple-server queuing
(MSQ) system, as described in Leemis & Park 2006, using Jason Liu's simulus
library to handle the event calendar.  This implementation was benchmarked
versus the Leemis/Park msq.c on 13 Apr 2023.

This program is updated in a way to answering question in DCS 307 Final.

Author: Barry Lawson/Eric Zhao
Last Updated: 20 Apr 2023
'''

MAX_ARRIVALS : int  = 100000
################################################################################
class QueueStats:

    num_arrivals    : int  = 0            # total number of arrivals
    num_completions : int  = 0            # total number of completions
    num_in_system   : int  = 0            # current number in the system

    t_prev          : float = 0.0         # previous simulated-event time
    t_last_arrival  : float = 0.0         # time of last arrival to system

    num_servers     : int  = 0            # number of servers

    # skyline area statistics
    area_system     : float = 0.0         # accumulated area of num in system
    area_queue      : float = 0.0         # accumulated area of num in queue

    arrival_time    : list[float] = [0.0 for s in range(MAX_ARRIVALS)]
    sojourn_time    : list[float] = [0.0 for s in range(MAX_ARRIVALS)]

    # per-server statistics data structures
    is_busy         : list[bool]  = []    # whether this suerver is busy now
    num_served      : list[int]   = []    # per-server count of customers
    total_service   : list[float] = []    # per-server sum of service times
    last_engaged    : list[float] = []    # last time this server was busy
    area_server     : list[float] = []    # accumulated area of num in service
    serving_index   : list[int]   = []    # the current index of customer serving

    #################################################################
    def __init__(self, num_servers: int) -> None:
        ''' QueueStats initializer to set up the class-level per-server lists
            appropriately
        Parameters:
            num_servers: integer number of servers being simulated
        '''
        QueueStats.num_servers   = num_servers
        QueueStats.is_busy       = [False for s in range(num_servers)]
        QueueStats.num_served    = [0     for s in range(num_servers)]
        QueueStats.total_service = [0.0   for s in range(num_servers)]
        QueueStats.last_engaged  = [0.0   for s in range(num_servers)]
        QueueStats.area_server   = [0.0   for s in range(num_servers)]
        QueueStats.serving_index = [0     for s in range(num_servers)]

################################################################################
'''
def getInterarrival() -> float:

        function to return an exponentially distributed interarrival
        time, with rate 1 (i.e., corresponding to a unit stationary
        Poisson process)
    Returns:
        a floating-point interarrival time
    mean_ia = 1.0
    return RNG.exponential(mean_ia, Stream.ARRIVAL)
'''
#Update the interarrival function by using the implementation from arrival.py
def getInterarrival() -> float:
    '''
        function that extends the algorithm 9.3.3 to produce the next
        interarrival time each time using the cumulative event rate function
        produced by the given arrival data from Eight Fifteen in University of Richmond.

    Return:
        a floating-point interarrival time
    '''

    arr=pd.read_csv("cleaned_arrival.txt")
    return arrivals.get_Interarrival(k = 1, times = arr, S = 17.5*3600)

################################################################################
'''
def getService() -> float:
    function to return an exponentially distributed service
        time
    Returns:
        a floating-point service time

    # note that, unlike random's expovariate, the numpy exponential
    # (which RNG wraps) parameterizes using mean, not rate
    mean_svc_time = 9/10
    return RNG.exponential(mean_svc_time, Stream.SERVICE)
    #return random.expovariate(1 / mean_svc_time, Stream.SERVICE)
'''
#Update the service function with best fit: Lognormal
def getService() -> float:
    ''' function to return an lognormally distributed service
        time
    Returns:
        a floating-point service time
    '''
    # note that the mean and sigma are estimated from the MOM method
    mean_svc_time = 3.958694702015
    sigma_svc_time = 0.554901137725597
    return RNG.lognormal(mean_svc_time, sigma_svc_time,Stream.SERVICE)

#################################################################
def selectServer(debug: bool = False) -> int:
    ''' function to select an idle server using the LRU algorithm
    Parameters:
        debug: if True, prints debugging output
    Returns:
        integer index of the server that has been idle longest
    '''
    # find the index of the first idle server
    idx: int = QueueStats.is_busy.index(False)
    # now check remainder to determine which has been idle the longest
    for s in range(idx + 1, QueueStats.num_servers, 1):
        if not QueueStats.is_busy[s] and \
           QueueStats.last_engaged[s] < QueueStats.last_engaged[idx]:
              idx = s
    if debug: print(f"Selected server #{idx}")
    return idx


#################################################################
def engageServer(server_idx: int, debug: bool = False) -> float:
    ''' method to engage the server having the given index, returning
        the generated service time
    Parameters:
        server_idx: integer index of the server being engaged for service
        debug:      if True, prints debugging output
    Return:
        floating-point service time generated upon engagement
    '''
    svc_time = getService()

    QueueStats.total_service[server_idx] += svc_time
    QueueStats.num_served[server_idx] += 1
    QueueStats.last_engaged[server_idx] = sim.now + svc_time
    QueueStats.is_busy[server_idx] = True

    if debug: print(f"Engaging server #{server_idx} with service time {svc_time:.3f}")
    return svc_time


################################################################################
def updateAreas() -> None:
    ''' function to handle updating the area stats asscoiated with the "skyline
        functions" of number in the system, number in queue, and number in
        service
    '''
    qs = QueueStats # references the class
    time_diff = (sim.now - qs.t_prev)  # i.e., rectangle width

    # update area for number in system
    qs.area_system += qs.num_in_system * time_diff

    if qs.num_in_system > qs.num_servers:
        # update area for number in queue
        qs.area_queue += (qs.num_in_system - qs.num_servers) * time_diff

    # update areas per server
    if qs.num_in_system > 0:
        for s in range(qs.num_servers):
            qs.area_server[s] += int(qs.is_busy[s]) * time_diff

################################################################
def completionOfService(server_idx:  int,
                        debug: bool = False) -> None:
    ''' function implementing the algorithm to handle a completion of
        service event from the MSQ at the given server index
    Parameters:
        server_idx:  integer index of the server where departure occurs
        debug:       if True, prints debugging output
    '''

    # update skyline area stats
    updateAreas()

    QueueStats.num_in_system   -= 1
    QueueStats.num_completions += 1
    QueueStats.serving_index[server_idx] = QueueStats.num_completions-1

    sojourn_t = sim.now-QueueStats.arrival_time[QueueStats.serving_index[server_idx]]
    QueueStats.sojourn_time[QueueStats.serving_index[server_idx]]= sojourn_t


    if debug:
        print(f"Completion by server #{server_idx} @ {sim.now}  ", end = "")
        print(f"# in system: {QueueStats.num_in_system}")

    # if there are any customers waiting in the queue, immediately move that
    # customer into service with this (now idle) server
    if QueueStats.num_in_system >= QueueStats.num_servers:
        service_time = engageServer(server_idx, debug)
        sim.sched(completionOfService, server_idx, debug, offset = service_time)
    else:
        # this server becomes idle
        QueueStats.is_busy[server_idx] = False
        if debug: print(f"Server #{server_idx} goes idle")

    QueueStats.t_prev = sim.now  # update the previous event time

################################################################################
def arrival(debug: bool = False) -> None:
    ''' function implementing the algorithm to handle an arrival to the MSQ
    Parameters:
        debug: if True, prints debugging output
    '''
    # update skyline area stats
    updateAreas()

    QueueStats.num_in_system += 1   # like n(t) += 1
    QueueStats.num_arrivals += 1

    QueueStats.arrival_time[QueueStats.num_arrivals-1]=sim.now


    if debug: print(f"Arrival @ {sim.now}  # in system: {QueueStats.num_in_system}")

    # if there is an available server, select one via appropriate algorithm,
    # engage that server (enter service there), and schedule a corresponding COS
    if QueueStats.num_in_system <= QueueStats.num_servers:
        server_idx   = selectServer(debug)
        service_time = engageServer(server_idx, debug)
        sim.sched(completionOfService, server_idx, debug, offset = service_time)

    # if still allowing arrivals, schedule the next arrival to the system
    if QueueStats.num_arrivals < MAX_ARRIVALS:
        sim.sched(arrival, debug, offset = getInterarrival())

    else:
        QueueStats.t_last_arrival = sim.now  # time of last arrival to system

    QueueStats.t_prev = sim.now  # update the previous event time

################################################################################
def printStats(seed: int, include_consistency_check: bool = False) -> None:
    ''' function to print the final MSQ statistics
    Parameters:
        seed: integer-valued seed supplied to the RNG
        include_consistency_check: if True, include additional statistics as
            computed in the Leemis/Park approach, which should match those
            statistics computed in the expected way inside computeAreas
    '''
    qs = QueueStats # references the class
    width = 55; title = "multiple-server queue (msq)"
    print("-" * width)
    print(f"{title:^{width}}".format("centered"))
    print("-" * width)
    print(f"number of servers ..... = {qs.num_servers}")
    print(f"initial seed .......... = {seed}")
    print(f"# of customers ........ = {qs.num_completions}")
    print(f"total simulated time .. = {sim.now:.3f}")
    print(f"avg interarrival ...... = {(qs.t_last_arrival/ qs.num_completions):.3f}")

    # adjust area to calculate avgs for the queue
    updated_area_system = QueueStats.area_system
    for s in range(QueueStats.num_servers):
        updated_area_system -= QueueStats.total_service[s]

    print(f"avg sojourn ........... = {(qs.area_system / qs.num_completions):.3f}")

    print(f"avg sojurn check--------- = {sum(qs.sojourn_time)/len(qs.sojourn_time)}")
    print(f"avg wait  ............. = {(qs.area_queue / qs.num_completions):.3f}")
    if include_consistency_check:
        # see leemis/park text, which uses this approach
        print(f"          ............. = {(updated_area_system / qs.num_completions):.3f}")
    print(f"avg # in system ....... = {(qs.area_system / sim.now):.3f}")
    print(f"avg # in queue ........ = {(qs.area_queue / sim.now):.3f}")
    if include_consistency_check:
        # see leemis/park text, which uses this approach
        print(f"               ........ = {(updated_area_system / sim.now):.3f}")

    print(f"per-server statistics:")
    print(f"  server    utilization    avg service       share");
    spacer = ' ' * 10
    for s in range(qs.num_servers):
        util    = qs.area_server[s] / sim.now
        avg_svc = qs.area_server[s] / qs.num_served[s]
        share   = qs.num_served[s]  / qs.num_completions
        print(f"  {s:>3}{spacer}{util:.3f}{spacer}{avg_svc:.3f}{spacer}{share:.3f}")
        if include_consistency_check:
            # see leemis/park text, which uses this approach
            util_cc    = qs.total_service[s] / sim.now
            avg_svc_cc = qs.total_service[s] / qs.num_served[s]
            print(f"     {spacer}{util:.3f}{spacer}{avg_svc:.3f}")


################################################################################

NUM_SERVERS  : int  = 4
DEBUG        : bool = False  # True


#SEED : int  = 8675309

# don't need a QueueStats object since all stats are stored as class-level
# (not instance) variables, but call __init__ for setup of per-server lists
QueueStats(NUM_SERVERS)
SEED : int  = RNG.randint(1000000, 9999999, Stream.SEED)
RNG.seed(SEED)

sim = simulus.simulator()  # construct a simulator object


# schedule the first arrival
sim.sched(arrival, DEBUG, until = sim.now + getInterarrival())

# kick off the simulation, noting that MAX_ARRIVALS will eventually cause
# the simulation to stop (see definition of arrival() above)
sim.run()

# change argument to True to include additional approach for some output stats
# (see printStats function)
printStats(SEED, include_consistency_check = False)

sojourn_times=pd.DataFrame({'sojourn time':QueueStats.sojourn_time})
sojourn_times.to_csv("sojourn_times_100000.csv")
