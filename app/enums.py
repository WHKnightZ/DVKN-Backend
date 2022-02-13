# coding=utf-8
from datetime import timedelta

ADMIN_ROUTE = "/manage/"

CARD_RANK_PROBABILITIES = [{"rank": 0, "probability": 100},
                           {"rank": 1, "probability": 100},
                           {"rank": 2, "probability": 20},
                           {"rank": 3, "probability": 5}]

CARD_RANK_MAX = 4
CARD_RANK_BY_LEVEL = 3
CARD_LEVEL_MAX = (CARD_RANK_MAX + 1) * CARD_RANK_BY_LEVEL

MSG_INCORRECT_AUTH = "1"
MSG_USER_EXISTED = "2"
MSG_CARD_EXISTED = "3"
MSG_CARD_NOT_EXISTED = "4"
MSG_DELETE_SUCCESS = "5"
MSG_UPDATE_SUCCESS = "6"
MSG_OUT_OF_BARREL = "7"
MSG_CARD_MAX_LEVEL = "8"

ACCESS_EXPIRES = timedelta(days=30)
REFRESH_EXPIRES = timedelta(days=90)
