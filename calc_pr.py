import multiprocessing
from tqdm import tqdm

from gacha import *
from state import *


char5_pool = {
    "라루(이브)": 1,
    "후유카": 1,
    "시아": 0,
    "치토세": 1,
    "나노하": 2,
    "프리지아": 1,
    "미네르바": 2,
    "미스티": 0,
    "치시아": 0,
    "그레이": 1,
    "나즈나": 0,
}
char4_pool = {
    "징린": 3,
    "테레사": 5,
    "코하쿠": 2,
    "틸리아": 1,
    "카시미라": 3,
    "아야메": 6,
    "세이나": 1,
    "시먀오": 1,
    "레이센": 1,
    "크루니스": 3,
    "카나체": 1,
    "안즈": 3,
    "플로라": 2,
    "코제트": 3,
    "캐러멜": 2,
    "라루": 2,
}

rc5_pool = {
    "반짝이는 옛 연못": 0,
    "맑은 하늘의 꽃": 1,
    "마녀의 그네": 1,
    "자정의 타락 천사": 0,
    "용과 봉황": 1,
    "대낮의 화원": 0,
    "길 잃은 순례자": 0,
    "전설을 잡아라": 2,
}

rc4_pool = {
    "열대야의 끝": 3,
    "괴도 콤비": 1,
    "★~펑펑 소녀~★": 1,
    "굿나잇": 0,
    "에메랄드 틈새 경계": 4,
    "휴식의 순간": 4,
    "'빗속의' 선율": 2,
    "수증기 증후군": 3,
    "고양이 리듬": 0,
    "별하늘에 안부를": 4,
    "가을날 속삭임": 4,
    "기사의 대장장이": 1,
    "알려지지 않은 이름": 4,
    "새장의 장미": 0,
    "★~돌고 도는 인생~★": 1,
    "음료수 사는 날": 1,
    "망언": 2,
    "플래시 고스트": 3,
    "영험한 찬가": 1,
}
rc3_pool = {
    "아침 안개": 6,
    "평온": 6,
    "황혼": 6,
    "분홍빛 꿈": 6,
    "고독한 연기": 6,
    "감로": 6,
    "희망": 6,
    "귀로": 6,
    "성찬": 6,
    "소란": 6,
    "극락": 6,
    "열정": 6,
    "상서로운 빛": 6,
    "바람을 타고": 6,
    "물거품": 6,
    "검은 소멸": 6,
    "강인함": 6,
}

init_frag_cnt = 92090
init_cert_cnt = 2840
init_sprout_ticket_cnt = 0
init_sky_ticket_cnt = 41 + 4
init_disk_cnt = 9420

init_state = CurrentState(
    init_frag_cnt,
    init_cert_cnt,
    char5_pool,
    char4_pool,
    rc5_pool,
    rc4_pool,
    rc3_pool,
    init_sprout_ticket_cnt,
    init_sky_ticket_cnt,
    init_disk_cnt,
)

snowish_laru_pickup = CharPickUp.load_gacha("snowish_laru_pickup.json")
cur_pickup1 = CharPickUp(*snowish_laru_pickup, (1, 1), init_mileage=16)
# chitose_rc_pickup = RcPickUp.load_gacha("chitose_rc_pickup.json")
# cur_pickup2 = RcPickUp(*chitose_rc_pickup, (0, 0))
# char_gacha = CharGacha.load_gacha("char_gacha.json")
# cur_gacha1 = CharGacha(char_gacha, init_stack=(100, 8))

trial_cnt = 1000000
pickup1_succ_thr = [("라루(이브)", 6)]
# pickup2_succ_thr = []
gacha1_succ_thr = []


def run_single_trial(_):
    is_succ, state = cur_pickup1.simulate_trial(init_state, pickup1_succ_thr)
    if not is_succ:
        return False
    # is_succ, state = cur_pickup2.simulate_trial(state, pickup2_succ_thr)
    # if not is_succ:
    #     return False

    # is_succ = cur_gacha1.simulate_trial(state, gacha1_succ_thr)[0]
    return is_succ


if __name__ == "__main__":
    with multiprocessing.Pool() as pool:
        results = list(
            tqdm(pool.imap(run_single_trial, range(trial_cnt)), total=trial_cnt)
        )

    succ_cnt = sum(results)
    pr = succ_cnt * 100 / trial_cnt
    print(pr)

# 시뮬레이션 1회 결과 확인
# is_succ, state = cur_pickup1.simulate_trial(init_state, pickup1_succ_thr)
# print(is_succ)
# print(state)
# if is_succ:
#     is_succ, state = cur_pickup2.simulate_trial(state, pickup2_succ_thr)
#     print(is_succ)
#     print(state)
#     if is_succ:
#         is_succ, state = cur_gacha1.simulate_trial(state, gacha1_succ_thr)
#         print(is_succ)
#         print(state)
