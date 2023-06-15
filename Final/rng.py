'''
Random Number Generator
Author: Eric Zhao
Last edit: April 20, 2023
'''

from enum import Enum
from numpy.random import MT19937, Generator
import numpy.typing

#############################################################################
class Stream(Enum):
    ''' enumeration to identify different streams (one per stochastic component
        in the model) for the random number generator
    '''
    ARRIVAL    = 0 #interarrival time
    SERVICE    = 1 #number of service task
    TOT        = 2 #time of each service task
    SEED       = 3

######################################################################
class RNG:
    ''' This class implements a wrapper around numpy's MT19937 generator
        to allow for a "streams" implementation, i.e., where we can have a
        different stream of random numbers for each different stochastic
        component.  The stream will be indicated using one of the values
        defined in the Stream enumeration class.  Each wrapper method will do
        the right thing to pull and then update the state of the particular
        stream.
    '''

    # class-level variables
    _seed: numpy.int64 = None
    _streams: list[numpy.random.Generator] = []
    _initialized: bool = False

    ############################################################################
    @classmethod
    def seed(cls, seed: numpy.int64) -> None:
        cls._seed = seed
        cls.initializeStreams()

    ############################################################################
    @classmethod
    def initializeStreams(cls) -> None:
        ''' Class-level method to initialize streams for generating random
            numbers.  This uses the .jumped() method to set up the streams
            sufficiently far apart, giving us one stream per stochastic
            component (i.e., number of entries in the Stream enum).

            See:
                https://bit.ly/numpy_random_jumping
                https://bit.ly/numpy_random_Generator
        '''
        cls._streams = []
        rng = MT19937(cls._seed)  # construct a Mersenne Twister with appropriate seed
        for i in range(len(Stream)):
            cls._streams.append(Generator(rng.jumped(i)))
        cls._initialized = True

    ############################################################################
    @classmethod
    def random(cls, which_stream: Stream) -> numpy.float64:
        ''' Class_level method to generate float values drawn from a uniform(0.0, 1.0)
        Parameters:
            None
        Returns:
            random floats in the half-open interval [0.0, 1.0).
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]

        return generator.random()



    ############################################################################
    @classmethod
    def randint(cls, a: int, b: int, which_stream: Stream) -> numpy.int64:
        ''' Class-level method to generate int values from a discrete
            uniform distribution. If high is None (the default), then results are from 0 to low.
        Parameters:
            a:Lowest (signed) integers to be drawn from the distribution
            (unless high=None, in which case this parameter is 0 and this value is used for high).

            b:If provided, one above the largest (signed) integer to be drawn from the distribution
        Returns:
            random integers from the "discrete uniform" distribution

        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]

        return generator.integers(low = a, high = b)



    ############################################################################
    @classmethod
    def uniform(cls, a: float, b: float, which_stream: Stream) -> numpy.float64:
        '''Class-level method to generate float values drawn from a uniform(a, b)
           distribution, where a and b corresponds to lower and higher bounds of
           the desired interval[a, b)
        Parameters:
           a:lower boundary of the output interval

           b:upper boundary of the output interval
        Returns:
           an uniform distributed float value
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]

        return generator.uniform(low = a, high = b)


    ############################################################################
    @classmethod
    def exponential(cls, scale: float, which_stream: Stream) -> numpy.float64:
        ''' Class-level method to generate float values drawn from a exponential(scale)
            distribution, where scale corresponds to beta=1/lambda(lambda is the rate parameter)
            it is a continuous analogue of the geometric distribution
        Parameters:
            scale:
        Returns:
            an exponential(scale) distributed float value, corresponding to the
            waiting time before first success or waiting time between success in
            a possion process
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]

        return generator.exponential(scale)



    ############################################################################
    @classmethod
    def geometric(cls, p: float, which_stream: Stream) -> numpy.int64:
        ''' class-level method to generate integer values drawn from a geometric(p)
            distribution, where p corresponds the probability of success on an
            individual trial (see numpy.Generator.geometric)
        Parameters:
            p: floating-point probability of success on any single trial
            which_stream: named entry from Stream class
        Returns:
            a geometric(p) distributed integer value, corresponding to the
            number of failures before the first success
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]

        # according to the API for numpy.Generator.geometric, it models the
        # number of _trials_ until the first success, rather than the number of
        # _failures_ before the first success as R does... so we subtract 1
        #     https://bit.ly/numpy_Generator_geometric
        #     https://stat.ethz.ch/R-manual/R-devel/library/stats/html/Geometric.html
        #
        #return generator.geometric(p)
        return generator.geometric(p) - 1  # see comment above

    ############################################################################
    @classmethod
    def gamma(cls, shape: float, scale: float, which_stream: Stream) -> numpy.float64:
        ''' class-level method to generate float values drawn from a gamma(shape, scale)
            distribution, where shape corresponds the k or alpha(shape parameter) of the gamma distribution
            and scale corresponds to theta or beta in gamma distribution. Notice that
            it is a generalization of exponential distribution(alpha=1)
        Parameters:
            shape:shape parameter

            scale:scale of gamma distribution(default==1)
        Returns:
            a gamma(shape, scale) distributed float value, corresponding to time to failure
            or waiting time between possion events
        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]

        return generator.gamma(shape, scale)

    ##############################################################################
    @classmethod
    def lognormal(cls, mean:float, sigma: float, which_stream: Stream) -> numpy.float64:
        '''
            class-level method to generate float values drawn from a lognormal(mean, sigma)
            distribution.Note that the mean and standard deviation are not the values for the distribution itself,
            but of the underlying normal distribution it is derived from.
        Parameters:
            mean:

            sigma:

        '''
        if not cls._initialized:
            cls.initializeStreams()
        generator = cls._streams[which_stream.value]

        return generator.lognormal(mean, sigma)



###################
def main() -> None:
    for i in range(10000):
        #print(RNG.random(Stream.ARRIVAL))
        #print(RNG.randint(0, 10, Stream.ARRIVAL))
        #print(RNG.uniform(0, 1, Stream.ARRIVAL))
        print(RNG.exponential(2, Stream.ARRIVAL))
        #print(RNG.geometric(0.2, Stream.ARRIVAL))
        #print(RNG.gamma(2, 0.2, Stream.ARRIVAL))


if __name__ == "__main__":
    main()
