import sqlite3 as sq
import math as m
import matplotlib.pyplot as plt
import numpy as np


class Debit:
    def __init__(self,
                 C: float,
                 P: float,
                 y: float,
                 T: float,
                 Z: float,
                 Q: float) -> None:
        self.C = C
        self.P = P
        self.y = y
        self.T = T
        self.Z = Z
        self.Q = Q
    
    def my_debit(self) -> float:
        my_Q1 = (self.C * self.P)
        my_Q2 = (m.sqrt(self.y * self.T * self.Z))
        my_Q = my_Q1 / my_Q2
        return my_Q
    
    def dq_equal(self) -> float:
        my_Q = self.my_debit()
        Q0 = self.Q
        dQ = abs(Q0 - my_Q)
        return dQ


class Plot_lib:  # Класс для рисования графиков функции
    def __init__(self) -> None:
        pass

with sq.connect('dikt.db') as con1:
    cur = con1.cursor()
    cur.execute("SELECT * FROM well_12102")
    def read_package(data: list) -> Debit:
        if data is None:
            raise TypeError ('Foo bar')
        return data
    dq_equal = []  # Список значений погрешностей
    #cur.execute("ALTER TABLE well_12102 ADD COLUMN IF NOT EXISTS 'dQ' 'float'")  # Создание столбца dQ в таблице well_12102
    for result in cur:
        qd = read_package(result)
        C, P, y, T, Z, Q = qd  # Распаковка кортежа
        well = Debit(C, P, y, T, Z, Q)  #С оздание объекта well класса Debit
        dq_equal.append(well.dq_equal()) # Создание списка погрешностей (ещё нужно отсортировать)
        #cur.execute("INSERT INTO well_12102 VALUSE")  # Добавление в столбец значений dQ
    dq_last = (sorted(dq_equal)[-1]) # Итоговое значение наибольшей погрешности


with sq.connect('filtr_koef.db') as con2:
    