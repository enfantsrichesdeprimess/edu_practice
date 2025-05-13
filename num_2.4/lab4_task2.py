import sqlite3

con = sqlite3.connect("task2.db")

with open('task2.sql', 'r') as file:
    create_table = file.read()

con.executescript(create_table)
con.commit()


def add_drink():
    cursor = con.cursor()
    name = input("Введите название напитка: ")
    alcohol_percentage = int(input("Введите крепкость напитка: ")) / 100
    price = float(input("Цена за литр: "))

    cursor.execute("insert INTO drink values (null, ?, ?, ?)",(name, alcohol_percentage, price))

    con.commit()
    print("Напиток добавлен.")


def add_ingredient():
    cursor = con.cursor()

    name = input("Введите название ингредиента: ")

    cursor.execute("insert INTO ingredient values (null, ?)", (name,))

    con.commit()
    print("Ингредиент добавлен.")


def add_cocktail():
    cursor = con.cursor()
    name = input("Введите название коктейля: ")
    price = float(input("Введите цену коктейля: "))

    cursor.execute("insert INTO cocktails values (null, ?, -1, ?)",
                   (name, price))

    con.commit()
    print("Коктейль добавлен.")


def add_component_to_cocktail(is_ingredient=False):
    cursor = con.cursor()
    cocktail_id = int(input("Введите номер коктейля: "))
    component_id = int(input("Введите номер напитка: "))
    volume = float(input("Введите объем напитка в коктейле: "))

    table = "drink"
    if is_ingredient:
        table = "ingredient"

    cursor.execute(f"insert INTO {table}s values (null, ?, ?, ?)", (cocktail_id, component_id, volume))

    update_cocktail_alcohol_percentage(cursor.lastrowid)
    print("Напиток добавлен в коктейль.")
    con.commit()

def remove_component_from_cocktail(is_ingredient=False):
    cursor = con.cursor()
    cocktail_id = int(input("Введите номер коктейля: "))
    component_id = int(input("Введите номер компонента: "))

    table = "drink"
    if is_ingredient:
        table = "ingredient"

    cursor.execute(f"delete from {table}s where cocktail=? and {table}=?",
                   (cocktail_id, component_id))

    print("Компонент удалён из коктейля.")
    con.commit()

    update_cocktail_alcohol_percentage(cursor.lastrowid)

def update_cocktail_alcohol_percentage(cocktail_id):
    cursor = con.cursor()

    cursor.execute("""
    update cocktails
    set alcohol_percentage = round((
    select COALESCE(sum(drinks.volume * alcohol_percentage),0) / 
    (select COALESCE(sum(ingredients.volume), 0) + (select COALESCE(sum(drinks.volume), 0) from drinks where cocktail = ?) 
    from ingredients where cocktail = ?) from drinks
    inner join drink on drink.id = drink
    where cocktail = ?
    ), 2)
    where id = ?;
    """, (cocktail_id, cocktail_id, cocktail_id, cocktail_id))

    con.commit()
    print("Крепкость обновлена!")


def sell_drink_or_cocktail(is_cocktail=False):
    cursor = con.cursor()
    drink_id = int(input("Введите номер: "))
    quantity = int(input("Введите количество: "))
    volume = float(input("Введите количество: "))
    price = float(input("Введите сумму закупки: "))

    table = "drink"
    if is_cocktail:
        table = "cocktail"

    cursor.execute(f"insert INTO sells_{table} values (null, date(), ?, ?, ?, ?)",
                   (drink_id, volume, quantity, price))

    con.commit()
    print("Продажа успешна")


def replenish_ingredient_stock(is_ingredient=False):
    cursor = con.cursor()
    ingredient_id = int(input("Введите ID ингредиента: "))
    quantity = float(input("Введите количество пополнения: "))
    volume = float(input("Введите объем(литры) пополнения: "))
    price = float(input("Введите сумму закупки: "))

    table = "drink"
    if is_ingredient:
        table = "ingredient"

    cursor.execute(f"insert INTO supply_{table} values (null, date(), ?, ?, ?, ?)",
                   (ingredient_id, volume, quantity, price))
    con.commit()
    print("Запас ингредиента пополнен")



