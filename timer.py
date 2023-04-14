import time
import datetime



class Timer:
    def __init__(self, duration_min):
        self.min = duration_min
        self.total_sec = self.min * 60

    def reset_timer(self):
        pass


    def countdown(self, h, m, s):
        self.total_sec = h * 3600 + m * 60 + s
        if self.total_sec > 0:
            self.timer = datetime.timedelta(seconds = self.total_sec)
            time.sleep(1)
            self.total_sec -= 1
        

timer = Timer(1)
timer.countdown(0, 1, 0)

