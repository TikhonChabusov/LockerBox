from Data.DB_Lockers import Locker, Tenant, History, create_lickers
from tkinter import messagebox as mb
from tkcalendar import DateEntry
from tkinter import ttk
from tkinter import *

import tkinter.tix as tkx
import tkinter as tk
import datetime
import sqlite3
import time


# Файл лого для окон
logo = 'Images/boxing.ico'

# Параметры основного окна 
root = Tk()
root.resizable(False, False)
root.title("Шкафчики")
root.iconbitmap(logo)
style = ttk.Style(root)
style.configure("vista")
#root.iconphoto(True, tk.PhotoImage(file='boxing.png'))
root.state('zoomed')


#--------------------------------------------------------------------------------

# Файл для хранения логов операций

logs = 'Logs/The_event_log.txt' 

# Переменные шаблонных png для отображения статуса
photo = PhotoImage(file = r"States/no_key/locker.png")
photo_red = PhotoImage(file = r"States/no_key/locker_red.png")
photo_green = PhotoImage(file = r"States/no_key/locker_green.png")
photo_yellow = PhotoImage(file = r"States/no_key/locker_yellow.png")
photo_key = PhotoImage(file = r"States/key/locker_key.png") 
photo_key_green = PhotoImage(file = r"States/key/locker_key_green.png")
photo_key_red = PhotoImage(file = r"States/key/locker_key_red.png")
photo_key_yellow = PhotoImage(file = r"States/key/locker_key_yellow.png")
#--------------------------------------------------------------------------------