def list_drinks():
    cursor = con.cursor()
    cursor.execute("select * FROM drink")
    drinks = cursor.fetchall()

    print("Список напитков:")
    if not drinks:
        print("Пусто")
        return

    for drink in drinks:
        print(f"№: {drink[0]}; Название: {drink[1]}; Крепость: {drink[2]}; Цена за литр: {drink[3]}")


def list_ingredients():
    cursor = con.cursor()
    cursor.execute("select * FROM ingredient")
    ingredients = cursor.fetchall()

    print("Список ингредиентов:")
    if not ingredients:
        print("Пусто")
        return

    for ingredient in ingredients:
        print(f"ID: {ingredient[0]}, Название: {ingredient[1]}")


def list_cocktails():
    cursor = con.cursor()
    cursor.execute("select * FROM cocktails")
    cocktails = cursor.fetchall()

    print("Список коктейлей:")

    if not cocktails:
        print("Пусто")
        return

    for cocktail in cocktails:
        print(f"№: {cocktail[0]}; Название: {cocktail[1]}; Крепкость: {cocktail[2]}; Цена: {cocktail[3]}")

        print("Ингредиенты в составе:")

        ingredients = cursor.execute("""
        select ingredient.name, volume from ingredients
        inner join ingredient on ingredient.id = ingredient
        where ingredients.cocktail = ?
        """,(cocktail[0],)).fetchall()
        if not ingredients:
            print("Пусто")
        else:
            for x in ingredients:
                print(f"{x[0]} в объёме {x[1]}")

        print("\nНапитки в составе:")

        drinks = cursor.execute("""
        select drink.name , alcohol_percentage, volume FROM  drinks
        inner join drink on drinks.drink = drink.id
        where drinks.cocktail = ?
        """, (cocktail[0],)).fetchall()
        if not drinks:
            print("Пусто")
        else:
            for x in drinks:
                print(f"{x[0]} в объёме {x[1]}")


while True:
    print("Выберите действие:\n"
    "1 - Добавить напиток\n"
    "2 - Добавить ингредиент\n"
    "3 - Добавить коктейль\n"
    "4. - Добавить напиток в коктейль\n"
    "5 - Добавить ингредиент в коктейль\n"
    "6 - Убрать напиток из коктейля\n"
    "7 - Убрать ингредиент из коктейля\n"
    "8 - Продать напиток\n"
    "9 - Продать коктейль\n"
    "10 - Пополнить запас ингредиента\n"
    "11 - Пополнить запас напитков\n"
    "12 - Список напитков\n"
    "13 - Список ингредиентов\n"
    "14 - Список коктейлей\n"
    "15 - Выход\n")

    try:
        choice = int(input("Введите номер действия:"))
    except:
        print("Введите номер!")
        continue

    if choice == 1:
        add_drink()
    elif choice == 2:
        add_ingredient()
    elif choice == 3:
        add_cocktail()
    elif choice == 4:
        add_component_to_cocktail()
    elif choice == 5:
        add_component_to_cocktail(True)
    elif choice == 6:
        remove_component_from_cocktail()
    elif choice == 7:
        remove_component_from_cocktail(True)
    elif choice == 8:
        sell_drink_or_cocktail()
    elif choice == 9:
        sell_drink_or_cocktail(True)
    elif choice == 10:
        replenish_ingredient_stock()
    elif choice == 11:
        replenish_ingredient_stock(True)
    elif choice == 12:
        list_drinks()
    elif choice == 13:
        list_ingredients()
    elif choice == 14:
        list_cocktails()
    elif choice == 15:
        break
    else:
        print("Некорректный ввод.")
        continue

    print()
    input("Нажмите enter для продолжения")