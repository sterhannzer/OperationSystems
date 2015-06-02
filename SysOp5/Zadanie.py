from random import randint, shuffle

LIMIT_P = 30
QUANTITY_PROC = 15
SIZE_QUEUE_PROCESS = 400
Z_RANDOM_PROCESOR = 5   # ilosc zapytan randomowych procesorow


class Proces():

    def __init__(self, power_calculate, time_execute, number):
        self.name = number
        self.power_calculate = power_calculate
        self.time_execute = time_execute

    def __str__(self):
        return str(self.name)


class Procesor():

    def __init__(self, number):
        self.number = number
        self.execute_process = []
        self.charge = 0
        self.limit_p = LIMIT_P
        self.average = []
        self.average_from_average = []

    def add_proces(self, proces):
        self.execute_process.append(proces)
        self.update_charge()

    def get_last_proces(self):
        last_proces = self.execute_process.pop()
        self.update_charge()
        return last_proces

    def update_charge(self):
        self.charge = 0
        for proces in self.execute_process:
            self.charge += proces.power_calculate


class Strategy_first():

    def __init__(self):
        self.queue_process = []
        self.queue_procesors = []
        self.migration = 0
        self.request_quantity = 0
        self.time = 0

    def generate_queue(self):
        self.queue_process = [Proces(randint(1, 90), randint(1, 15), number) for number in range(SIZE_QUEUE_PROCESS)]

    def create_procesors(self):
        self.queue_procesors = [Procesor(x) for x in range(QUANTITY_PROC)]

    def get_random_procesor(self):
        return self.queue_procesors[randint(0, len(self.queue_procesors)-1)]

    def find_under_P_procesor(self, procesor_request):
        random = range(0, QUANTITY_PROC)
        shuffle(random)
        for _ in range(Z_RANDOM_PROCESOR):
            if self.charge_smaller_then_limit(random[-1]):
                self.request_quantity += 1
                return self.queue_procesors[random.pop()]  # zwraca losowy procesor
            else:
                random.pop()
        return procesor_request

    def charge_smaller_then_limit(self, digit):
        return self.queue_procesors[digit].charge <= LIMIT_P

    def proces_expire(self):
        for procesor in self.queue_procesors:
            for proces in procesor.execute_process:
                if proces.time_execute == self.time:
                    procesor.execute_process.remove(proces)

    def add_calculate(self, procesor, proces):
        procesor.average.append(proces)

    def calculate_average_10sek(self):
        if self.time % 10 == 0:
            self.average_calculate_of_procesors()

    def average_calculate_of_procesors(self):
        licznik = 0
        for procesor in self.queue_procesors:
            for proces in procesor.average:
                licznik += proces.power_calculate
            if len(procesor.average) != 0:
                procesor.average_from_average.append(licznik/len(procesor.average))
            else:
                break
            licznik = 0
            procesor.average = []

    def print_average_from_all_process(self):
        licznik = 0
        for procesor in self.queue_procesors:
            for srednia in procesor.average_from_average:
                licznik += srednia
            print "srednie obciazenie procesora nr: " + str(procesor.number) + " to " + str(licznik/len(procesor.average_from_average))
            licznik = 0

    def exe(self):
        procesor = self.get_random_procesor()
        proces = self.queue_process.pop()
        proces.time_execute += self.time
        procesor.add_proces(proces)
        other_procesor = self.find_under_P_procesor(procesor)
        if other_procesor == procesor:
            self.add_calculate(procesor, proces)
        else:
            self.migration += 1
            self.add_calculate(other_procesor, proces)
            other_procesor.add_proces(procesor.get_last_proces())
        self.proces_expire()
        self.calculate_average_10sek()
        self.time += 1


# class Strategy_second(Strategy_first):
#
#     def exe(self, SIZE_QUEUE_PROCESS=SIZE_QUEUE_PROCESS):
#         procesor = self.get_random_procesor()
#         proces = self.queue_process[-1]
#         proces.time_execute += self.time
#         if procesor.charge > procesor.limit_p:
#             other_procesor = self.find_under_P_procesor(procesor)
#             if other_procesor.charge < LIMIT_P:
#                 other_procesor.add_proces(proces)
#                 self.add_calculate(other_procesor, proces)
#                 self.migration += 1
#             else:
#                 self.time += 1
#
#                 SIZE_QUEUE_PROCESS += 1
#                 self.queue_process.append(Proces(randint(1, 90), randint(1, 15), SIZE_QUEUE_PROCESS))
#
#                 return
#         else:
#             procesor.add_proces(proces)
#             self.migration += 1
#             self.add_calculate(procesor, proces)
#         self.proces_expire()
#         self.calculate_average_10sek()
#         self.time += 1
