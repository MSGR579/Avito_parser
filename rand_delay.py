import random
import time


class RandDelay:
    """
    Класс, в котором реализован метод, для установления рандомной задержки 
    между запросами, чтобы уменьшить нагрузку на сервер и не получить блокировку.

    """
    
    def slepper(self):
        delay = random.uniform(1, 10)
        time.sleep(delay)


