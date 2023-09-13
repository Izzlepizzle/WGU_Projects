from collections import deque
from datetime import datetime


# Truck class
class Truck:
    def __init__(self, name):
        self.name = name
        self.size = 16
        self.distance = 0.0
        self.packages = deque([])
        self.speed = 0.3
        self.finished_time = datetime.today()

    def add_package(self, package):
        self.packages.append(package)
