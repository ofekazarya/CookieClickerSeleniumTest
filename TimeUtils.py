from time import time, sleep


def timer(timeout, interval=0):
    """
    Allows the creation of for loops that keeps going for a given length of
    time rather than a given iterable.

    # t is how much time is passed since the start of the for loop.
    # t will be printed every 0.5 a second for 60 seconds.
    >>> for t in timer(60, 0.5):
    ...    print(t)

    The same timer can be shared between several for loops. Just create it
    before the first loop.

    >>> timerInstance = timer(60, 1):
    >>> for t in timerInstance:
    ...     if t > 30:
    ...         break
    >>> sleep(5)
    >>>
    >>> # Starts at around 35 as the timer never stops once started
    >>> for t in timerInstance: 
    ...     print("hello") # will print hello around 25 times

    :param (int) timeout: Timeout in seconds
    :param (float) interval: How long between each iteration
    """
    startTime = time()
    elapsedTime = 0
    while elapsedTime < timeout:
        yield elapsedTime

        # Saves some time on large intervals
        if elapsedTime + interval > timeout:
            break

        sleep(interval)
        elapsedTime = time() - startTime
