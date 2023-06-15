
"""
@classmethod
def xxx(cls, value:int) -> int:
    cls.

@staticmethod
def xyy(value)

"""
from numpy import random.MT19937, Generator
import numpy.typing

class RNG:

    #class level variables
    _seed: numpy.int64 = None
    _streams: list[numpy.random.Generator] = []
    _initialized: bool = False

    @classmethod
    def setSeed(cls, seed: numpy.int64) -> None:
        cls._seed = seed
        cls.initialzedStreams()

    @classmethod
    def initialzedStreams(cls) -> None:
        cls._streams = []
        rng = MT19937(cls._seed) # construct a Mersenne Twister with appropriate seed
        for i in range(25):
            cls._streams.append(Generator(rng.jumped(i)))
        cls._initialized = True

    @classmethod
    def geometric(cls, p: float, which_streams: int) -> numpy.int64:
        if not cls._initialized:
            cls.initialzedStreams()
        generator = cls._streams[which_streams]
        return generator.geometric(p)

def main() -> None:
    stream = 0
    for i in range(10000):
        print(RNG.geometric(0.2, stream))

if __name__ == "__main__":
    main()
