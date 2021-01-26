from .constants import CHECKPOINTS
from time import time, strftime, gmtime


class Checkpoint:
    def __init__(self):
        self.checkpoints = [False for _ in range(7)]
        self.checkpoints[0] = True
        self.cc = 0
        self.checkpoint_times = [None for _ in range(7)]
        self.start_time = time()

    def set_checkpoint(self, color):
        if color in CHECKPOINTS[self.cc] and self.checkpoints[self.cc]:
            self.checkpoint_times[self.cc] = time() - self.start_time
            self.checkpoints[self.cc] = False

            if self.cc != 6:
                self.cc += 1
                self.checkpoints[self.cc] = True

    def get_checkpoint(self, number):
        if number < 7:
            return self.checkpoint_times[number]
        else:
            return False

    def get_current_time(self):
        return time() - self.start_time

    def get_checkpoint_fitness(self):
        return self.checkpoint_times


def time_conventor(time):
    return strftime('%M:%S:', gmtime(time)) + str(time - int(time))[2:4]
