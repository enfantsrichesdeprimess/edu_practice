class Train:
    def __init__(self,destination,train_num,time_departure):
        self.destination = destination
        self.train_num = train_num
        self.time_departure = time_departure


    def info(self):
        return((f"Пункт назначения поезда: {self.destination}\n"
              f"-Номер поезда: {self.train_num}\n"
              f"-Время отправления: {self.time_departure}\n"
              ))

def get_search_info():
    search_train_num = int(input("Введите номер поезда: "))
    for train in trains:
        if search_train_num == train.train_num:
            print(f"Вот поезд по вашему запросу:\n"
                  f"{train.info()}")
            break
        else:
            print("Ничего не найдено")

trains = [Train("Moscov",1, "10:30"),
          Train("Saint-Petersburg",2,"11:00"),
          Train("Kazan",3,"12:00")]

while True:
    i = int(input(("Выберите что хотите сделать:\n"
      "1 - отобразить информацию о всех поездах\n"
      "2 - найти поезд по номеру\n"
      "3 - выйти\n"
    )))
    if i == 1:
        for train in trains:
            train.info()
    if i == 2:
       get_search_info()
    if i == 3:
        break
