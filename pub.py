"""The entry point of the application."""
import json

def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_data(data, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)


def list_drinks(drinks):
    for idx, drink in enumerate(drinks, start=1):
        if drink['stock'] > 0:
            print(f"{idx} - {drink['name']}: {drink['price']} Ft/{drink['unit']}")


def list_guests(guests):
    for idx, guest in enumerate(guests, start=1):
        print(f"{idx} - {guest['name']}: {guest['balance']} Ft")


def new_guest(guests):
    name = input("Adja meg az új törzsvendég nevét: ")
    for guest in guests:
        if guest['name'] == name:
            print("Hiba: Ez a név már létezik!")
            return
    guests.append({"name": name, "balance": 0})
    save_data(guests, "data/guests.json")
    print(f"{name} sikeresen hozzáadva.")

def purchase(guests, drinks):
    list_guests(guests)
    guest_idx = int(input("Válasszon vendéget: "))
    if guest_idx < 0 or guest_idx > len(guests):
        return
    guest = guests[guest_idx - 1]

    list_drinks(drinks)
    drink_idx = int(input("Válasszon italt: "))
    if drink_idx <= 0 or drink_idx > len(drinks):
        return
    drink = drinks[drink_idx - 1]

    quantity = -1
    while quantity < 0 or quantity * drink['price'] > guest['balance']:
        quantity = int(input("Mennyiség dl egységben: "))
        if quantity < 0:
            print("Nemnegatív egész számot adjon meg!")
        elif quantity * drink['price'] > guest['balance']:
            print("Nincs elég készlet vagy egyenleg!")
    
    if quantity == 0:
        return

    sum = quantity * drink['price']
    guest['balance'] -= sum
    drink['stock'] -= quantity

    save_data(guests, "data/guests.json")
    save_data(drinks, "data/drinks.json")
    print(f"+{sum} Ft {guest['name']} számlájára írva, egyenleg: {guest['balance']} Ft")

def payment(guests):
    list_guests(guests)
    guest_idx = int(input("Válasszon vendéget: "))
    if guest_idx < 0 or guest_idx > len(guests):
        return
    guest = guests[guest_idx - 1]

    amount = int(input("Adja meg a befizetett összeget: "))
    guest['balance'] += amount
    save_data(guests, "data/guests.json")
    print(f"{guest['name']} egyenlege frissítve: {guest['balance']} Ft")

def admin(drinks):
    while True:
        print("\nItalkészlet:")
        for idx, drink in enumerate(drinks, start=1):
            print(f"{idx} - {drink['name']}: {drink['price']} Ft/{drink['unit']} - Készlet: {drink['stock']}")
        print("0 - Vissza")
        print("4 - Új ital hozzáadása")
        option = int(input("Válasszon italt: "))
        if option == 0:
            return
        elif option == 4:
            new_drink(drinks)
        else:
            modify_drink(drinks, option)

def new_drink(drinks):
    name = input("Az új ital neve: ")
    unit = input("Az új ital kiszerelése (pl. dl): ")
    price = int(input("Az új ital ára: "))
    stock = int(input("Az új ital készlete: "))
    
    for drink in drinks:
        if drink['name'] == name and drink['unit'] == unit:
            print("Hiba: Azonos nevű és kiszerelésű ital már létezik!")
            return

    drinks.append({"name": name, "unit": unit, "price": price, "stock": stock})
    save_data(drinks, "data/drinks.json")
    print(f"{name} hozzáadva az italkészlethez.")

def modify_drink(drinks, idx):
    drink = drinks[idx - 1]
    print(f"Jelenlegi adatok: {drink}")
    drink['name'] = input(f"Új név[{drink['name']}]: ") or drink['name']
    drink['unit'] = input(f"Új kiszerelés[{drink['unit']}]: ") or drink['unit']
    drink['price'] = int(input(f"Új ár[{drink['price']}]: ") or drink['price'])
    drink['stock'] = int(input(f"Új készlet[{drink['stock']}]: ") or drink['stock'])
    
    save_data(drinks, "data/drinks.json")
    print("Ital módosítva.")

def run():
    guests = load_data("data/guests.json")
    drinks = load_data("data/drinks.json")
    
    while True:
        print("\nFőmenü:")
        print("0 - Kilépés")
        print("1 - Pénztáros mód")
        print("2 - Admin mód")
        option = int(input("Válasszon menüpontot: "))
        
        if option == 0:
            break
        elif option == 1:
            while True:
                print("\nPénztáros mód:")
                print("0 - Vissza a főmenübe")
                print("1 - Új törzsvendég")
                print("2 - Rendelés")
                print("3 - Befizetés")
                sub_option = int(input("Válasszon menüpontot: "))
                
                if sub_option == 0:
                    break
                elif sub_option == 1:
                    new_guest(guests)
                elif sub_option == 2:
                    purchase(guests, drinks)
                elif sub_option == 3:
                    payment(guests)
                else:
                    print("Érvénytelen menüpont!")
        elif option == 2:
            admin(drinks)
        else:
            print("Érvénytelen menüpont!")
            
if __name__ == "__main__":
    run()

