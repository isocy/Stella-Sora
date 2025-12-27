import copy
import json
import random

from state import *

# 0: 5★ char, 1: 4★ char, 2: 5★ rc, 3: 4★ rc 4: 3★ rc
collection_dict = {
    "라루(이브)": 0,
    "후유카": 0,
    "시아": 0,
    "치토세": 0,
    "나노하": 0,
    "프리지아": 0,
    "미네르바": 0,
    "미스티": 0,
    "치시아": 0,
    "그레이": 0,
    "나즈나": 0,
    "징린": 1,
    "테레사": 1,
    "코하쿠": 1,
    "틸리아": 1,
    "카시미라": 1,
    "아야메": 1,
    "세이나": 1,
    "시먀오": 1,
    "레이센": 1,
    "크루니스": 1,
    "카나체": 1,
    "안즈": 1,
    "플로라": 1,
    "코제트": 1,
    "캐러멜": 1,
    "라루": 1,
    "반짝이는 옛 연못": 2,
    "맑은 하늘의 꽃": 2,
    "마녀의 그네": 2,
    "자정의 타락 천사": 2,
    "용과 봉황": 2,
    "대낮의 화원": 2,
    "길 잃은 순례자": 2,
    "전설을 잡아라": 2,
    "열대야의 끝": 3,
    "괴도 콤비": 3,
    "★~펑펑 소녀~★": 3,
    "굿나잇": 3,
    "에메랄드 틈새 경계": 3,
    "휴식의 순간": 3,
    "'빗속의' 선율": 3,
    "수증기 증후군": 3,
    "고양이 리듬": 3,
    "별하늘에 안부를": 3,
    "가을날 속삭임": 3,
    "기사의 대장장이": 3,
    "알려지지 않은 이름": 3,
    "새장의 장미": 3,
    "★~돌고 도는 인생~★": 3,
    "음료수 사는 날": 3,
    "망언": 3,
    "플래시 고스트": 3,
    "아침 안개": 4,
    "평온": 4,
    "황혼": 4,
    "분홍빛 꿈": 4,
    "고독한 연기": 4,
    "감로": 4,
    "희망": 4,
    "귀로": 4,
    "성찬": 4,
    "소란": 4,
    "극락": 4,
    "열정": 4,
    "상서로운 빛": 4,
    "바람을 타고": 4,
    "물거품": 4,
    "검은 소멸": 4,
    "강인함": 4,
}


