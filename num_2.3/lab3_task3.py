class Calculation:
    def __init__(self, calculation_line):
        self.calculation_line = calculation_line

    def set_calculation_line(self,new_value_for_line):
        self.calculation_line = new_value_for_line

    def set_last_symbol_calculation_line(self,last_symbol):
        self.calculation_line += last_symbol

    def get_info_about_line(self):
        return self.calculation_line

    def get_last_symbol(self):
        if len(self.calculation_line) == 0:
            return ""
        else:
            return self.calculation_line[-1]

    def delete_last_symbol(self):
        self.calculation_line = self.calculation_line[:-1]

line = Calculation("")

while True:
    i = int(input(("Выберите что хотите сделать:\n"
      "1 -Отобразить значение\n"
      "2 -Изменить значение\n"
      "3 -Добавить значение в конец\n"
      "4 -Посмотреть последний символ\n"
      "5 -Удалить символ с конца\n"
      "6 - end.\n"
      )))
    if i == 1:
        print(f"Значение calculation_line - {line.get_info_about_line()}")
    if i == 2:
       line.set_calculation_line(input("Введите новое значение для calculation_line "))
    if i == 3:
        line.set_last_symbol_calculation_line(input("Введите символ в конец calculation_line "))
        print(f"теперь значение calculation_line - {line.get_info_about_line()}")
    if i == 4:
        print(f"последний символ сейчас - {line.get_last_symbol()}")
    if i == 5:
        line.delete_last_symbol()
        print(f"Вы удалили символ, теперь calculation_line выглядит так - {line.get_info_about_line()}")
    if i == 6:
        break