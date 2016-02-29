from copy import deepcopy
from Zgloszenie import *
from random import randint, shuffle

class Kolejka():

    def __init__(self, max):
        self.kolejka = []
        self.kolejnosc_wyszukiwania_zgl = []  # posortowane sa od najwiekszego do najmniejszego, pobierac ostatni elem
        self.kolejka_real_time = []
        self.max = max
        self.sum_przemieszczen = 0
        self.aktualna_pozycja = 0  # index biezacej pozycji glowicy w kolejce

    def get_kolejka(self):
        return self.kolejka

    def set_kolejka(self, kolejka):
        self.kolejka = kolejka

    def get_last(self):
        return self.kolejka.pop()

    def get_kolejka_real_time(self):
        return self.kolejka_real_time

    def shuffle(self):
        shuffle(self.kolejka)

    def get_ost_kolejnosc(self):
        return self.get_kolejnosc().pop()

    def get_akt_poz(self):
        return self.aktualna_pozycja

    def get_kolejnosc(self):
        return self.kolejnosc_wyszukiwania_zgl

    def deep_copy(self, lista_kopiowana):
        self.kolejka = deepcopy(lista_kopiowana)

    def get_max(self):
        return self.max

    def get_sum_przemieszczen(self):
        return self.sum_przemieszczen

    def generowanie_zgloszen(self):
        self.kolejka = [Zgloszenie(x, False) for x in range(self.get_max()/2)]
        for i in range((self.get_max())/2):
            self.kolejka.append(None)
        self.shuffle()

    def czy_niepusta_kolejka(self):
        return len(self.kolejnosc_wyszukiwania_zgl) != 0

    def czy_wszystkie_obsluzone(self):
        for zgl in self.kolejka:
            if not zgl is None and not zgl.obsluzony:
                return True
        return False

    def losowanie(self):
        return randint(1, 2) == 1

    def dodaj_zgloszenie(self):
        if self.losowanie():
            zgloszenie = Zgloszenie(randint(self.max, self.max*2), True)
            if zgloszenie.priorytet:
                self.get_kolejka_real_time().append(zgloszenie)
            else:
                self.get_kolejka().append(zgloszenie)

    def przypisz_akt_poz(self, index):
        self.aktualna_pozycja = index

    def zwroc_index(self, nr_zgloszenia):
        for temp in self.get_kolejka():
            if temp is None:
                continue
            if temp.nr == nr_zgloszenia:
                return self.kolejka.index(temp)

    def ruch_glowicy(self, nr_zgloszenia):
        index_zgl = self.zwroc_index(nr_zgloszenia)
        self.sum_przemieszczen += abs(
           index_zgl - self.get_akt_poz()
        )
        self.przypisz_akt_poz(index_zgl)

    def stworz_kolejnosc_szukania(self):  # pobiera numery zgloszen i dodaje do do listy sortujac od najwiekszych
        for i in self.get_kolejka():
            if i is None:
                continue
            self.kolejnosc_wyszukiwania_zgl.append(i.nr)
        self.kolejnosc_wyszukiwania_zgl.sort(reverse=True)

    def print_kolejka(self):
        for zgl in self.get_kolejka():
            if zgl is not None and zgl.priorytet:
                print "*",
            else:
                print zgl,

    def znajdz_nieobsl_zgl(self):
        for index, zgl in enumerate(self.kolejka):
            if zgl is not None and not zgl.obsluzony:
                return index

    def pobierz_priorytety(self):  # pobiera zgloszenia priorytetowe i dodaje do listy
        for zgl in self.kolejka_real_time:
            self.get_kolejka().insert(self.wylosuj_miejsce(), zgl)
            self.kolejnosc_wyszukiwania_zgl.append(zgl.nr)
        self.kolejka_real_time = []

    def dlugosc_kolejki(self):
        return len(self.kolejka)

    def wylosuj_miejsce(self):
        return randint(0, self.dlugosc_kolejki())

    def zerowanie_danych(self):
        self.sum_przemieszczen = 0
        self.aktualna_pozycja = 0
        self.kolejnosc_wyszukiwania_zgl = []
        self.obsluzony_na_false()

    def obsluzony_na_false(self):
        for i in self.kolejka:
            if i is not None:
                i.obsluzony = False

    def sa_priorytety(self):
        for zgl in self.kolejka:
            if zgl is None:
                continue
            if not zgl.obsluzony and zgl.priorytet:
                return True
        return False

    def najblizsze_zgloszenie(self):
        min = self.max-1
        pozycja = self.aktualna_pozycja

        for index, zgl in enumerate(self.kolejka):
            if zgl is None:
                continue
            if zgl.priorytet and not zgl.obsluzony:
                self.kolejka[index].obsluzony = True
                self.kolejnosc_wyszukiwania_zgl.pop()
                return self.kolejka[index].nr
            if abs(index - self.aktualna_pozycja < min) and zgl.obsluzony is False:
                min = abs(index - self.aktualna_pozycja)
                pozycja = index
        self.kolejka[pozycja].obsluzony = True
        self.kolejnosc_wyszukiwania_zgl.pop()
        return self.kolejka[pozycja].nr

    def odwiedzanie_po_kolei(self):
        wskaznik = self.aktualna_pozycja
        while True:
            zgl = self.kolejka[wskaznik]
            if wskaznik >= self.dlugosc_kolejki()-1:
                self.aktualna_pozycja = self.znajdz_nieobsl_zgl()
                wskaznik = self.aktualna_pozycja
                zgl = self.kolejka[wskaznik]
            if self.sa_priorytety():
                return self.najblizsze_zgloszenie()
            if zgl is None:
                wskaznik += 1
                continue
            if zgl.obsluzony:
                wskaznik += 1
                continue
            if not zgl.obsluzony and not zgl.priorytet:
                zgl.obsluzony = True
                self.kolejnosc_wyszukiwania_zgl.pop()
                return zgl.nr
