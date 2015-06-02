from Zadanie import *

strategia_pierwsza = Strategy_first()
strategia_pierwsza.create_procesors()
strategia_pierwsza.generate_queue()

while strategia_pierwsza.queue_process:
    strategia_pierwsza.exe()

print "migracje: " + str(strategia_pierwsza.migration)
print "ilosc zapytan: " + str(strategia_pierwsza.request_quantity)
strategia_pierwsza.print_average_from_all_process()



# strategia_druga = Strategy_second()
# strategia_druga.create_procesors()
# strategia_druga.generate_queue()
# while strategia_druga.queue_process:
#     strategia_druga.exe()
# print "migracje: " + str(strategia_druga.migration)
# print "ilosc zapytan: " + str(strategia_druga.request_quantity)
# strategia_pierwsza.print_average_from_all_process()