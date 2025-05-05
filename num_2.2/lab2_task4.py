class NumsCounter:
    def __init__(self, number=0):
        self.number = number

    def increment(self):
        self.number += 1

    def decrement(self):
        self.number -= 1

    def value(self):
        return self.number

number_for_counter = NumsCounter(int(input("Введите число счетчика: ")))

while True:
    i = int(input(("Выберите что хотите сделать:\n"
      "1 - отобразить состояние счетчика\n"
      "2 - добавить единицу\n"
      "3 - отнять единицу\n"
      "4 - выйти\n"
      )))
    if i == 1:
        print(number_for_counter.value())
    if i == 2:
        number_for_counter.increment()
    if i == 3:
       number_for_counter.decrement()
    if i == 4:
        break