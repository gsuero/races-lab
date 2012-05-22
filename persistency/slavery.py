#!/usr/bin/env python

import datetime
import cx_Oracle

FORMAT = '%Y-%m-%d %H:%M:%S'

class HorseJockey:

    def __init__(self):
        self.horse_id = None
        self.horse_nickname = None
        self.jockey_id = None
        self.jockey_fullname = None
        self.from_date = None
        self.due_date = None

class SlaveryPersistency:

    def __init__(self, oracle):
        self.__oracle = oracle

    def create_horse_jockey(self):
        return HorseJockey()

    def insert_horse_jockey(self, horse_jockey):
        cursor = self.__oracle.cursor()

        from_date = datetime.datetime.strptime(horse_jockey.from_date, FORMAT)
        from_date = cx_Oracle.Date(from_date.year, from_date.month, from_date.day)

        due_date = datetime.datetime.strptime(horse_jockey.due_date, FORMAT)
        due_date = cx_Oracle.Date(due_date.year, due_date.month, due_date.day)

        cursor.execute('''
            insert into lab3_horse_jockeys (horse_id, jockey_id, from_date, due_date)
            values (:horse_id, :jockey_id, :from_date, :due_date)''',
            horse_id=horse_jockey.horse_id, 
            jockey_id=horse_jockey.jockey_id,
            from_date=from_date,
            due_date=due_date
        )
        cursor.close()

    def update_horse_jockey(self, horse_jockey):
        cursor = self.__oracle.cursor()

        from_date = datetime.datetime.strptime(horse_jockey.from_date, FORMAT)
        from_date = cx_Oracle.Date(from_date.year, from_date.month, from_date.day)

        due_date = datetime.datetime.strptime(horse_jockey.due_date, FORMAT)
        due_date = cx_Oracle.Date(due_date.year, due_date.month, due_date.day)
        
        cursor.execute('''
            update lab3_horse_jockeys
            set 
                from_date = :from_date,
                due_date = :due_date 
            where horse_id = :horse_id and jockey_id = :jockey_id''',
            horse_id=horse_jockey.horse_id.upper(),
            jockey_id=horse_jockey.jockey_id.upper(), 
            from_date=from_date,
            due_date=due_date)
        cursor.close()

    def get_horse_jockey(self, horse_id, jockey_id):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select hj.horse_id, h.nickname, hj.jockey_id, j.fullname, hj.from_date, hj.due_date 
            from lab3_horse_jockeys hj, lab3_horses h, lab3_jockeys j
            where hj.horse_id = :horse_id and hj.jockey_id = :jockey_id and h.horse_id = hj.horse_id and j.jockey_id = hj.jockey_id''',
            horse_id=horse_id.upper(),
            jockey_id=jockey_id.upper())
        return self.__read_horse_jockey(cursor.fetchone())

    def get_horse_jockeys(self):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select hj.horse_id, h.nickname, hj.jockey_id, j.fullname, hj.from_date, hj.due_date 
            from lab3_horse_jockeys hj, lab3_horses h, lab3_jockeys j
            where h.horse_id = hj.horse_id and j.jockey_id = hj.jockey_id'''
        )
        horse_jockeys = [self.__read_horse_jockey(row) for row in cursor]
        cursor.close()
        return horse_jockeys

    def delete_horse_jockey(self, horse_id, jockey_id):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            delete from lab3_horse_jockeys 
            where horse_id = :horse_id and jockey_id = :jockey_id''', 
            horse_id=horse_id.upper(),
            jockey_id=jockey_id.upper()
        )
        cursor.close()

    def clear(self):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_horse_jockeys')
        cursor.close()

    def __read_horse_jockey(self, row):
        if row is None:
            return None
        horse_jockey = HorseJockey()
        horse_jockey.horse_id = row[0].encode('hex')
        horse_jockey.horse_nickname = row[1]
        horse_jockey.jockey_id = row[2].encode('hex')
        horse_jockey.jockey_fullname = row[3]
        horse_jockey.from_date = row[4]
        horse_jockey.due_date = row[5]
        return horse_jockey