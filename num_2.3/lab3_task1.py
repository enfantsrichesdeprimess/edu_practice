class Worker:
    def __init__(self, name, surname, rate, days):
        self.name = name
        self.surname = surname
        self.rate = rate
        self.days = days

    def get_salary(self):
        return self.rate * self.days


worker = Worker("Алексей", "Красов", 9500, 300)

print(f"Работник {worker.name} {worker.surname} "
      f"со ставкой {worker.rate} рублей "
      f"проработал {worker.days} дней\n"
      f"И получил ЗП в размере {worker.get_salary()} рублей")