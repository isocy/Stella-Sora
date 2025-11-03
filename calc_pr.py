import multiprocessing
from tqdm import tqdm

from pickup import *
from state import *


char5_pool = {
    "치토세": 1,
    "나노하": 0,
    "프리지아": 0,
    "미네르바": 1,
    "미스티": 0,
    "치시아": 0,
    "그레이": 1,
    "나즈나": 0,
}
char4_pool = {
    "징린": 1,
    "테레사": 0,
    "코하쿠": 2,
    "틸리아": 0,
    "카시미라": 2,
    "아야메": 3,
    "세이나": 1,
    "시먀오": 0,
    "레이센": 0,
    "크루니스": 3,
    "카나체": 1,
    "안즈": 2,
    "플로라": 1,
    "코제트": 2,
    "캐러멜": 0,
    "라루": 0,
}

rc5_pool = {
    "반짝이는 옛 연못": 0,
    "맑은 하늘의 꽃": 0,
    "마녀의 그네": 1,
    "자정의 타락 천사": 0,
    "용과 봉황": 1,
    "대낮의 화원": 0,
    "길 잃은 순례자": 0,
    "전설을 잡아라": 2,
}

rc4_pool = {
    "열대야의 끝": 2,
    "영험한 찬가": 1,
    "휴식의 순간": 2,
    "에메랄드 틈새 경계": 1,
    "'빗속의' 선율": 2,
    "★~펑펑 소녀~★": 1,
    "망언": 2,
    "별하늘에 안부를": 3,
    "수증기 증후군": 2,
    "플래시 고스트": 3,
    "가을날 속삭임": 3,
    "괴도 콤비": 0,
    "굿나잇": 0,
    "고양이 리듬": 0,
    "기사의 대장장이": 0,
    "알려지지 않은 이름": 0,
    "새장의 장미": 0,
    "★~돌고 도는 인생~★": 0,
    "음료수 사는 날": 1,
}
rc3_pool = {
    "아침 안개": 6,
    "평온": 6,
    "황혼": 6,
    "분홍빛 꿈": 6,
    "고독한 연기": 6,
    "감로": 4,
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

init_frag_cnt = 43495
init_cert_cnt = 1000
init_ticket_cnt = 41
init_disk_cnt = 3600

init_state = CurrentState(
    init_frag_cnt,
    init_cert_cnt,
    char5_pool,
    char4_pool,
    rc5_pool,
    rc4_pool,
    rc3_pool,
    init_ticket_cnt,
    init_disk_cnt,
)

chitose_pickup = CharPickUp.load_pickup("chitose_pickup.json")
cur_char_pickup = CharPickUp(*chitose_pickup, (5, 3), init_mileage=10)
chitose_rc_pickup = RcPickUp.load_pickup("chitose_rc_pickup.json")
cur_rc_pickup = RcPickUp(*chitose_rc_pickup, (0, 0))

trial_cnt = 1000000
char_succ_thr = [("치토세", 3), ("프리지아", 1), ("테레사", 1)]
rc_succ_thr = [("반짝이는 옛 연못", 1)]


def run_single_trial(_):
    is_succ, state = cur_char_pickup.simulate_trial(init_state, char_succ_thr)
    if not is_succ:
        return False

    is_succ = cur_rc_pickup.simulate_trial(state, rc_succ_thr)[0]
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
# is_succ, new_state = cur_char_pickup.simulate_trial(init_state, char_succ_thr)
# if is_succ:
#     is_succ, new_state = cur_rc_pickup.simulate_trial(new_state, rc_succ_thr)
# print(is_succ)
# print(new_state)