class Gacha:
    @staticmethod
    def save_gacha(contents, prs, file_path, pickup):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([[contents, prs], pickup], file, ensure_ascii=False, indent=4)

    @staticmethod
    def load_gacha(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            pr_pairs = json.load(file)
        return pr_pairs

    def get_target_pool(state, pull_id):
        if pull_id == 0:
            return state.char5_pool
        elif pull_id == 1:
            return state.char4_pool
        elif pull_id == 2:
            return state.rc5_pool
        elif pull_id == 3:
            return state.rc4_pool
        elif pull_id == 4:
            return state.rc3_pool
        else:
            raise ValueError("Invalid pull_id")


class CharGacha(Gacha):
    def __init__(self, pr_pairs, init_stack):
        self.contents = pr_pairs[0]
        self.prs = pr_pairs[1]

        char5_pool = []
        char4_pool = []
        for content in self.contents:
            pull_id = collection_dict[content]
            if pull_id == 0:
                char5_pool.append(content)
            elif pull_id == 1:
                char4_pool.append(content)
        self.char5_pool = char5_pool
        self.char4_pool = char4_pool

        self.init_stack = init_stack

    @staticmethod
    def save_gacha(contents, prs, file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([contents, prs], file, ensure_ascii=False, indent=4)

    def simulate_trial(self, state, succ_thr):
        state = copy.deepcopy(state)

        stack5, stack4 = self.init_stack

        frag_cnt = state.frag_cnt
        sprout_ticket_cnt = state.sprout_ticket_cnt
        cert_cnt = state.cert_cnt

        is_succ = False
        while sprout_ticket_cnt > 0 or cert_cnt >= 100 or frag_cnt >= 300:
            if sprout_ticket_cnt > 0:
                sprout_ticket_cnt -= 1

                pulled = random.choices(self.contents, weights=self.prs, k=1)[0]
                if pulled in Gacha.get_target_pool(state, 0).keys():
                    stack5, stack4 = 0, 0
                else:
                    stack5 += 1
                    if stack5 >= 160:
                        pulled = random.choices(self.char5_pool, k=1)[0]
                        stack5, stack4 = 0, 0
                    elif pulled in Gacha.get_target_pool(state, 4).keys():
                        stack4 += 1
                        if stack4 >= 10:
                            pulled = random.choices(self.char4_pool, k=1)[0]
                            stack4 = 0
                    else:
                        stack4 = 0
                pull_id = collection_dict[pulled]
                target_pool = Gacha.get_target_pool(state, pull_id)
                if target_pool[pulled] > 0:
                    if pull_id == 0:
                        cert_cnt += 200
                        if target_pool[pulled] == 6:
                            cert_cnt += 300
                        else:
                            target_pool[pulled] += 1
                    elif pull_id == 1:
                        cert_cnt += 40
                        if target_pool[pulled] == 11:
                            cert_cnt += 30
                        else:
                            target_pool[pulled] += 1
                    elif pull_id == 3:
                        cert_cnt += 40
                        if target_pool[pulled] == 6:
                            cert_cnt += 40
                        else:
                            target_pool[pulled] += 1
                    elif pull_id == 4:
                        if target_pool[pulled] < 6:
                            target_pool[pulled] += 1
                else:
                    target_pool[pulled] += 1

                is_succ = True
                for content, cnt in succ_thr:
                    if (
                        Gacha.get_target_pool(state, collection_dict[content])[content]
                        < cnt
                    ):
                        is_succ = False
                        break
                else:
                    break
            elif cert_cnt >= 100:
                cert_cnt -= 100
                sprout_ticket_cnt += 1
            else:
                frag_cnt -= 300
                sprout_ticket_cnt += 1

        return is_succ, CurrentState(
            frag_cnt,
            cert_cnt,
            state.char5_pool,
            state.char4_pool,
            state.rc5_pool,
            state.rc4_pool,
            state.rc3_pool,
            sprout_ticket_cnt,
            state.sky_ticket_cnt,
            state.disk_cnt,
        )


class CharPickUp(Gacha):
    # init_mileage: -1이면 이미 마일리지 사용
    def __init__(self, pr_pairs, pickup, init_stack, init_mileage=0):
        self.pickup = pickup
        self.contents = pr_pairs[0]
        self.prs = pr_pairs[1]

        char4_pool = []
        for content in self.contents:
            pull_id = collection_dict[content]
            if pull_id == 1:
                char4_pool.append(content)
        self.char4_pool = char4_pool

        self.init_mileage = init_mileage
        self.init_stack = init_stack

    def simulate_trial(self, state, succ_thr):
        state = copy.deepcopy(state)

        mileage = self.init_mileage
        stack5, stack4 = self.init_stack

        frag_cnt = state.frag_cnt
        sky_ticket_cnt = state.sky_ticket_cnt
        cert_cnt = state.cert_cnt

        is_succ = False
        while sky_ticket_cnt > 0 or cert_cnt >= 100 or frag_cnt >= 300:
            if sky_ticket_cnt > 0:
                sky_ticket_cnt -= 1
                if mileage != -1:
                    mileage += 1

                pulled = random.choices(self.contents, weights=self.prs, k=1)[0]
                if pulled == self.pickup:
                    stack5, stack4 = 0, 0
                else:
                    stack5 += 1
                    if stack5 >= 160:
                        pulled = self.pickup
                        stack5, stack4 = 0, 0
                    elif pulled in Gacha.get_target_pool(state, 4).keys():
                        stack4 += 1
                        if stack4 >= 10:
                            pulled = random.choices(self.char4_pool, k=1)[0]
                            stack4 = 0
                    else:
                        stack4 = 0
                pull_id = collection_dict[pulled]
                target_pool = Gacha.get_target_pool(state, pull_id)
                if target_pool[pulled] > 0:
                    if pull_id == 0:
                        cert_cnt += 200
                        if target_pool[pulled] == 6:
                            cert_cnt += 300
                        else:
                            target_pool[pulled] += 1
                    elif pull_id == 1:
                        cert_cnt += 40
                        if target_pool[pulled] == 11:
                            cert_cnt += 30
                        else:
                            target_pool[pulled] += 1
                    elif pull_id == 3:
                        cert_cnt += 40
                        if target_pool[pulled] == 6:
                            cert_cnt += 40
                        else:
                            target_pool[pulled] += 1
                    elif pull_id == 4:
                        if target_pool[pulled] < 6:
                            target_pool[pulled] += 1
                else:
                    target_pool[pulled] += 1

                if mileage == 120:
                    mileage = -1
                    Gacha.get_target_pool(state, 0)[self.pickup] += 1

                is_succ = True
                for content, cnt in succ_thr:
                    if (
                        Gacha.get_target_pool(state, collection_dict[content])[content]
                        < cnt
                    ):
                        is_succ = False
                        break
                else:
                    break
            elif cert_cnt >= 100:
                cert_cnt -= 100
                sky_ticket_cnt += 1
            else:
                frag_cnt -= 300
                sky_ticket_cnt += 1

        return is_succ, CurrentState(
            frag_cnt,
            cert_cnt,
            state.char5_pool,
            state.char4_pool,
            state.rc5_pool,
            state.rc4_pool,
            state.rc3_pool,
            state.sprout_ticket_cnt,
            sky_ticket_cnt,
            state.disk_cnt,
        )


class RcPickUp(Gacha):
    # init_mileage: -1이면 이미 마일리지 사용
    def __init__(self, pr_pairs, pickup, init_stack):
        self.pickup = pickup
        self.contents = pr_pairs[0]
        self.prs = pr_pairs[1]

        rc4_pool = []
        for content in self.contents:
            pull_id = collection_dict[content]
            if pull_id == 3:
                rc4_pool.append(content)
        self.rc4_pool = rc4_pool

        self.init_stack = init_stack

    def simulate_trial(self, state, succ_thr):
        state = copy.deepcopy(state)

        stack5, stack4 = self.init_stack

        frag_cnt = state.frag_cnt
        disk_cnt = state.disk_cnt
        cert_cnt = state.cert_cnt

        is_succ = False
        while disk_cnt >= 300 or cert_cnt >= 100 or frag_cnt >= 300:
            if disk_cnt >= 300:
                disk_cnt -= 300

                pulled = random.choices(self.contents, weights=self.prs, k=1)[0]
                if pulled == self.pickup:
                    stack5, stack4 = 0, 0
                else:
                    stack5 += 1
                    if stack5 >= 120:
                        pulled = self.pickup
                        stack5, stack4 = 0, 0
                    elif pulled in Gacha.get_target_pool(state, 4).keys():
                        stack4 += 1
                        if stack4 >= 10:
                            pulled = random.choices(self.rc4_pool, k=1)[0]
                            stack4 = 0
                    else:
                        stack4 = 0
                pull_id = collection_dict[pulled]
                target_pool = Gacha.get_target_pool(state, pull_id)
                if target_pool[pulled] > 0:
                    if pull_id == 2:
                        cert_cnt += 200
                        if target_pool[pulled] == 6:
                            cert_cnt += 200
                        else:
                            target_pool[pulled] += 1
                    elif pull_id == 3:
                        cert_cnt += 40
                        if target_pool[pulled] == 6:
                            cert_cnt += 40
                        else:
                            target_pool[pulled] += 1
                    elif pull_id == 4:
                        if target_pool[pulled] < 6:
                            target_pool[pulled] += 1
                else:
                    target_pool[pulled] += 1

                is_succ = True
                for content, cnt in succ_thr:
                    if (
                        Gacha.get_target_pool(state, collection_dict[content])[content]
                        < cnt
                    ):
                        is_succ = False
                        break
                else:
                    break
            elif cert_cnt >= 100:
                cert_cnt -= 100
                disk_cnt += 300
            else:
                frag_cnt -= 300
                disk_cnt += 300

        return is_succ, CurrentState(
            frag_cnt,
            cert_cnt,
            state.char5_pool,
            state.char4_pool,
            state.rc5_pool,
            state.rc4_pool,
            state.rc3_pool,
            state.sprout_ticket_cnt,
            state.sky_ticket_cnt,
            disk_cnt,
        )


if __name__ == "__main__":
    pass

    # 캐릭터 상시 가챠
    # char_contents = [
    #     "나노하",
    #     "프리지아",
    #     "미네르바",
    #     "미스티",
    #     "치시아",
    #     "그레이",
    #     "나즈나",
    #     "코하쿠",
    #     "틸리아",
    #     "카시미라",
    #     "아야메",
    #     "세이나",
    #     "시먀오",
    #     "레이센",
    #     "징린",
    #     "크루니스",
    #     "카나체",
    #     "안즈",
    #     "플로라",
    #     "테레사",
    #     "코제트",
    #     "캐러멜",
    #     "라루",
    #     "열대야의 끝",
    #     "괴도 콤비",
    #     "★~펑펑 소녀~★",
    #     "굿나잇",
    #     "에메랄드 틈새 경계",
    #     "휴식의 순간",
    #     "'빗속의' 선율",
    #     "수증기 증후군",
    #     "고양이 리듬",
    #     "별하늘에 안부를",
    #     "가을날 속삭임",
    #     "기사의 대장장이",
    #     "알려지지 않은 이름",
    #     "새장의 장미",
    #     "★~돌고 도는 인생~★",
    #     "음료수 사는 날",
    #     "망언",
    #     "플래시 고스트",
    #     "아침 안개",
    #     "평온",
    #     "황혼",
    #     "분홍빛 꿈",
    #     "고독한 연기",
    #     "감로",
    #     "희망",
    #     "귀로",
    #     "성찬",
    #     "소란",
    #     "극락",
    #     "열정",
    #     "상서로운 빛",
    #     "바람을 타고",
    #     "물거품",
    #     "검은 소멸",
    #     "강인함",
    # ]
    # char_prs = [2 / 7] * 7 + [1 / 4] * 16 + [2 / 9] * 18 + [90 / 17] * 17

    # CharGacha.save_gacha(char_contents, char_prs, "char_gacha.json")

    # 캐릭터 픽업
    char_contents = [
        "라루(이브)",
        "크루니스",
        "플로라",
        "나노하",
        "프리지아",
        "미네르바",
        "미스티",
        "치시아",
        "그레이",
        "나즈나",
        "코하쿠",
        "틸리아",
        "카시미라",
        "아야메",
        "세이나",
        "시먀오",
        "레이센",
        "징린",
        "카나체",
        "안즈",
        "테레사",
        "코제트",
        "캐러멜",
        "라루",
        "열대야의 끝",
        "괴도 콤비",
        "★~펑펑 소녀~★",
        "굿나잇",
        "에메랄드 틈새 경계",
        "휴식의 순간",
        "'빗속의' 선율",
        "수증기 증후군",
        "고양이 리듬",
        "별하늘에 안부를",
        "가을날 속삭임",
        "기사의 대장장이",
        "알려지지 않은 이름",
        "새장의 장미",
        "★~돌고 도는 인생~★",
        "음료수 사는 날",
        "망언",
        "플래시 고스트",
        "아침 안개",
        "평온",
        "황혼",
        "분홍빛 꿈",
        "고독한 연기",
        "감로",
        "희망",
        "귀로",
        "성찬",
        "소란",
        "극락",
        "열정",
        "상서로운 빛",
        "바람을 타고",
        "물거품",
        "검은 소멸",
        "강인함",
    ]
    char_prs = [1] * 3 + [1 / 7] * 21 + [2 / 9] * 18 + [90 / 17] * 17
    char_pickup = "라루(이브)"

    CharPickUp.save_gacha(
        char_contents, char_prs, "snowish_laru_pickup.json", char_pickup
    )

    # 레코드 픽업
    # rc_contents = [
    #     "반짝이는 옛 연못",
    #     "★~펑펑 소녀~★",
    #     "'빗속의' 선율",
    #     "맑은 하늘의 꽃",
    #     "마녀의 그네",
    #     "자정의 타락 천사",
    #     "용과 봉황",
    #     "대낮의 화원",
    #     "길 잃은 순례자",
    #     "전설을 잡아라",
    #     "열대야의 끝",
    #     "괴도 콤비",
    #     "굿나잇",
    #     "에메랄드 틈새 경계",
    #     "휴식의 순간",
    #     "수증기 증후군",
    #     "고양이 리듬",
    #     "별하늘에 안부를",
    #     "가을날 속삭임",
    #     "기사의 대장장이",
    #     "알려지지 않은 이름",
    #     "새장의 장미",
    #     "★~돌고 도는 인생~★",
    #     "음료수 사는 날",
    #     "망언",
    #     "플래시 고스트",
    #     "아침 안개",
    #     "평온",
    #     "황혼",
    #     "분홍빛 꿈",
    #     "고독한 연기",
    #     "감로",
    #     "희망",
    #     "귀로",
    #     "성찬",
    #     "소란",
    #     "극락",
    #     "열정",
    #     "상서로운 빛",
    #     "바람을 타고",
    #     "물거품",
    #     "검은 소멸",
    #     "강인함",
    # ]
    # rc_prs = [1.5] + [2] * 2 + [1 / 14] * 7 + [1 / 4] * 16 + [90 / 17] * 17
    # rc_pickup = "반짝이는 옛 연못"

    # RcPickUp.save_gacha(rc_contents, rc_prs, rc_pickup, "chitose_rc_pickup.json")
