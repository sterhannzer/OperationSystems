from Zgloszenie import *
from Kolejka import *
from copy import deepcopy


fcfs = Kolejka(10)
fcfs.generowanie_zgloszen()
fcfs.stworz_kolejnosc_szukania()
fcfs.print_kolejka()
kolejka = deepcopy(fcfs.get_kolejka())
kolejka2 = deepcopy(fcfs.get_kolejka())
print



# FCFS - ze zgloszeniami priorytetowymi
while fcfs.czy_niepusta_kolejka():
    if fcfs.get_kolejka_real_time():
        fcfs.pobierz_priorytety()
        fcfs.ruch_glowicy(fcfs.get_ost_kolejnosc())
    fcfs.ruch_glowicy(fcfs.get_ost_kolejnosc())
    fcfs.dodaj_zgloszenie()
print "FCFS suma przemieszczen z priorytetami: " + str(fcfs.get_sum_przemieszczen())

fcfs.set_kolejka(kolejka)
fcfs.zerowanie_danych()
fcfs.stworz_kolejnosc_szukania()



# FCFS - bez zgloszen priorytetowych
while fcfs.czy_niepusta_kolejka():
    fcfs.ruch_glowicy(fcfs.get_ost_kolejnosc())
print "FCFS suma przemieszczen bez priorytetow: " + str(fcfs.get_sum_przemieszczen())
print



# SSTF - bez zgloszen priorytetowych
sstf = Kolejka(11)
sstf.set_kolejka(kolejka)
sstf.stworz_kolejnosc_szukania()

while sstf.czy_niepusta_kolejka():
    sstf.ruch_glowicy(sstf.najblizsze_zgloszenie())

print "SSTF suma przemieszczen bez priorytetow: " + str(sstf.get_sum_przemieszczen())


# SSTF - ze zgloszeniami priorytetowymi
sstf.set_kolejka(kolejka)
sstf.zerowanie_danych()
sstf.stworz_kolejnosc_szukania()

while sstf.czy_niepusta_kolejka():
    if sstf.get_kolejka_real_time():
        sstf.pobierz_priorytety()
        sstf.ruch_glowicy(sstf.najblizsze_zgloszenie())
    sstf.ruch_glowicy(sstf.najblizsze_zgloszenie())
    sstf.dodaj_zgloszenie()
print "SSTF suma przemieszczen z priorytetami: " + str(sstf.get_sum_przemieszczen())
print


# SCAN - ze zgloszeniami priorytetowymi
scan = Kolejka(11)
scan.set_kolejka(kolejka)
scan.zerowanie_danych()
scan.stworz_kolejnosc_szukania()

while scan.czy_wszystkie_obsluzone():
    if scan.get_kolejka_real_time():
        scan.pobierz_priorytety()
        scan.ruch_glowicy(scan.odwiedzanie_po_kolei())
    scan.ruch_glowicy(scan.odwiedzanie_po_kolei())
    scan.dodaj_zgloszenie()
print "SCAN suma przemieszczen z priorytetami: " + str(scan.get_sum_przemieszczen())

# scan - bez zgloszen priorytetowych
scan.set_kolejka(kolejka2)
scan.zerowanie_danych()
scan.stworz_kolejnosc_szukania()

while scan.czy_wszystkie_obsluzone():
    scan.ruch_glowicy(scan.odwiedzanie_po_kolei())
print "SCAN suma przemieszczen bez priorytetow: " + str(scan.get_sum_przemieszczen())
