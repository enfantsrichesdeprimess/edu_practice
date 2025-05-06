class Worker:
    def __init__(self, name, surname, rate, days):
        self.__name = name
        self.__surname = surname
        self.__rate = rate
        self.__days = days

    def get_salary(self):
        return self.__rate * self.__days

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname

    def get_rate(self):
        return self.__rate

    def get_days(self):
        return self.__days

worker = Worker("Алексей", "Красов", 9500, 300)

print(
    f"Работник {worker.get_name()} {worker.get_surname()} со ставкой "
    f"{worker.get_rate()} рублей проработал {worker.get_days()} дней\n"
     f"И получил ЗП в размере {worker.get_salary()} рублей")