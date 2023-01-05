# LockerBox
Program for monitoring payments for renting lockers

"""LOGIC OF THE PROGRAM"""


Control over the state of the lockers is carried out by the administrator of the gym

The locker can have the following states:

- Empty
White color

- Busy
Green color
If the lease is not overdue
Red color
If the lease is overdue

- Damaged
Yellow

- spare key
Present
The key is displayed on the icon of the locker
Absent
Key icon not showing

The history of all locker state changes is displayed in the log file and database (history table)

#################################################################################################

"""ЛОГИКА РАБОТЫ ПРОГРАММЫ"""


Контроль за состоянием шкафчиков осуществляет администратор спортивного зала

Шкафчик может иметь следующие состояния:

	- Пуст
	 	Белый цвет
	
	- Занят	
	 	Зеленый цвет
	 		Если аренда не просрочена 
	 	Красный цвет
	 		Если аренда просрочена
	
	- Поврежден
		Желтый цвет
	
	- Запасной ключ
		Присутствует
			Отображается ключик на иконке шкафчика
		Отсутствует
			Иконка ключика не отображается

История всех изменений состояний шкафчиков отображается в файле лога и базе данных (таблица history)