"""БЛОК ИНФОРМАЦИИ О ВЫБРАННОМ ШКАФЧИКЕ"""
#--------------------------------------------------------------------------------
def locker(arg, arg2): # Имя, Название
	newWindow = Toplevel(arg)
	newWindow.geometry('500x300+380+200')
	newWindow.iconbitmap(logo)
	newWindow.title(arg2)
	newWindow.resizable(False, False)
	newWindow.focus_force()
	newWindow.grab_set()

	lock = Locker.get(Locker.name == arg2)
	now = datetime.datetime.today() # Дата в данный момент
	rental = 'foo'
	num = 'foo'
	date_rental = 'foo'
	st = f"Тестовый текст!"

	for tenant in lock.tenants: # Вывод информации об арендаторе
		rental =  tenant.name
		num = tenant.number
		date_rental = tenant.end_date_of_the_lease
		date_time_obj = datetime.datetime.strptime(date_rental, '%d/%m/%Y')
		tp = date_time_obj - now # Время до/после даты последнего продления/изменения
		tp2 = str(tp)
		time_pay = int(tp2.split()[0])

	if lock.status != 'Пуст' and lock.status != 'Поврежден':
		if time_pay <= 0:
			st = f"Просрочен на {abs(time_pay)} суток!"
		else:
			st = f"До конца аренды {time_pay} суток."
	else:
		st = '--------'
		rental = '--------'
		num = '--------'
		date_rental = '--------'

	label_name = Label(newWindow, text = "Именование:")
	label_name.place(x=100, y=37, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	label_name = Label(newWindow, text = arg2)
	label_name.place(x=150, y=37, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	labeljob = Label(newWindow, text = "Статус:")
	labeljob.place(x=100, y=67, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	labeljob = Label(newWindow, text = lock.status)
	labeljob.place(x=150, y=67, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	labelnum = Label(newWindow, text = "Арендатор:")
	labelnum.place(x=100, y=97, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	labelnum = Label(newWindow, text = rental)
	labelnum.place(x=150, y=97, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	labelnum1 = Label(newWindow, text = "Телефон:")
	labelnum1.place(x=100, y=127, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	labelnum1 = Label(newWindow, text = num)
	labelnum1.place(x=150, y=127, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	labelnum2 = Label(newWindow, text = "Срок аренды:")
	labelnum2.place(x=100, y=157, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	labelnum2t = Label(newWindow, text = f'{lock.comment} | {st} |')
	labelnum2t.place(x=150, y=157, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	labelnum3 = Label(newWindow, text = "Аренда до:")
	labelnum3.place(x=100, y=187, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	labelnum3 = Label(newWindow, text = date_rental)
	labelnum3.place(x=150, y=187, anchor="w", height=20, width=200, bordermode=OUTSIDE)

	labelnum4 = Label(newWindow, text = "Оплачено:")
	labelnum4.place(x=100, y=217, anchor="e", height=20, width=95, bordermode=OUTSIDE)
	labelnum4 = Label(newWindow, text = lock.rental_counter)
	labelnum4.place(x=150, y=217, anchor="w", height=20, width=200, bordermode=OUTSIDE)


	# Изменение данных о шкафчике
	def change(arg, arg2): 
		newWindow.destroy()
		change_Window = Toplevel(root)
		change_Window.geometry('500x300+380+200')
		change_Window.iconbitmap(logo)
		change_Window.title(f"Редактировать {arg2}")
		change_Window.resizable(False, False)
		change_Window.focus_force()
		change_Window.grab_set()

		lock = Locker.get(Locker.name == arg2)

		rental =  '--------'
		num = '--------'
		place_com = f"{now.day}/{now.month}/{now.year}"


		# Вывод информации об арендаторе
		for tenant in lock.tenants: 
			rental =  tenant.name
			num = tenant.number
			place_com = tenant.end_date_of_the_lease

		label_name = Label(change_Window, text = "Именование:")
		label_name.place(x=100, y=37, anchor="e", height=20, width=95, bordermode=OUTSIDE)
		label_name = Label(change_Window, text = arg2)
		label_name.place(x=150, y=37, anchor="w", height=20, width=200, bordermode=OUTSIDE)
	
		labelnum = Label(change_Window, text = "Статус:")
		labelnum.place(x=100, y=67, anchor="e", height=20, width=95, bordermode=OUTSIDE)


		status_list = ['Поврежден', 'Просрочен', 'Аренда. OK', 'Пуст']
		Operatorcombo_status = ttk.Combobox(change_Window)
		Operatorcombo_status['values'] = status_list
		place_n = lock.status
		Operatorcombo_status.insert('', place_n)
		Operatorcombo_status.current() 
		Operatorcombo_status.place(x=150, y=67, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
		labelpl = Label(change_Window, text = "Арендатор:")
		labelpl.place(x=100, y=97, anchor="e", height=20, width=95, bordermode=OUTSIDE)
		labelpl1 = Entry(change_Window)
		labelpl1.insert(0, rental)
		labelpl1.place(x=150, y=97, anchor="w", height=20, width=200, bordermode=OUTSIDE)
		
		labeladm = Label(change_Window, text = "Телефон:")
		labeladm.place(x=100, y=127, anchor="e", height=20, width=95, bordermode=OUTSIDE)
		labelpln = Entry(change_Window)
		labelpln.insert(0, num)
		labelpln.place(x=150, y=127, anchor="w", height=20, width=200, bordermode=OUTSIDE)

		labeladm = Label(change_Window, text = "Срок аренды:")
		labeladm.place(x=100, y=157, anchor="e", height=20, width=95, bordermode=OUTSIDE)
		status_list1 = ['Месяц', 'Полгода', 'Год']
		Operatorcombo_place1 = ttk.Combobox(change_Window)
		Operatorcombo_place1['values'] = status_list1
		place_n1 = lock.comment
		Operatorcombo_place1.insert('', place_n1)
		Operatorcombo_place1.current() 
		Operatorcombo_place1.place(x=150, y=157, anchor="w", height=20, width=200, bordermode=OUTSIDE)
	
		labelcom = Label(change_Window, text = "Аренда до:")
		labelcom.place(x=100, y=187, anchor="e", height=20, width=95, bordermode=OUTSIDE)

		calendar = DateEntry(change_Window,locale='ru_RU', date_pattern='dd/MM/yyyy', textvariable=place_com)
		calendar.delete(0, 'end')
		calendar.insert('', place_com)
		calendar.place(x=150, y=187, anchor="w", height=20, width=200, bordermode=OUTSIDE)

		labeladm = Label(change_Window, text = "Запасной ключ:")
		labeladm.place(x=100, y=217, anchor="e", height=20, width=95, bordermode=OUTSIDE)

		status_key = ['Присутствует', 'Отсутствует']
		Operatorcombo_key = ttk.Combobox(change_Window)
		Operatorcombo_key['values'] = status_key

		place_key = lock.spare_key
		if lock.spare_key == 1:
			place_key = "Присутствует"
		else:
			place_key = "Отсутствует"
		Operatorcombo_key.insert('', place_key)
		Operatorcombo_key.place(x=150, y=217, anchor="w", height=20, width=200, bordermode=OUTSIDE)

		labelasum = Label(change_Window, text = "Оплачено:")
		labelasum.place(x=100, y=247, anchor="e", height=20, width=95, bordermode=OUTSIDE)
		labelpsumentry = Entry(change_Window)
		labelpsumentry.insert(0, lock.rental_counter)
		labelpsumentry.place(x=150, y=247, anchor="w", height=20, width=200, bordermode=OUTSIDE)

		
	
		def save_visit():

			lock.status = Operatorcombo_status.get() # Статус

			key = Operatorcombo_key.get()
			if key == 'Присутствует':
				key = 1
			else:
				key = 0
			lock.spare_key = key # Запасной ключ

			lock.comment = Operatorcombo_place1.get() # Комментарий

			summ = labelpsumentry.get() # Оплачено
			lock.rental_counter = summ
			
			# Арендатор
			rental = labelpl1.get()
			num = labelpln.get()
			arenda = calendar.get()

			# save update
			if lock.tenants.count() == 0:
				Tenant.create(name=rental, locker_id = lock.id, number = num, end_date_of_the_lease = arenda)
				History.create(comment = lock.status, locker = lock.id, tenant = rental, number = num, summ = summ, end_date_of_the_lease = arenda, key = key, srock = lock.comment)
				f = open(logs, 'a')
				f.write(f"Дата: {now}. К {lock.name} добавлен арендатор {rental} / номер {num} на срок {lock.comment} до {arenda}. Оплачено {summ}. Запасной ключ {place_key}\n")
				f.close()
			else:	
				tenant.name = rental
				tenant.locker_id = lock.id
				tenant.number = num
				tenant.end_date_of_the_lease = arenda
				tenant.save()
				History.create(comment = lock.status, locker = lock.id, tenant = rental, number = num, summ = summ, end_date_of_the_lease = arenda, key = place_key, srock = lock.comment)
				f = open(logs, 'a')
				f.write(f"Дата: {now}. У {lock.name} изменен арендатор {rental} / номер {num} на срок {lock.comment} до {arenda}. Оплачено {summ}. Запасной ключ {place_key}\n")
				f.close()	
			lock.save()
			stat(arg, arg2)

			try:
				mb.showinfo("Успех!", "Изменения успешно внесены!")
				change_Window.destroy()
			except:
				mb.showerror("Ошибка!", "Ошибка при внесении изменений!")




		btn_save = Button(change_Window, text="Сохранить", 
			width=10, height=1, anchor="n", command = save_visit)
		btn_save.place(relx=0.95, y=280, anchor="e")



	# Хотите освободить шкафчик?
	def delete_locker(): 
		answer = mb.askyesno(
			title="Вопрос", 
			message=f"Освободить {arg2}?")
		if answer:
			#print(f'Освобождаю {arg2}!')
			lock.status = 'Пуст'
			lock.save()
			key = 'foo'
			mb.showinfo("Успех!", "Шкафчик освобожден!")

			# Удаление закрепленного арендатора
			for tenant in lock.tenants: 
				tenant.delete_instance()
				if lock.spare_key == 1:
					key = 'Присутствует' 
					arg.config(image=photo_key)
				else:
					key = 'Отсутствует'
					arg.config(image=photo)
				f = open(logs, 'a')
				f.write(f"Дата: {now}. {lock.name} освобожден! Запасной ключ {key}\n")
				f.close()
				History.create(comment = lock.status, locker = lock.id, tenant = '--------', number = '--------', summ = '--------', end_date_of_the_lease = '--------', key = lock.spare_key, srock = '--------')			
		else:
			#print('Действие отменено!')
			mb.showerror("Ошибка!", "Ошибка освобождения шкафчика!")



	def history(arg, arg2):
		newWindow.destroy()
		history_Window = Toplevel(root)
		history_Window.geometry('880x300+280+200')
		history_Window.title(f"История {arg2}")
		history_Window.iconbitmap(logo)
		history_Window.resizable(False, False)
		history_Window.focus_force()
		history_Window.grab_set()

		lock = Locker.get(Locker.name == arg2)

		tree_history = ttk.Treeview(history_Window, column=(
					"column1", 
					"column2", 
					"column3",
					"column4",
					"column5",
					"column6", 
					),
					show='headings')
		tree_history.heading("#1", text="Дата")
		tree_history.column("#1",minwidth=0,width=68, stretch=NO, anchor=CENTER)
		tree_history.heading("#2", text="Арендатор")
		tree_history.column("#2",minwidth=0,width=200, stretch=NO, anchor=CENTER)
		tree_history.heading("#3", text="Телефон")
		tree_history.column("#3",minwidth=0,width=130, stretch=NO, anchor=CENTER)
		tree_history.heading("#4", text="Зап.ключ")
		tree_history.column("#4",minwidth=0,width=130, stretch=NO, anchor=CENTER)
		tree_history.heading("#5", text="Срок аренды")
		tree_history.column("#5",minwidth=0,width=213, stretch=NO, anchor=CENTER)
		tree_history.heading("#6", text="Оплачено")
		tree_history.column("#6",minwidth=0,width=130, stretch=NO, anchor=CENTER)
		tree_history.pack(expand=1, anchor=NW, fill="both")

		record = History.select().where(History.locker_id == lock.id)	
		for recording in record:
			if recording.key == 1:
				recording.key = "Присутствует"
			else:
				recording.key = "Отсутствует"	
			tree_history.insert('', tk.END, values=[recording.created_at, recording.tenant_id, recording.number,
													recording.key, recording.srock, recording.summ])
		
		
		# Скролбар история
		scroll = Scrollbar(tree_history)
		scroll.pack(side = 'right', fill = 'y')
		scroll['command'] =tree_history.yview
		tree_history['yscrollcommand'] = scroll.set	
							

	# Кнопки окна истории шкафчика
	btn_history = Button(newWindow, text="История", 
			        	width=10, height=1, anchor="n", command = lambda: history(arg,arg2))
	btn_history.place(relx=0.60, y=280, anchor="e")

	btn_change = Button(newWindow, text="Изменить", 
			        	width=10, height=1, anchor="n", command = lambda: change(arg,arg2))
	btn_change.place(relx=0.78, y=280, anchor="e")

	btn_change = Button(newWindow, text="Освободить", 
			        	width=10, height=1, anchor="n", command = delete_locker)
	btn_change.place(relx=0.96, y=280, anchor="e")		




"""БЛОК СТАТУСА"""
# Вывод и обновление статуса шкафчиков
def stat(arg, arg2): # arg-переменная-имя arg2-Название шкафчика

	lock = Locker.get(Locker.name == arg2)
	now = datetime.datetime.now() # Дата в данный момент
	if lock.status == 'Поврежден': # Выявление поврежденных шкафчиков
		if lock.spare_key == 1 and lock.status == 'Поврежден': # Проблемный с ключом
			arg.config(image=photo_key_yellow)
		elif lock.spare_key == 0 and lock.status == 'Поврежден': # Проблемный без ключа
			arg.config(image=photo_yellow)
	else:
		if lock.tenants.count() == 0: # Если за шкафчиком не закреплен арендатор
			lock.status = 'Пуст'
			lock.save()
			#print(f"{arg2} пуст!")
			if lock.spare_key == 1: # Пустой с ключом
				arg.config(image=photo_key)
			elif lock.spare_key == 0: # Пустой без ключа
				arg.config(image=photo)
		else:
			for tenant in lock.tenants:
				date_rental = tenant.end_date_of_the_lease
				date_time_obj = datetime.datetime.strptime(date_rental, '%d/%m/%Y')
				tp = date_time_obj - now # Время до/после даты последнего продления/изменения
				tp2 = str(tp)
				tp3 = tp2.partition('.')[0][0]
				try:
					time_pay = int(tp2.split()[0]) #(tp2.split()[0])
				except:
					time_pay = 0

				
		
			if time_pay == 0:
				#print(f"{arg2} сегодня последний день!")
				if lock.spare_key == 1: # Просрочен с ключом
					arg.config(image=photo_key_red)
				else: 
					lock.spare_key == 0 # Просрочен без ключа
					arg.config(image=photo_red)
			elif time_pay < 0:
				#print(f"{arg2} просрочен на {abs(time_pay)} дней!")
				if lock.spare_key == 1: # Просрочен с ключом
					arg.config(image=photo_key_red)
				else: 
					lock.spare_key == 0 # Просрочен без ключа
					arg.config(image=photo_red)
			else:
				#print(f"{arg2} до конца аренды {time_pay} дней.")
				if lock.spare_key == 1: # Ок с ключом
					arg.config(image=photo_key_green)
				elif lock.spare_key == 0: # Ок без ключа
					arg.config(image=photo_green)




"""БЛОК ОТРИСОВКИ ШКАФЧИКОВ"""
#--------------------------------------------------------------------------------
def rendering_lockers(parent):

	block_TOP = Frame(parent)
	block_TOP.pack(expand=1, side=TOP)

	# Блоки шкафчиков
	lockers_1 = Frame(block_TOP, padx="10")
	lockers_1.pack(side=LEFT)
	row_1 = Frame(lockers_1)
	row_1.pack()
	row_2 = Frame(lockers_1)
	row_2.pack()
	row_3 = Frame(lockers_1)
	row_3.pack()
	row_4 = Frame(lockers_1)
	row_4.pack()


	btn = Button(row_1, image=photo_key_red, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn, 'Шкафчик №1'))
	btn.pack(side=LEFT) 
	
	btn2 = Button(row_1, background="#555", image=photo_key_yellow, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn2, 'Шкафчик №2'))
	btn2.pack(side=LEFT)
	
	btn3 = Button(row_1, text="Click Me", background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn3, 'Шкафчик №3'))
	btn3.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn4 = Button(row_2, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn4, 'Шкафчик №4'))
	btn4.pack(side=LEFT)
	
	btn5 = Button(row_2, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn5, 'Шкафчик №5'))
	btn5.pack(side=LEFT)
	
	btn6 = Button(row_2, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn6, 'Шкафчик №6'))
	btn6.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn7 = Button(row_3, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn7, 'Шкафчик №7'))
	btn7.pack(side=LEFT)
	
	btn8 = Button(row_3, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn8, 'Шкафчик №8'))
	btn8.pack(side=LEFT)
	
	btn9 = Button(row_3, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn9, 'Шкафчик №9'))
	btn9.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn10 = Button(row_4, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn10, 'Шкафчик №10'))
	btn10.pack(side=LEFT)
	
	btn11 = Button(row_4, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn11, 'Шкафчик №11'))
	btn11.pack(side=LEFT)
	
	btn12 = Button(row_4, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn12, 'Шкафчик №12'))
	btn12.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	#--------------------------------------------------------------------------------
	
	lockers_2 = Frame(block_TOP, padx="5")
	lockers_2.pack(side=LEFT)
	
	row_1_1 = Frame(lockers_2)
	row_1_1.pack()
	row_2_1 = Frame(lockers_2)
	row_2_1.pack()
	row_3_1 = Frame(lockers_2)
	row_3_1.pack()
	row_4_1 = Frame(lockers_2)
	row_4_1.pack()
	
	#--------------------------------------------------------------------------------
	
	btn13 = Button(row_1_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn13, 'Шкафчик №13'))
	btn13.pack(side=LEFT)
	
	btn14 = Button(row_1_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn14, 'Шкафчик №14'))
	btn14.pack(side=LEFT)
	
	btn15 = Button(row_1_1, text="Click Me", background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn15, 'Шкафчик №15'))
	btn15.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn16 = Button(row_2_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn16, 'Шкафчик №16'))
	btn16.pack(side=LEFT)
	
	btn17 = Button(row_2_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn17, 'Шкафчик №17'))
	btn17.pack(side=LEFT)
	
	btn18 = Button(row_2_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn18, 'Шкафчик №18'))
	btn18.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn19 = Button(row_3_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn19, 'Шкафчик №19'))
	btn19.pack(side=LEFT)
	
	btn20 = Button(row_3_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn20, 'Шкафчик №20'))
	btn20.pack(side=LEFT)
	
	btn21 = Button(row_3_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn21, 'Шкафчик №21'))
	btn21.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn22 = Button(row_4_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn22, 'Шкафчик №22'))
	btn22.pack(side=LEFT)
	
	btn23 = Button(row_4_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn23, 'Шкафчик №23'))
	btn23.pack(side=LEFT)
	
	btn24 = Button(row_4_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn24, 'Шкафчик №24'))
	btn24.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	#--------------------------------------------------------------------------------
	
	lockers_3 = Frame(block_TOP)
	lockers_3.pack(side=LEFT)
	
	row_1_1 = Frame(lockers_3)
	row_1_1.pack()
	row_2_1 = Frame(lockers_3)
	row_2_1.pack()
	row_3_1 = Frame(lockers_3)
	row_3_1.pack()
	row_4_1 = Frame(lockers_3)
	row_4_1.pack()
	
	#--------------------------------------------------------------------------------
	
	btn25 = Button(row_1_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn25, 'Шкафчик №25'))
	btn25.pack(side=LEFT)
	
	btn26 = Button(row_1_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn26, 'Шкафчик №26'))
	btn26.pack(side=LEFT)
	
	btn27 = Button(row_1_1, text="Click Me", background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn27, 'Шкафчик №27'))
	btn27.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn28 = Button(row_2_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn28, 'Шкафчик №28'))
	btn28.pack(side=LEFT)
	
	btn29 = Button(row_2_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn29, 'Шкафчик №29'))
	btn29.pack(side=LEFT)
	
	btn30 = Button(row_2_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn30, 'Шкафчик №30'))
	btn30.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn31 = Button(row_3_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn31, 'Шкафчик №31'))
	btn31.pack(side=LEFT)
	
	btn32 = Button(row_3_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn32, 'Шкафчик №32'))
	btn32.pack(side=LEFT)
	
	btn33 = Button(row_3_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn33, 'Шкафчик №33'))
	btn33.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn34 = Button(row_4_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn34, 'Шкафчик №34'))
	btn34.pack(side=LEFT)
	
	btn35 = Button(row_4_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn35, 'Шкафчик №35'))
	btn35.pack(side=LEFT)
	
	btn36 = Button(row_4_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn36, 'Шкафчик №36'))
	btn36.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	#--------------------------------------------------------------------------------
	
	lockers_4 = Frame(block_TOP, padx="10")
	lockers_4.pack(side=LEFT)
	
	row_1_1 = Frame(lockers_4)
	row_1_1.pack()
	row_2_1 = Frame(lockers_4)
	row_2_1.pack()
	row_3_1 = Frame(lockers_4)
	row_3_1.pack()
	row_4_1 = Frame(lockers_4)
	row_4_1.pack()
	
	#--------------------------------------------------------------------------------
	
	btn37 = Button(row_1_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn37, 'Шкафчик №37'))
	btn37.pack(side=LEFT)
	
	btn38 = Button(row_1_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn38, 'Шкафчик №38'))
	btn38.pack(side=LEFT)
	
	btn39 = Button(row_1_1, text="Click Me", background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn39, 'Шкафчик №39'))
	btn39.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn40 = Button(row_2_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn40, 'Шкафчик №40'))
	btn40.pack(side=LEFT)
	
	btn41 = Button(row_2_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn41, 'Шкафчик №41'))
	btn41.pack(side=LEFT)
	
	btn42 = Button(row_2_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn42, 'Шкафчик №42'))
	btn42.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn43 = Button(row_3_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn43, 'Шкафчик №43'))
	btn43.pack(side=LEFT)
	
	btn44 = Button(row_3_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn44, 'Шкафчик №44'))
	btn44.pack(side=LEFT)
	
	btn45 = Button(row_3_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn45, 'Шкафчик №45'))
	btn45.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn46 = Button(row_4_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn46, 'Шкафчик №46'))
	btn46.pack(side=LEFT)
	
	btn47 = Button(row_4_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn47, 'Шкафчик №47'))
	btn47.pack(side=LEFT)
	
	btn48 = Button(row_4_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn48, 'Шкафчик №48'))
	btn48.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	#--------------------------------------------------------------------------------
	
	lockers_5 = Frame(block_TOP, padx="15")
	lockers_5.pack(side=LEFT)
	
	row_1_1 = Frame(lockers_5)
	row_1_1.pack()
	row_2_1 = Frame(lockers_5)
	row_2_1.pack()
	row_3_1 = Frame(lockers_5)
	row_3_1.pack()
	row_4_1 = Frame(lockers_5)
	row_4_1.pack()
	
	#--------------------------------------------------------------------------------
	
	btn49 = Button(row_1_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn49, 'Шкафчик №49'))
	btn49.pack(side=LEFT)
	
	btn50 = Button(row_1_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn50, 'Шкафчик №50'))
	btn50.pack(side=LEFT)
	
	btn51 = Button(row_1_1, text="Click Me", background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn51, 'Шкафчик №51'))
	btn51.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn52 = Button(row_2_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn52, 'Шкафчик №52'))
	btn52.pack(side=LEFT)
	
	btn53 = Button(row_2_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn53, 'Шкафчик №53'))
	btn53.pack(side=LEFT)
	
	btn54 = Button(row_2_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn54, 'Шкафчик №54'))
	btn54.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn55 = Button(row_3_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn55, 'Шкафчик №55'))
	btn55.pack(side=LEFT)
	
	btn56 = Button(row_3_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn56, 'Шкафчик №56'))
	btn56.pack(side=LEFT)
	
	btn57 = Button(row_3_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn57, 'Шкафчик №57'))
	btn57.pack(side=LEFT)
	
	#--------------------------------------------------------------------------------
	
	btn58 = Button(row_4_1, image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn58, 'Шкафчик №58'))
	btn58.pack(side=LEFT)
	
	btn59 = Button(row_4_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn59, 'Шкафчик №59'))
	btn59.pack(side=LEFT)
	
	btn60 = Button(row_4_1, background="#555", image=photo, foreground="#ccc",
	             padx="20", pady="8", font="16", command=lambda:locker(btn60, 'Шкафчик №60'))
	btn60.pack(side=LEFT)

	def status_check():
		""" БЛОК ОТРИСОВКИ АКТУАЛЬНОГО СОСТОЯНИЯ ОБЪЕКТА """
		
		btns = {btn :  'Шкафчик №1',  btn2: 'Шкафчик №2',   btn3: 'Шкафчик №3',   btn4: 'Шкафчик №4',
				btn5:  'Шкафчик №5',  btn6: 'Шкафчик №6',   btn7: 'Шкафчик №7',   btn8: 'Шкафчик №8',
				btn9:  'Шкафчик №9',  btn10: 'Шкафчик №10', btn11: 'Шкафчик №11', btn12: 'Шкафчик №12',
				btn13: 'Шкафчик №13', btn14: 'Шкафчик №14', btn15: 'Шкафчик №15', btn16: 'Шкафчик №16',
				btn17: 'Шкафчик №17', btn18: 'Шкафчик №18', btn19: 'Шкафчик №19', btn20: 'Шкафчик №20',
				btn21: 'Шкафчик №21', btn22: 'Шкафчик №22', btn23: 'Шкафчик №23', btn24: 'Шкафчик №24',
				btn25: 'Шкафчик №25', btn26: 'Шкафчик №26', btn27: 'Шкафчик №27', btn28: 'Шкафчик №28',
				btn29: 'Шкафчик №29', btn30: 'Шкафчик №30', btn31: 'Шкафчик №31', btn32: 'Шкафчик №32',
				btn33: 'Шкафчик №33', btn34: 'Шкафчик №34', btn35: 'Шкафчик №35', btn36: 'Шкафчик №36',
				btn37: 'Шкафчик №37', btn38: 'Шкафчик №38', btn39: 'Шкафчик №39', btn40: 'Шкафчик №40',
				btn41: 'Шкафчик №41', btn42: 'Шкафчик №42', btn43: 'Шкафчик №43', btn44: 'Шкафчик №44',
				btn45: 'Шкафчик №45', btn46: 'Шкафчик №46', btn47: 'Шкафчик №47', btn48: 'Шкафчик №48',
				btn49: 'Шкафчик №49', btn50: 'Шкафчик №50', btn51: 'Шкафчик №51', btn52: 'Шкафчик №52',
				btn53: 'Шкафчик №53', btn54: 'Шкафчик №54', btn55: 'Шкафчик №55', btn56: 'Шкафчик №56',
				btn57: 'Шкафчик №57', btn58: 'Шкафчик №58', btn59: 'Шкафчик №59', btn60: 'Шкафчик №60'}
		
		for i in btns: # Передача списка шкафчиков в функцию статуса
			name = btns.get(i)
			stat(i, name)


	status_check()
	#--------------------------------------------------------------------------------
