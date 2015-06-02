from Algorytm import *
from copy import deepcopy

fifo = Fifo()
rand = Rand()
opt = Opt()
lru = Lru()
lruaproks = LruAproksymowany()

fifo.generate_query()
rand.copy_to_query(deepcopy(fifo.query))
opt.copy_to_query(deepcopy(fifo.query))
lru.copy_to_query(deepcopy(fifo.query))
lruaproks.copy_to_query((deepcopy(fifo.query)))


while fifo.is_query_empty():
    fifo.exe()
print "Bledy strony dla algorytmu FIFO: " + str(fifo.fail_page)


while rand.is_query_empty():
    rand.exe()
print "Bledy strony dla algorytmu RAND: " + str(rand.fail_page)


while opt.is_query_empty():
    opt.exe()
print "Bledy strony dla algorytmu OPT: " + str(opt.fail_page)


while lru.is_query_empty():
    lru.exe()
print "Bledy strony dla algorytmu LRU: " + str(lru.fail_page)


while lruaproks.is_query_empty():
    lruaproks.exe()
print "Bledy strony dla algorytmu LRU aproksymowany: " + str(lruaproks.fail_page)