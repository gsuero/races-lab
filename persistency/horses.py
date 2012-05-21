#!/usr/bin/env python

class Horse:

    def __init__(self):
        self.id = None
        self.nickname = None
        self.sex = None
        self.age = None
        self.owner_id = None
        self.owner_fullname = None

    def get_id(self):
        return self.id.encode('hex')

    def get_owner_id(self):
        return self.owner_id.encode('hex') if self.owner_id is not None else ''

class HorsesPersistency:

    def __init__(self, oracle):
        self.__oracle = oracle

    def create_horse(self):
        return Horse()

    def insert_horse(self, horse):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            insert into lab3_horses (nickname, sex, age, owner_id)
            values (:nickname, :sex, :age, :owner_id)''',
            nickname=horse.nickname,
            sex=horse.sex,
            age=horse.age,
            owner_id=horse.owner_id.upper()
        )
        cursor.close()

    def update_horse(self, horse):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            update lab3_horses set
                nickname = :nickname, 
                sex = :sex, 
                age = :age, 
                owner_id = :owner_id
            where horse_id = :id''',
            id=horse.id.upper(),
            nickname=horse.nickname,
            sex=horse.sex,
            age=horse.age,
            owner_id=horse.owner_id.upper()
        )
        cursor.close()

    def get_horse(self, id):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select h.horse_id, h.nickname, h.sex, h.age, h.owner_id, o.fullname 
            from lab3_horses h, lab3_owners o 
            where o.owner_id = h.owner_id and h.horse_id = :id''',
            id=id.upper())
        return self.__read_horse(cursor.fetchone())

    def get_horses(self):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select h.horse_id, h.nickname, h.sex, h.age, h.owner_id, o.fullname 
            from lab3_horses h, lab3_owners o 
            where o.owner_id = h.owner_id 
            order by h.nickname'''
        )
        horses = [self.__read_horse(row) for row in cursor]
        cursor.close()
        return horses

    def clear(self):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_horses')
        cursor.close()

    def delete_horse(self, id):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            delete from lab3_horses
            where horse_id = :id''',
            id=id.upper()
        )
        cursor.close()

    def __read_horse(self, row):
        if row is None:
            return None
        horse = Horse()
        horse.id = row[0]
        horse.nickname = row[1]
        horse.sex = row[2]
        horse.age = int(row[3])
        horse.owner_id = row[4]
        horse.owner_fullname = row[5]
        return horse