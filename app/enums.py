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

MSG_ERROR = "error"
MSG_SUCCESS = "success"
MSG_FORMAT_ERROR = "format_error"
MSG_AUTH_ERROR = "auth_error"
MSG_INCORRECT_AUTH = "1"
MSG_USER_EXISTED = "2"
MSG_CARD_EXISTED = "3"
MSG_CARD_NOT_EXISTED = "4"
MSG_DELETE_SUCCESS = "5"
MSG_UPDATE_SUCCESS = "6"
MSG_OUT_OF_BARREL = "7"
MSG_CARD_MAX_LEVEL = "8"
MSG_USER_NOT_EXISTED = "9"
MSG_NOT_ENOUGH_HEALTH = "10"

MAPPING_MSG = {
    MSG_ERROR: "Có lỗi xảy ra",
    MSG_SUCCESS: "Thành công",
    MSG_FORMAT_ERROR: 'Thông tin không hợp lệ',
    MSG_AUTH_ERROR: 'Bạn không có quyền truy cập',
    MSG_INCORRECT_AUTH: "Sai tài khoản hoặc mật khẩu",
    MSG_USER_EXISTED: "Tài khoản đã tồn tại",
    MSG_CARD_EXISTED: "Thẻ bài đã tồn tại",
    MSG_CARD_NOT_EXISTED: "Thẻ bài không tồn tại",
    MSG_DELETE_SUCCESS: "Xóa thành công",
    MSG_UPDATE_SUCCESS: "Sửa thành công",
    MSG_OUT_OF_BARREL: "Không đủ vò rượu",
    MSG_CARD_MAX_LEVEL: "Đã đạt cấp tối đa",
    MSG_USER_NOT_EXISTED: "Tài khoản không tồn tại",
    MSG_NOT_ENOUGH_HEALTH: "Không đủ sức khỏe"
}

ACCESS_EXPIRES = timedelta(days=30)
REFRESH_EXPIRES = timedelta(days=90)

HEALTH_INTERVAL = 30
HEALTH_INCREASE = 5

LOSE_HEALTH_BATTLE = 5
LOSE_HEALTH_MISSION = 3
LOSE_HEALTH_BOSS = 10
