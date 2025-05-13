import sqlite3

con = sqlite3.connect("task1.db")

create_table = """
create table if not exists student(
id integer primary key,
name char(26) not null,
surname char(26) not null,
lastname char(26) not null,
group_number int not null
);

create table if not exists grades(
id integer primary key,
student_id int references student(id),
grade int not null check(grade between 2 and 5)
);
"""

con.executescript(create_table)
con.commit()


class Student:
    @staticmethod
    def from_result_set(info, grades=None):
        return Student(info[0], info[1], info[2], info[3], info[4], grades, info[5] if len(info) >= 6 else None)

    @staticmethod
    def from_list_result_set_without_grades(lst):
        return list(map(lambda x: Student.from_result_set(x), lst))

    def __init__(self, student_id: int, name: str, surname: str, lastname: str, group: int, grades: [int] = None,
                 average_grade: int = None):
        self.id = student_id
        self.name = name
        self.surname = surname
        self.lastname = lastname
        self.group = group
        self.average = average_grade
        self.grades = grades

        if grades is not None:
            self.validate_grades()

            self.calculate_average_grade()

    def print_information(self):
        print(f"№: {self.id}; ФИО: {self.name} {self.surname} {self.lastname}; Группа: {self.group}")

        if self.average is not None:
            print("Средний балл:", self.average)
        if self.grades is not None:
            print("Оценки:", *self.grades)

    def calculate_average_grade(self):
        self.average = 0

        for x in self.grades:
            self.average += x

        self.average /= len(self.grades)

    def validate_grades(self):
        if len(self.grades) != 4:
            raise ValueError("Оценок должно быть ровно 4!")

        for x in self.grades:
            if x not in (2, 3, 4, 5):
                raise ValueError("Оценки должны быть!")


def add_student(student):
    cursor = con.cursor()
    cursor.execute("insert into student values (null, ?, ?, ?, ?)",
                   (student.name, student.surname, student.lastname, student.group))

    student_id = cursor.lastrowid

    ids = [student_id for x in range(len(student.grades))]

    grades_to_insert = zip(ids, student.grades)

    cursor.executemany("insert into grades values (null, ?, ?)", grades_to_insert)
    con.commit()


def view_all():
    cursor = con.cursor()
    cursor.execute("select * FROM student")
    rows = Student.from_list_result_set_without_grades(cursor.fetchall())

    print("\nСписок всех студентов:")
    if len(rows) == 0:
        print("Пусто")
        return

    for x in rows:
        x.print_information()


def view_student():
    cursor = con.cursor()

    id = int(input("Номер студента для просмотра:"))

    cursor.execute("select * FROM student WHERE id=?", (id,))

    student = cursor.fetchone()

    if not student:
        print("Студент не найден")
        return

    cursor.execute("select grade FROM grades WHERE student_id=?", (id,))
    grades_res = cursor.fetchall()

    grades = tuple(zip(*grades_res))[0]

    student = Student.from_result_set(student, grades)

    print(f"Информация о студенте:")
    student.print_information()


def edit_student():
    cursor = con.cursor()

    id = int(input("Номер студента для редактирования:"))

    cursor.execute("select * FROM student WHERE id=?", (id,))
    student = cursor.fetchone()

    if not student:
        print("Студент не найден")
        return

    cursor.execute("select id, grade from grades where student_id=?", (id,))
    grades_id, grades = tuple(zip(*cursor.fetchall()))

    student = Student.from_result_set(student, grades)

    print("Изменяемый студент")
    student.print_information()

    print("(Пропустите значения если не хотите их изменения)")

    new_name = input("Новое имя: ")
    new_surname = input("Новая фамилия: ")
    new_lastname = input("Новое отчество: ")
    new_group = input("Новая группа: ")
    new_grades = input("Оценки (через пробел):")

    try:
        new_grades = list(map(int, new_grades.split()))
        if new_group != "":
            int(new_group)
    except:
        print("Введены неправильные данные группы и/или оценках")
        return

    if new_grades != "":
        if len(new_grades) ==4 or all(x in (2,3,4,5) for x in new_grades):
            cursor.executemany("update grades set grade=? where id=?", zip(new_grades,grades_id))
        else:
            print("Оценок должно быть 4 и они должны быть цифрами!")
            return

    if new_name != "":
        cursor.execute("update student set name=? where id=?", (new_name, id))
    if new_surname != "":
        cursor.execute("update student set surname=? where id=?", (new_surname, id))
    if new_lastname != "":
        cursor.execute("update student set lastname=? where id=?", (new_lastname, id))
    if new_group != "":
        cursor.execute("update student set group_number=? where id=?", (int(new_group), id))

    print("Применено!")
    con.commit()


def delete_student():
    cursor = con.cursor()

    id = int(input("Номер студента для удаления:"))

    cursor.execute("delete FROM student WHERE id=?", (id,))
    cursor.execute("delete FROM grades WHERE student_id=?", (id,))

    if cursor.rowcount != 0:
        print("Удалено!")
    else:
        print("Удалять нечего")
    con.commit()


def group_avg_grade():
    cursor = con.cursor()

    group_number = int(input("Введите номер группы: "))

    cursor.execute(
        """
        select student.id, student.name, student.surname, student.lastname, student.group_number, AVG(grade) FROM student 
        inner JOIN grades ON student.id = grades.student_id
        where group_number = ? 
        group by student.id 
        """, (group_number,))

    students_of_group = Student.from_list_result_set_without_grades(cursor.fetchall())

    print("\nСредние оценки в группе:")

    if len(students_of_group) == 0:
        print("Пусто")
        return

    for x in students_of_group:
        x.print_information()


while True:
    print("Меню:")
    print("1 - добавить студента")
    print("2 - вывести всех студентов")
    print("3 - просмотреть информацию о студенте")
    print("4 - редактировать данные студента")
    print("5 - удалить студента")
    print("6 - средние оценки по группам")
    print("7 - выйти из программы")

    try:
        choice = int(input("Введите номер действия:"))
    except:
        print("Введите номер!")
        continue

    print()

    if choice == 1:
        name = input("Имя:")
        surname = input("Фамилия:")
        lastname = input("Отчество:")
        group = int(input("Номер группы:"))
        grades = list(map(int, input("Оценки (через пробел):").split()))

        try:
            student = Student(-1, name, surname, lastname, group, grades, 0)
            add_student(student)
        except ValueError as err:
            print(err)

    elif choice == 2:
        view_all()
    elif choice == 3:
        view_student()
    elif choice == 4:
        edit_student()
    elif choice == 5:
        delete_student()
    elif choice == 6:
        group_avg_grade()
    elif choice == 7:
        break
    else:
        print("Неверный выбор")
        continue

    print()
    input("Нажмите enter для продолжения")