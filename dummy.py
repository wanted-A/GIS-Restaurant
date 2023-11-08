import os
import django
from django.core.cache import cache

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import User
from restaurants.models import Restaurant
from ratings.models import Rating

from random import *


def save_ratings():
    user = User.objects.get(username="admin")
    restaurants = Restaurant.objects.all()

    for restaurant in restaurants:
        number_of_ratings = randint(1, 30)

        for _ in range(number_of_ratings):
            score = float(randint(3, 5))
            Rating.objects.create(
                user=user,
                restaurant=restaurant,
                score=score,
                content="무작위 숫자 입력중",
            )

        # rating = Rating.objects.get_or_create(
        #     user=user,
        #     restaurant=restaurant,
        #     score=float(randint(0, 5)),
        #     content="무작위 숫자 입력중",
        # )

        restaurant.rating = score
        restaurant.save()


if __name__ == "__main__":
    save_ratings()
