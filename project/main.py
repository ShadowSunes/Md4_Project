import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):   # Класс главного окна
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self): # Хранение и инициализация графических объектов(кнопки таблицы заголовки)
        toolbar = tk.Frame(bg='#d7d8e0', bd=2) # bg - color, bd  В панели toolbar находятся все наши виджеты
        toolbar.pack(side=tk.TOP, fill=tk.X) # TOP- под верхней границей X-растягивает от левой до правой границе

        self.add_img = tk.PhotoImage(file='C:/Users/ShadowSun/Desktop/project/img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog) #Кнопка на добавление
        btn_open_dialog.pack(side=tk.LEFT)
    
        self.tree = ttk.Treeview(self, columns=('ID', 'name','tel','email','salary'), height=45, show='headings') #Табличка все записи из бд
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=250, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=200, anchor=tk.CENTER)
        self.tree.column('salary', width=150, anchor=tk.CENTER)


        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Номер телефона')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary',  text='Зарплата')

        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='C:/Users/ShadowSun/Desktop/project/img/update.png') # добавляем кнопу на редактирование
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='C:/Users/ShadowSun/Desktop/project/img/delete.png')# Добавляем кнопу на удаление
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_record)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='C:/Users/ShadowSun/Desktop/project/img/search.png') #Добавляем кнопку на поиск
        btn_search = tk.Button(toolbar, bg='#d7d8e0', bd=0, image = self.search_img, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='C:/Users/ShadowSun/Desktop/project/img/refresh.png') #добавляем кнопу на возвращение в исходное состояния после поиска
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, image = self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

    def open_dialog(self): # Открытие дочернего окна Child прии нажатии на кнопу btn_open_dialog
        Child()

    def open_update_dialog(self): # Открытие дочернего окна Update при нажатии на кнопу btn_update_dialog
        Update()

    def records(self, name, tel, email, salary): # Отвечает за добавление записей в таблицу бд
        self.db.insert_data(name, tel, email, salary)
        self.view_records()

    def view_records(self): # Необходим для ототбражения в таблице записей в бд и выбираем все записи из таблицы
        self.db.cur.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()] #Очищаем таблицу
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]# добавляем запиис в таблицу

    def update_record(self, name, tel,email, salary):
        self.db.cur.execute('UPDATE db SET name=?,tel=?, email=?, salary=? WHERE id=?', (name,tel, email, salary, self.tree.set(self.tree.selection() [0], '#1'))) #Показывает обновленные записи в таблице
        self.db.conn.commit()
        self.view_records()

    def delete_record(self): # Удаление по id
        for select_item in self.tree.selection():
            self.db.cur.execute('DELETE FROM db WHERE id=?', self.tree.set(select_item, '#1'))

        self.db.conn.commit()
        self.view_records()

    def open_search_dialog(self): # Открытие дочернего окна Search прии нажатии на кнопу open_search_dialog
        Search()

    def search_records(self, name): # Отображение контактов по имени
        #name=('%' + name + '%',)
        name=(name,)
        #name=name
        self.db.cur.execute('SELECT * FROM db WHERE name=?', (name))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]




class Child(tk.Toplevel): # класс необходим для добавления новых сторудников
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self): #Необходим для инициализации и хранения графического интерфейса
        self.title('Добавить сотрудника')
        self.geometry('500x300')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:') #Форма на добавление нового контакта
        label_name.place(x=50, y=50)
        label_tel = tk.Label(self, text='Номер телефона:')
        label_tel.place(x=50, y=80)
        label_select = tk.Label(self, text='E-mail:')
        label_select.place(x=50, y=110)
        label_sum = tk.Label(self, text='Зарплата:')
        label_sum.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=80)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.btn_cansel = ttk.Button(self, text='Закрыть', command=self.destroy) # Кнопка закрытия окна
        self.btn_cansel.place(x=300, y=200)

        self.btn_ok = ttk.Button(self, text='Добавить') # Кноака добавления в бд
        self.btn_ok.place(x=220, y=200)
        self.btn_ok.bind('<Button-1>', lambda event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_tel.get(),  
                                           self.entry_email.get(),
                                           self.entry_salary.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')

class Update(Child): # класс необходим для редактирования данных о сотрудниках
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать данные о сотруднике') #Заголовок дочернего окна
        btn_edit = ttk.Button(self, text='Редактировать') # кнопка "редактировать"
        btn_edit.place(x=180, y=200)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_record(self.entry_name.get(),
                                              self.entry_tel.get(), 
                                              self.entry_email.get(),
                                              self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda ebent: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self): #Отображение уже заполненных полей в дочерем окне, которые можно редактировать
        self.db.cur.execute('SELECT * FROM db WHERE ID=?', (self.view.tree.set(self.view.tree.selection() [0], '#1')))
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tk.Toplevel): # класс необходим для поиска сотрудников
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск сотрудника') #Заголовок дочернего окна
        self.geometry('300x100')
        self.resizable(False, False) # не изменяемость(по длине ширине) дочернего окна

        label_search = tk.Label(self, text='ФИО:') # Название 
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)# Поле для ввода
        self.entry_search.place(x=105, y=20, width=150)

        btn_cansel = ttk.Button(self, text='Закрыть', command=self.destroy) #Кнопка "закрыть"
        btn_cansel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск') # кнопка поиска контактов по ФИО
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB: # Создаём подключение к бд, отправляем запрос на создание таблицы, прописываем метод на добавление новых контактов в бд
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS db (
            id INTEGER PRIMARY KEY,
            name TEXT,
            tel TEXT,
            email TEXT,
            salary TEXT
        );''')
        self.conn.commit()

    def insert_data(self, name, tel, email, salary):
        self.cur.execute('INSERT OR IGNORE INTO db(name, tel, email, salary) VALUES (?, ?, ?, ?);', (name, tel, email, salary))
        self.conn.commit()



if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    #root.geometry('665x450')
    root.geometry('900x600')
    root.resizable(False, False)
    root.mainloop()