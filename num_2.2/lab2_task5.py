class Class:
    def __init__(self, first=None, second=None):
        if first is None and second is None:
            self.first = 2
            self.second = 4
        else:
            self.first = first
            self.second = second
        print(f"создание обьекта, его свойства: {self.first}, {self.second}")

    def __del__(self):
        print(f"удален обьект, имеющий такие свойства:: {self.first}, {self.second}")


while True:
    obj_one = Class()
    obj_two = Class(input("Введите первое значение "),
                    input("Введите второе значение "))

    del obj_one
    del obj_two
    break