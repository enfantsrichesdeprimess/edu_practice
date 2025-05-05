class Numbers:
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def info_numbers(self):
        print(f"Числа: {self.num1}, {self.num2}")

    def refactor_numbers(self, new_num1, new_num2):
        self.num1 = new_num1
        self.num2 = new_num2

    def get_sum(self):
        return self.num1 + self.num2

    def get_max(self):
        return max(self.num1, self.num2)

numbers = Numbers(7,2)

while True:
    i = int(input(("Выберите что хотите сделать:\n"
      "1 - отобразить числа\n"
      "2 - изменить значения\n"
      "3 - вывести сумму чисел\n"
      "4 - найти наибольшее\n"
      "5 - выйти\n"
      )))
    if i == 1:
        numbers.info_numbers()
    if i == 2:
       numbers.refactor_numbers(int(input("Введите первое число ")),
                                int(input("Введите второе число "))
                                )
    if i == 3:
        print(f"сумма чисел - {numbers.get_sum()}")
    if i == 4:
        print(f"наибольшее число - {numbers.get_max()}")
    if i == 5:
        break