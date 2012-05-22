#!/usr/bin/env python

class Jockey:

    def __init__(self):
        self.id = None
        self.address = None
        self.age = None
        self.weight = None
        self.height = None
        self.fullname = None

class JockeysPersistency:

    def __init__(self, oracle):
        self.__oracle = oracle

    def create_jockey(self):
        return Jockey()

    def insert_jockey(self, jockey):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            insert into lab3_jockeys (address, age, weight, height, fullname)
            values (:address, :age, :weight, :height, :fullname)''',
            address=jockey.address,
            age=jockey.age,
            weight=jockey.weight,
            height=jockey.height,
            fullname=jockey.fullname)
        cursor.close()

    def update_jockey(self, jockey):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            update lab3_jockeys 
            set 
                address = :address, 
                age = :age,
                weight = :weight,
                height = :height,
                fullname = :fullname 
            where jockey_id = :id''',
            address=jockey.address,
            age=jockey.age,
            weight=jockey.weight,
            height=jockey.height,
            fullname=jockey.fullname,
            id=jockey.id.upper())
        cursor.close()

    def get_jockey(self, id):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select jockey_id, address, age, weight, height, fullname
            from lab3_jockeys where jockey_id = :id''',
            id=id.upper())
        return self.__read_jockey(cursor.fetchone())

    def get_jockeys(self):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select jockey_id, address, age, weight, height, fullname
            from lab3_jockeys''')
        jockeys = [self.__read_jockey(row) for row in cursor]
        cursor.close()
        return jockeys

    def get_jockeys_by_horse_nickname(self, nickname):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select j.jockey_id, j.address, j.age, j.weight, j.height, j.fullname
            from lab3_jockeys j, lab3_horses h, lab3_horse_jockeys hj
            where h.nickname = :nickname and hj.jockey_id = j.jockey_id and hj.horse_id = h.horse_id''',
            nickname=nickname)
        jockeys = [self.__read_jockey(row) for row in cursor]
        cursor.close()
        return jockeys

    def delete_jockey(self, id):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_jockeys where jockey_id = :id', id=id.upper())
        cursor.close()

    def clear(self):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_jockeys')
        cursor.close()

    def __read_jockey(self, row):
        if row is None:
            return None
        jockey = Jockey()
        jockey.id = row[0].encode('hex')
        jockey.address = row[1]
        jockey.age = row[2]
        jockey.weight = row[3]
        jockey.height = row[4]
        jockey.fullname = row[5]
        return jockey