rendering_lockers(root)



"""БЛОК ДОПОЛНИТЕЛЬНОЙ ИНФОРМАЦИИ"""
#--------------------------------------------------------------------------------

def mainInfoBlock(parent):
	block_BOTTOM = Frame(parent)
	block_BOTTOM.pack(side=TOP, pady=10)

	def tabs(parent):
		# Родитель вкладок
		tab_control = ttk.Notebook(block_BOTTOM)  
		tab1 = ttk.Frame(tab_control) # 
		tab2 = ttk.Frame(tab_control) # 
		tab3 = ttk.Frame(tab_control) # 
		tab4 = ttk.Frame(tab_control) # 
		tab5 = ttk.Frame(tab_control) # 
		tab6 = ttk.Frame(tab_control) # 
		tab7 = ttk.Frame(tab_control) # 
		tab8 = ttk.Frame(tab_control) # 
		tab9 = ttk.Frame(tab_control) # 
		#ВАЖНО! Пакует все вкладки на странице
		tab_control.pack(expand=1, fill=BOTH, side=TOP)

		def update():
			tab_control.destroy()
			return(tabs(parent))

		#Вкладки
		#---------------------------------------------------------------
		
		tab1 = ttk.Frame(tab_control, width=1340, height=600)
		tab_control.add(tab1, text='Общая информация')

		lock_free = Locker.select().where(Locker.status == 'Пуст')
		free_lock = len(lock_free)

		free_lockers = Label(tab1, text=f'Свободны: {free_lock}', font="12")
		free_lockers.pack(anchor=W, pady="5")

		lock_busy = Locker.select().where(Locker.status == 'Просрочен')
		busy_lock = len(lock_busy)

		busy_lockers = Label(tab1, text=f'Просрочены: {busy_lock}', font="12")
		busy_lockers.pack(anchor=W, pady="5")

		lock_faulty = Locker.select().where(Locker.status == 'Поврежден')
		faulty_lock = len(lock_faulty)

		faulty_lockers = Label(tab1, text=f'Повреждены: {faulty_lock}', font="12")
		faulty_lockers.pack(anchor=W, pady="5")

		lock_noKey = Locker.select().where(Locker.spare_key == False)
		noKey_lock = len(lock_noKey)

		noKey_lockers = Label(tab1, text=f'Без запасного ключа: {noKey_lock}', font="12")
		noKey_lockers.pack(anchor=W, pady="5")


		Update_btn = Button(tab1, text='Обновить', font="12", command = update)
		Update_btn.pack(anchor=W, pady="5")
	
		#---------------------------------------------------------------

		tab2 = ttk.Frame(tab_control, width=1340, height=600)
		tab_control.add(tab2, text='Просрочены')

		tree21 = ttk.Treeview(tab2, column=(
					"column1",
					"column2",
					"column3",
					"column4",
					"column5",
					"column6",  
							), 
					show='headings')
		tree21.heading("#1", text="№")
		tree21.column("#1", minwidth=0, width=50, stretch=NO, anchor=CENTER)

		tree21.heading("#2", text="Арендатор")
		tree21.column("#2", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree21.heading("#3", text="Телефон")
		tree21.column("#3", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree21.heading("#4", text="До")
		tree21.column("#4", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree21.heading("#5", text="Комментарий")
		tree21.column("#5", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree21.heading("#6", text="Оплачено")
		tree21.column("#6", minwidth=0, width=252, stretch=NO, anchor=CENTER)
		tree21.pack()
		
		prosrochen = Locker.select().where(Locker.status == 'Просрочен')
		for i in prosrochen:
			ten = Tenant.get(Tenant.locker_id == i.id)
			tree21.insert('', tk.END, values= (i.id, ten.name, ten.number, ten.end_date_of_the_lease, i.comment, i.rental_counter))
			tree21.pack()
			tree21.config(height=600)

		#---------------------------------------------------------------

		tab3 = ttk.Frame(tab_control)
		tab_control.add(tab3, text='Список арендаторов')

		tree_arendator = ttk.Treeview(tab3, column=(
					"column1",
					"column2",
					"column3",
					"column4",
					"column5",
					"column6",  
							), 
					show='headings')
		tree_arendator.heading("#1", text="№")
		tree_arendator.column("#1", minwidth=0, width=50, stretch=NO, anchor=CENTER)

		tree_arendator.heading("#2", text="Арендатор")
		tree_arendator.column("#2", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree_arendator.heading("#3", text="Телефон")
		tree_arendator.column("#3", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree_arendator.heading("#4", text="До")
		tree_arendator.column("#4", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree_arendator.heading("#5", text="Комментарий")
		tree_arendator.column("#5", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree_arendator.heading("#6", text="Оплачено")
		tree_arendator.column("#6", minwidth=0, width=252, stretch=NO, anchor=CENTER)
		tree21.pack()
		
		arendator = Locker.select()
		for i in arendator:
			tt = Tenant.select().where(Tenant.locker_id == i.id)
			for t in tt:
				tree_arendator.insert('', tk.END, values= (i.id, t.name, t.number, t.end_date_of_the_lease, i.comment, i.rental_counter))
				tree_arendator.pack()
				tree_arendator.config(height=600)
			


		#---------------------------------------------------------------

		tab4 = ttk.Frame(tab_control)
		tab_control.add(tab4, text='Без запасного ключа')

		tree_noKey = ttk.Treeview(tab4, column=(
					"column1",
					"column2",
					"column3",
					"column4",
					"column5",
					"column6",  
							), 
					show='headings')
		tree_noKey.heading("#1", text="№")
		tree_noKey.column("#1", minwidth=0, width=50, stretch=NO, anchor=CENTER)

		tree_noKey.heading("#2", text="Арендатор")
		tree_noKey.column("#2", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree_noKey.heading("#3", text="Телефон")
		tree_noKey.column("#3", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree_noKey.heading("#4", text="До")
		tree_noKey.column("#4", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree_noKey.heading("#5", text="Комментарий")
		tree_noKey.column("#5", minwidth=0, width=258, stretch=NO, anchor=CENTER)

		tree_noKey.heading("#6", text="Оплачено")
		tree_noKey.column("#6", minwidth=0, width=252, stretch=NO, anchor=CENTER)
		tree_noKey.pack()
		
		noKey = Locker.select().where(Locker.spare_key == False)
		for i in noKey:
			tt = Tenant.select().where(Tenant.locker_id == i.id)
			t1, t2, t3 = "--------", "--------", "--------"

			for t in tt:
				t1, t2, t3 = t.name, t.number, t.end_date_of_the_lease

			print(i.id, t.name, t.number, t.end_date_of_the_lease, i.comment, i.rental_counter)	
			tree_noKey.insert('', tk.END, values= (i.id, t.name, t.number, t.end_date_of_the_lease, i.comment, i.rental_counter))
			tree_noKey.config(height=600)	
		#---------------------------------------------------------------


	tabs(block_BOTTOM)








mainInfoBlock(root)

root.mainloop()