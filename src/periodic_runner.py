from time import sleep


class PeriodicRunner:

    def __init__(self, period=1.0):
        self.period = period

    def start(self):
        while True:
            sleep(self.period)
