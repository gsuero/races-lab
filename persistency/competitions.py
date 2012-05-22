#!/usr/bin/env python

import datetime
import cx_Oracle

class Competition:

    def __init__(self):
        self.id = None
        self.starts_on = None
        self.location = None
        self.title = None
        self.races_count = None

    def get_id(self):
        return self.id.encode('hex')

class CompetitionsPersistency:

    def __init__(self, oracle):
        self.__oracle = oracle

    def create_competition(self):
        return Competition()

    def insert_competition(self, competition):
        cursor = self.__oracle.cursor()
        fmt = '%Y-%m-%d %H:%M:%S';
        date = datetime.datetime.strptime(competition.starts_on, fmt)
        date = cx_Oracle.Date(date.year, date.month, date.day)
        cursor.execute('insert into lab3_competitions (starts_on, location, title, races_count) values (:starts_on, :location, :title, :races_count)',
		    starts_on = date, location = unicode(competition.location), title = unicode(competition.title), races_count = competition.races_count)
        cursor.close()

    def update_competition(self, competition):
        cursor = self.__oracle.cursor()
        fmt = '%Y-%m-%d %H:%M:%S';
        date = datetime.datetime.strptime(competition.starts_on, fmt)
        date = cx_Oracle.Date(date.year, date.month, date.day)
        cursor.execute('update lab3_competitions set starts_on = :starts_on, location = :location, title = :title, races_count = :races_count where competition_id = :id',
            starts_on = date, location = unicode(competition.location), title = unicode(competition.title), races_count = competition.races_count, id = competition.id.upper())
        cursor.close()

    def get_competition(self, id):
        cursor = self.__oracle.cursor()
        cursor.execute(
            'select competition_id, starts_on, location, title, races_count from lab3_competitions where competition_id = :id',
            id=id.upper())
        return self.__read_competition(cursor.fetchone())

    def get_competitions(self):
        cursor = self.__oracle.cursor()
        cursor.execute('select competition_id, starts_on, location, title, races_count from lab3_competitions')
        owners = [self.__read_competition(row) for row in cursor]
        cursor.close()
        return owners

    def delete_competition(self, id):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_competitions where competition_id = :id', id=id.upper())
        cursor.close()

    def clear(self):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_competitions')
        cursor.close()

    def __read_competition(self, row):
        if row is None:
            return None
        competition = Competition()
        competition.id = row[0]
        competition.starts_on = row[1]
        competition.location = row[2]
        competition.title = row[3]
        competition.races_count = row[4]
        return competition