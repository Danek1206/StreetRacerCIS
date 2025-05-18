import random
import json
import os
import sys

# Данные игрока
player = {
    "name": "",
    "country": "",
    "money": 10000,
    "car": None,
    "skills": {"driving": 50, "charisma": 30, "reputation": 0},
    "inventory": []
}

# Машины
cars = {
    "ВАЗ-2109": {"speed": 80, "acceleration": 70, "handling": 60, "reliability": 50, "price": 5000},
    "ГАЗ-3110": {"speed": 70, "acceleration": 60, "handling": 50, "reliability": 60, "price": 6000},
    "ВАЗ-2121": {"speed": 60, "acceleration": 50, "handling": 70, "reliability": 80, "price": 7000}
}

# Валюты
currencies = {
    "Россия": "RUB",
    "Беларусь": "BYN",
    "Казахстан": "KZT",
    "Таджикистан": "TJS",
    "Узбекистан": "UZS",
    "Грузия": "GEL"
}

# Сохранение и загрузка
def save_game():
    with open(os.path.join(os.path.dirname(sys.argv[0]), "save.json"), "w") as f:
        json.dump(player, f)
    print("Прогресс сохранён.")

def load_game():
    save_path = os.path.join(os.path.dirname(sys.argv[0]), "save.json")
    if os.path.exists(save_path):
        with open(save_path, "r") as f:
            global player
            player = json.load(f)
        print("Прогресс загружен.")
        return True
    return False

# Начало игры
def start_game():
    if load_game():
        return
    print("Ты — пацан с большой мечтой: покорить трассу и сердце той самой девчонки.")
    print("В кармане — 10,000 в местной валюте, в гараже — тишина.")
    try:
        player["name"] = input("Как звать, брат? ")
        print("Выбери страну: Россия, Беларусь, Казахстан, Таджикистан, Узбекистан, Грузия")
        player["country"] = input("Откуда ты? ")
        while player["country"] not in currencies:
            print("Такой страны нет, выбери снова.")
            player["country"] = input("Откуда ты? ")
        print(f"Бюджет: 10,000 {currencies[player['country']]}. Пора брать тачку и рвать!")
        save_game()
    except EOFError:
        print("Ввод прерван. Попробуй снова.")
        exit(1)

# Покупка машины
def buy_car():
    print("Базар с тачками:")
    for car, stats in cars.items():
        print(f"{car}: {stats['price']} {currencies[player['country']]} (Скорость: {stats['speed']}, Управляемость: {stats['handling']})")
    try:
        choice = input("Что берёшь? (напиши название или 'отмена'): ")
        if choice in cars and cars[choice]["price"] <= player["money"]:
            player["car"] = choice
            player["money"] -= cars[choice]["price"]
            print(f"Теперь у тебя {choice}! Остаток: {player['money']} {currencies[player['country']]}")
            save_game()
        elif choice == "отмена":
            print("Без тачки пока, брат.")
        else:
            print("Бабок не хватает или тачка не та. Выбирай снова.")
            buy_car()
    except EOFError:
        print("Ввод прерван.")
        exit(1)

# Гонка
def race():
    if not player["car"]:
        print("Без тачки на трассу не пускают. Купи что-нибудь!")
        return
    print("Выбирай: Кольцо, Спринт, Драг")
    try:
        discipline = input("Что гоняем? ").lower()
        car_stats = cars[player["car"]]
        print(f"\nТы на {player['car']}. Магнитола орёт, движок рычит.")
        print("Трасса: асфальт дымится, толпа ревёт. Противник — наглый тип на заниженной Приоре.")

        player_score = (car_stats["speed"] + car_stats["acceleration"] + car_stats["handling"] + player["skills"]["driving"]) // 4
        opponent_score = random.randint(60, 90)

        if discipline == "кольцо":
            print("Кольцо — три круга. Первый поворот: жёсткий, 90 градусов.")
            print("Жмёшь на газ или аккуратно входишь? (газ/аккуратно)")
            choice = input("Твой ход: ").lower()
            if choice == "газ" and car_stats["handling"] < 60:
                print("Занесло! Теряешь секунды, противник вырывается вперёд.")
                player_score -= 10
            elif choice == "аккуратно":
                print("Чётко вошёл, держишься за ним!")
                player_score += 5
            print("Финальный круг: рискнуть и обогнать? (риск/держаться)")
            choice = input("Твой ход: ").lower()
            if choice == "риск" and random.random() < 0.7:
                print("Обгон удался! Ты вырываешься вперёд!")
                player_score += 10
            elif choice == "риск":
                print("Слишком рискнул, чуть не влетел в отбойник!")
                player_score -= 15

        if random.random() < car_stats["reliability"] / 100:
            if player_score > opponent_score:
                winnings = 3000
                player["money"] += winnings
                player["skills"]["driving"] += 5
                player["skills"]["reputation"] += 10
                print(f"\nФиниш! Ты порвал всех, толпа орёт! Выигрыш: {winnings} {currencies[player['country']]}")
            else:
                print("\nФиниш... Противник обошёл на финише. Без призов, но опыт есть.")
                player["skills"]["driving"] += 2
        else:
            print("\nДвижок заглох! Ремонт: -1500.")
            player["money"] -= 1500
        save_game()
    except EOFError:
        print("Ввод прерван.")
        exit(1)

# Сюжет
def story_scene():
    print("\nВечер. Ты в гараже, крутишь гайки. В голове — она, та девчонка с гонки.")
    print("Кореш звонит: 'Бери тачку, заезд на районе. Победителю — бабки, но там мутный тип. Может предложить сдать гонку за 5000.'")
    print("Что делаешь? (гонка/договориться/отказаться)")
    try:
        choice = input("Твой выбор: ").lower()
        if choice == "гонка":
            print("Честная игра — твой путь. Погнали!")
            race()
        elif choice == "договориться":
            print("Встретился с типом. Он суёт 5000, но пацаны косо смотрят.")
            player["money"] += 5000
            player["skills"]["reputation"] -= 20
            save_game()
        else:
            print("Решил не лезть. Спокойно, но без движухи.")
        save_game()
    except EOFError:
        print("Ввод прерван.")
        exit(1)

# Главное меню
def main():
    start_game()
    while True:
        print(f"\n{player['name']}, что делаем? Бабки: {player['money']} {currencies[player['country']]}, Репа: {player['skills']['reputation']}")
        print("1. Купить тачку")
        print("2. На гонку")
        print("3. Сюжет")
        print("4. Выйти")
        try:
            choice = input("Твой выбор (1-4): ")
            if choice == "1":
                buy_car()
            elif choice == "2":
                race()
            elif choice == "3":
                story_scene()
            elif choice == "4":
                print("Сворачиваем с трассы? Возвращайся, братан!")
                break
            else:
                print("Не трынди, выбирай нормально.")
            save_game()
        except EOFError:
            print("Ввод прерван.")
            exit(1)

if __name__ == "__main__":
    main()