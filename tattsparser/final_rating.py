# final_rating.py
# Calculate final value for rating

import decimal


def get_final_rating(rating, horse_number):
    decimal.getcontext().prec = 3
    rating = decimal.Decimal(rating)
#    horse_number = decimal.Decimal(horse_number)

    rating_fin = None

    if rating >= 100:
        rating_fin = 2.5
    elif 98 <= rating < 100:
        rating_fin = 2
    elif 95 <= rating < 98:
        rating_fin = 1.5
    elif 93 <= rating < 95:
        rating_fin = 1
    elif 90 <= rating < 93:
        rating_fin = 0
    elif 80 <= rating < 90: 
        rating_fin = -1
    elif rating < 80:
        rating_fin = -1.5

    return rating_fin
