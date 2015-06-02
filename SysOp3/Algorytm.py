from random import randint

FRAMES = 10
PAGE_SIZE = 25
SIZE_QUERY = 500


class Request(object):

    def __init__(self, number):
        self.number = number
        self.second_chance = 1


class Algorytm(object):

    def __init__(self):
        self.physical_memory = []
        self.query = []
        self.fail_page = 0

    def copy_to_query(self, list_new_query):
        self.query = list_new_query

    def losowanie(self):
        l = [Request(randint(0, PAGE_SIZE)) for _ in range(PAGE_SIZE*2)]
        while len(l) < SIZE_QUERY:
            index = randint(0, len(l)-1)
            liczba = l[index].number
            if liczba == PAGE_SIZE:
                l.insert(index, Request(liczba-(randint(0, 2))))
            if liczba <= 2 or liczba >= PAGE_SIZE-3:
                pass
            else:
                if randint(0, 1) == 0:
                    l.insert(index, Request(liczba-randint(0, 2)))
                else:
                    l.insert(index, Request(liczba+randint(0, 2)))
        return l

    def generate_query(self):
        self.query = self.losowanie()

    def preview_elem_query(self):
        return self.query[0].number

    def get_elem_query(self):
        return self.query.pop(0)

    def add_to_physical(self):
        self.physical_memory.append(self.get_elem_query())

    def free_place(self):
        if len(self.physical_memory) < FRAMES:
            return True
        return False

    def increase_fail_page(self):
        self.fail_page += 1

    def is_query_empty(self):
        return bool(self.query)

    def elem_in_physical_mem(self):
        for request in self.physical_memory:
            if request.number == self.preview_elem_query():
                return True
        return False

    def remove(self):
        raise NotImplementedError

    def exe(self):
        if self.elem_in_physical_mem():
            self.get_elem_query()
        else:
            if self.free_place():
                self.add_to_physical()
            else:
                self.remove()
                self.add_to_physical()
                self.increase_fail_page()

    def move_to_end(self, index):
        elem = self.physical_memory[index]
        del self.physical_memory[index]
        self.physical_memory.append(elem)


class Fifo(Algorytm):

    def remove(self):
        self.physical_memory.pop(0)


class Rand(Algorytm):

    def remove(self):
        del self.physical_memory[randint(0, FRAMES-1)]


class Opt(Algorytm):

    def __init__(self):
        super(Opt, self).__init__()
        self.dictionary_frequency = {}

    def remove(self):
        index = self.frequency_query()

        del self.physical_memory[index]

    def reset_dict_freq(self):
        self.dictionary_frequency.clear()

    def request_not_in_query(self, elem):
        for obj in self.query:
            if obj.number == elem.number:
                return False
        return True

    def index_request_in_list(self, elem, list):
        for index, request in enumerate(list):
            if request.number == elem:
                return index

    def frequency_query(self):
        self.reset_dict_freq()
        for index, elem in enumerate(self.physical_memory):
            if self.request_not_in_query(elem):
                return index
            else:
                self.dictionary_frequency[elem.number] = self.index_request_in_list(elem.number, self.query)
        value = max(self.dictionary_frequency.values())
        return self.find_key(value)

    def find_key(self, value):
        for key in self.dictionary_frequency.keys():
            if self.dictionary_frequency[key] == value:
                return self.index_request_in_list(key, self.physical_memory)


class Lru(Algorytm):

    def remove(self):
        del self.physical_memory[0]

    def exe(self):
        if self.elem_in_physical_mem():
            elem = self.get_elem_query().number
            for index, req in enumerate(self.physical_memory):
                if req.number == elem:
                    self.move_to_end(index)
                    break
        else:
            if self.free_place():
                self.add_to_physical()
            else:
                self.remove()
                self.add_to_physical()
                self.increase_fail_page()


class LruAproksymowany(Algorytm):

    def remove(self):
        del self.physical_memory[0]

    # def add_to_physical_rand(self):
    #     self.physical_memory.insert(randint(0, 9), self.get_elem_query())

    def get_first_physical_mem(self):
        return self.physical_memory[0]

    def return_index_from_ph_mem(self, elem):
        for index, request in enumerate(self.physical_memory):
            if request.number == elem.number:
                return index

    def exe(self):
        if self.elem_in_physical_mem():
            elem = self.get_elem_query()
            elem.second_chance = 1
            self.move_to_end(self.return_index_from_ph_mem(elem))
        else:
            if self.free_place():
                self.add_to_physical()
            else:
                while True:
                    if self.get_first_physical_mem().second_chance == 0:
                        self.remove()
                        self.add_to_physical()
                        self.increase_fail_page()
                        break
                    else:
                        elem = self.get_first_physical_mem()
                        elem.second_chance = 0
                        self.move_to_end(0)
                        continue
