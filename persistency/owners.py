#!/usr/bin/env python

class Owner:

    def __init__(self):
        self.id = None
        self.fullname = None
        self.address = None

    def get_id(self):
        return self.id.encode('hex')

class OwnersPersistency:

    def __init__(self, oracle):
        self.__oracle = oracle

    def create_owner(self):
        return Owner()

    def insert_owner(self, owner):
        cursor = self.__oracle.cursor()
        cursor.execute('insert into lab3_owners (fullname, address) values (:fullname, :address)',
            fullname=unicode(owner.fullname), address=unicode(owner.address))
        cursor.close()

    def update_owner(self, owner):
        cursor = self.__oracle.cursor()
        cursor.execute('update lab3_owners set fullname = :fullname, address = :address where owner_id = :id',
            fullname=unicode(owner.fullname), address=unicode(owner.address), id=owner.id.upper())
        cursor.close()

    def get_owner(self, id):
        cursor = self.__oracle.cursor()
        cursor.execute(
            'select owner_id, fullname, address from lab3_owners where owner_id = :id',
            id=id.upper())
        return self.__read_owner(cursor.fetchone())

    def get_owners(self):
        cursor = self.__oracle.cursor()
        cursor.execute('select owner_id, fullname, address from lab3_owners')
        owners = [self.__read_owner(row) for row in cursor]
        cursor.close()
        return owners

    def delete_owner(self, id):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_owners where owner_id = :id', id=id.upper())
        cursor.close()

    def clear(self):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_owners')
        cursor.close()

    def __read_owner(self, row):
        if row is None:
            return None
        owner = Owner()
        owner.id = row[0]
        owner.fullname = row[1]
        owner.address = row[2]
        return owner