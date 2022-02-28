import math as m
import sqlite3 as sq


class Debit:
    def __init__(self,
                 c: float,
                 p: float,
                 y: float,
                 t: float,
                 z: float,
                 q: float) -> None:
        self.c = c
        self.p = p
        self.y = y
        self.t = t
        self.z = z
        self.q = q

    def my_debit(self) -> float:
        my_q1 = (self.C * self.P)
        my_q2 = (m.sqrt(self.y * self.T * self.Z))
        return my_q1 / my_q2

    def dq_equal(self) -> float:
        my_q = self.my_debit()
        q0 = self.Q
        return abs(q0 - my_q)


class Filtr:  # Класс для обработки входных параметров и расчёта сводной таблицы
    def __init__(self,
                 dp: float,
                 q: float) -> None:
        self.dp = dp
        self.q = q

    def koef_x(self):
        return self.q

    def koef_y(self):
        return self.dp / self.q


class Svodnaya:
    def __init__(self,
                 koef_x: float,
                 koef_y: float) -> None:
        self.koef_x = koef_x
        self.koef_y = koef_y

    def koef_x_2(self):
        return self.koef_x * self.koef_x

    def koef_x_y(self):
        return self.koef_x * self.koef_y


class Grpahics:  # Класс для рисования графиков функции
    def __init__(self) -> None:
        pass


with sq.connect('dikt.db') as con1:
    cur = con1.cursor()
    cur.execute("SELECT * FROM well_12102")

    def read_package(data: list) -> Debit:
        if data is None:
            raise TypeError('Ошибка чтения базы данных')
        return data
    dq_equal = []  # Список значений погрешностей
    #cur.execute("ALTER TABLE well_12102 ADD COLUMN IF NOT EXISTS 'dQ' 'float'")  # Создание столбца dQ в таблице well_12102
    sqlite_insert_query = """INSERT INTO well_12102
                             (dQ) VALUES (?)"""
    for result in cur:
        qd = read_package(result)
        c, p, y, t, z, q = qd  # Распаковка кортежа
        well = Debit(c, p, y, t, z, q)  # С оздание объекта well класса Debit
        dq_equal.append(well.dq_equal())  # Создание списка погрешностей (ещё нужно отсортировать)
    #cur.executemany(sqlite_insert_query, dq_equal)
    #cur.execute("ALTER TABLE well_12102 ADD COLUMN 'de' 'float'")  # Создание столбца максимальной погрешности
    dq_last = (sorted(dq_equal)[-1])  # Итоговое значение наибольшей погрешности
    sqlite_insert_dq = """INSERT INTO WELL_12102
                          (de) VALUES (?)"""
    #cur.executemany(sqlite_insert_dq, dq_last)  # Добавление значений максимальной погрешности в столбец de


with sq.connect('filtr_koef.db') as con2:
    cur = con2.cursor()
    cur.execute('SELECT dP, Q FROM well_10201')

    def read_package(data: list) -> Filtr:
        if data is None:
            raise TypeError('Ошибка чтения базы данных')
        return data
    koef_x = []  # Список для коэффициента х
    koef_y = []  # Список для коэффициента у
    k_x_2 = []  # Список для х^2
    k_x_y = []  # Список для x*y
    spot = tuple()
    for result in cur:
        fq = read_package(result)  # Проверка целостности пакета данных
        dp, q = fq  # Распаковка кортежа
        well_filtr = Filtr(dp, q)
        koef_x.append(well_filtr.koef_x())
        koef_y.append(well_filtr.koef_y())
        kx = well_filtr.koef_x()
        ky = well_filtr.koef_y()
        svod = Svodnaya(kx, ky)
        k_x_2.append(svod.koef_x_2())
        k_x_y.append(svod.koef_x_y())
    sum_x = sum(koef_x)
    sum_y = sum(koef_y)
    sum_x_2 = sum(k_x_2)
    sum_x_y = sum(k_x_y)
    spot = (sum_x_y, sum_x_2, sum_x, sum_y)
    l_svodnaya = list(zip(k_x_y, k_x_2, koef_x, koef_y))
    #cur.execute("INSERT INTO svodnaya_summ VALUES(?, ?, ?, ?)", spot)  # Кортеж суммы в SQL
    #cur.executemany("INSERT INTO svodnaya VALUES(?, ?, ?, ?)", l_svodnaya)  # Распаковка архива кортежа из списков в SQL
