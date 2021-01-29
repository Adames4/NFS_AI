from time import time, strftime, gmtime

from .constants import CHECKPOINTS


class Checkpoint:
    '''
    Checkpoint object represention all checkpoints that belong to single Car
    object
    '''
    def __init__(self):
        self.checkpoints = [False for _ in range(7)]
        self.checkpoints[0] = True
        self.cc = 0
        self.checkpoint_times = [None for _ in range(7)]
        self.start_time = time()

    def set_checkpoint(self, color):
        '''
        set current checkpoint
        '''
        if color in CHECKPOINTS[self.cc] and self.checkpoints[self.cc]:
            self.checkpoint_times[self.cc] = time() - self.start_time
            self.checkpoints[self.cc] = False

            if self.cc != 6:
                self.cc += 1
                self.checkpoints[self.cc] = True

    def get_checkpoint(self, number):
        '''
        number: number of current checkpoint
        return: current checkpoint
        '''
        if number < 7:
            return self.checkpoint_times[number]
        else:
            return False

    def get_current_time(self):
        '''
        return: number of second from start
        '''
        return time() - self.start_time

    def get_checkpoint_fitness(self):
        '''
        return: all checkpoints
        '''
        return self.checkpoint_times


def time_conventor(time):
    '''
    return: number of second converted to 00:00:00 format
            (62.54 seconds -> 01:02:54)
    '''
    return strftime('%M:%S:', gmtime(time)) + str(time - int(time))[2:4]
