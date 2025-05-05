class Student:
    def __init__(self,first_name,birthday,group_number,academic_perfomance):
        self.first_name = first_name
        self.birthday = birthday
        self.group_number = group_number
        self.academic_performance = academic_perfomance

    def refactor_first_name(self, new_first_name):
        self.first_name = new_first_name

    def refactor_birthday(self, new_birthday):
        self.birthday = new_birthday

    def refactor_group_number(self, new_group_number):
        self.group_number = new_group_number

    def info(self):
        print(f"Фамилия студента: {self.first_name}\n",
              f"Дата рождения студента: {self.birthday}\n",
              f"Номер группы студента: {self.group_number}\n",
              f"Успеваемость студента: {self.academic_performance}")

def search():
    search_first_name = input("Введите фамилию студента которого хотите найти: ")
    search_birthday = input("Введите дату рождения в формате дд.мм.гггг: ")
    if search_first_name == student.first_name and search_birthday == student.birthday:
        print(f"Студент найден\n"
              f"{student.info()}")
    else:
        print("Такого студента не найдено")



student = Student("Забиралов",
                  "10.11.2006",
                  "632",
                  ["5","5","5","5","5"])
while True:
    i = int(input(("Выберите что хотите сделать:\n"
      "1 - отобразить информацию о студенте\n"
      "2 - изменить фамимлию\n"
      "3 - изменить дату рождения\n"
      "4 - изменить номер группы\n"
      "5 - поиск студента\n"
      "6 - завершить работу\n")))
    if i == 1:
        student.info()
    if i == 2:
        student.refactor_first_name(input("Введите новую фамилию студента: "))
        print(f"Новая фамилия: {student.first_name}")
    if i == 3:
        student.refactor_birthday(input("Введите новую дату рождения: "))
        print(f"Новая дата рождения: {student.birthday}")
    if i == 4:
        student.refactor_group_number(input("Введите новый номер группы: "))
        print(f"Новая группа студента: {student.group_number}")
    if i == 5:
        search()
    if i == 6:
        break





