import random

# ==========================
# 플레이어 상태 초기화
# ==========================
player = {
    "level": 1,       # 낚싯대 레벨
    "money": 0,       # 재화
    "inventory": []   # 낚은 물고기 기록
}

# ==========================
# 물고기 리스트 및 원가 설정
# ==========================
fish_list = ["연어","대구","고등어","돔","꽃게","흰동가리","전갱이","광어","참치","갈치"]

# 순서대로 뒤로 갈수록 비싸지게
base_price = {}
start_price = 100
increment = 50
for i, f in enumerate(fish_list):
    base_price[f] = start_price + increment * i

# ==========================
# 낚싯대 강화 함수
# ==========================
def upgrade_rod(player):
    cost = player["level"] * 50
    print(f"\n현재 낚싯대 레벨: {player['level']}, 강화 비용: {cost}원")
    choice = input("강화하시겠습니까? (y/n) ")
    if choice.lower() == 'y':
        if player["money"] >= cost:
            player["money"] -= cost
            player["level"] += 1
            print(f"강화 성공! 현재 낚싯대 레벨: {player['level']}")
        else:
            print("재화가 부족합니다.")
    else:
        print("강화를 취소했습니다.")

# ==========================
# 상점
# ==========================
def shop(player):
    while True:
        print("\n=== 상점 ===")
        print(f"보유 금액: {player['money']}원")
        print("1. 낚싯대 강화")
        print("2. 종료")
        choice = input("선택: ")
        if choice == "1":
            upgrade_rod(player)
        elif choice == "2":
            break
        else:
            print("잘못된 선택입니다.")

# ==========================
# 낚시 함수
# ==========================
def fishing(player):
    # 1. 랜덤 물고기 선택
    fished = random.choice(fish_list)
    print("\n무언가가 낚였다!")
    print("낚인 물고기:", fished)

    # 2. 물고기 무게 설정
    weight_range = {
        "연어": (2, 5),
        "대구": (3, 12),
        "고등어": (0.3, 1.5),
        "돔": (1, 4),
        "꽃게": (0.2, 0.8),
        "흰동가리": (0.1, 0.4),
        "전갱이": (0.2, 1.2),
        "광어": (3, 10),
        "참치": (50, 300),
        "갈치": (0.5, 2)
    }
    min_w, max_w = weight_range[fished]
    weight = round(random.uniform(min_w, max_w), 2)
    print(f"예상 무게: {weight} kg")

    # 3. 시도 횟수 설정
    times = 20 if fished in ["참치", "갈치"] else 15

    # 4. 난이도(time)
    time_table = {
        "연어": 10, "대구": 15, "고등어": 15, "돔": 20,
        "꽃게": 30, "흰동가리": 20, "전갱이": 15,
        "광어": 30, "참치": 50, "갈치": 50
    }
    time = time_table[fished]
    total_time = time
    per = 0

    # 5. 낚시 루프
    while time > 0:
        if times == 0:
            print("낚시 실패... 남은 시도 횟수가 0입니다.")
            return None

        progress = per / total_time * 100
        choice = input(
            f"\n진행도 : {progress:.2f}%\n"
            f"남은 횟수 : {times}\n"
            "1 → 낚시 시도\n"
            "2 → 놓아주기\n"
            ">>> "
        )

        if choice == "1":
            print("낚시 중...")
            g = random.randint(1,5) + player["level"] - 1
            time -= g
            per += g
            times -= 1
            continue
        elif choice == "2":
            print("낚시를 끝냅니다.")
            return None
        else:
            print("잘못된 입력입니다. 다시 입력해주세요.")
            continue

    # 6. 낚시에 성공
    print(f"\n🎣 축하합니다! {fished} 를 낚았습니다!")
    print(f"무게는 {weight} kg 입니다!")

    # 7. 수익 계산
    if fished == "참치":
        money_earned = int(base_price[fished] * 0.01 * weight)
    else:
        money_earned = int(base_price[fished] * 0.1 * weight)

    player["money"] += money_earned
    print(f"{money_earned}원을 획득했습니다!")

    # 8. 인벤토리에 추가
    player["inventory"].append((fished, weight))
    return fished, weight

# ==========================
# 게임 루프
# ==========================
def game_loop():
    print("=== 낚시 게임 시작! ===")
    while True:
        print("\n=== 메뉴 ===")
        print("1. 낚시")
        print("2. 상점")
        print("3. 인벤토리 확인")
        print("4. 종료")
        choice = input("선택: ")
        if choice == "1":
            fishing(player)
        elif choice == "2":
            shop(player)
        elif choice == "3":
            print("\n=== 인벤토리 ===")
            if not player["inventory"]:
                print("낚은 물고기가 없습니다.")
            else:
                for idx, (name, w) in enumerate(player["inventory"], 1):
                    print(f"{idx}. {name} ({w} kg)")
            print(f"보유 금액: {player['money']}원")
            print(f"낚싯대 레벨: {player['level']}")
        elif choice == "4":
            print("게임 종료!")
            break
        else:
            print("잘못된 선택입니다.")

# ==========================
# 게임 시작
# ==========================
game_loop()
