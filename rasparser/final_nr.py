# final_nr.py
# Calculate final value for NR number

import decimal


def get_final_nr(nr, horse_number):
    decimal.getcontext().prec = 3
    nr = decimal.Decimal(nr)
#    horse_number = decimal.Decimal(horse_number)

    nr_fin = None

    if nr >= 300.0:
        nr_fin = 3
    elif 230.0 <= nr < 300.0:
        nr_fin = 2.5
    elif 180.0 <= nr < 230.0:
        nr_fin = 2
    elif 140.0 <= nr < 180.0:
        nr_fin = 1.5
    elif 100.0 <= nr < 140.0:
        nr_fin = 1
    elif 90.0 <= nr < 100.0:
        nr_fin = 0
    elif 80.0 <= nr < 90.0:
        nr_fin = -1
    elif nr < 80.0:
        nr_fin = -2

    return nr_fin
