#!/usr/bin/env python

class HorseResult:

    def __init__(self):
        self.competition_id = None
        self.horse_id = None
        self.horse_name = None
        self.competition_title = None
        self.place = None

    def get_competition_id(self):
        return self.competition_id.encode('hex') if self.competition_id is not None else ''

    def get_horse_id(self):
        return self.horse_id.encode('hex') if self.horse_id is not None else ''

class HorseResultsPersistency:

    def __init__(self, oracle):
        self.__oracle = oracle

    def create_horse_result(self):
        return HorseResult()

    def insert_horse_result(self, horse_result):
        try:
            self.delete_horse_result(horse_result.competition_id, horse_result.horse_id)
        except Exception:
            print 'Failed to delete'
        cursor = self.__oracle.cursor()
        cursor.execute('''
            insert into lab3_horse_results (competition_id, horse_id, place)
            values (:competition_id, :horse_id, :place)''',
            competition_id = horse_result.competition_id.upper(),
            horse_id = horse_result.horse_id.upper(),
            place = horse_result.place
        )
        cursor.close()

    def update_horse_result(self, horse_result):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            update lab3_horse_results set
                place = :place
            where competition_id = :competition_id and horse_id = :horse_id''',
            competition_id = horse_result.competition_id.upper(),
            horse_id = horse_result.horse_id.upper(),
            place = horse_result.place
        )
        cursor.close()

    def get_horse_result(self, competition_id, horse_id):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select hr.competition_id, hr.horse_id, h.nickname, c.title, hr.place
            from lab3_horse_results hr, lab3_horses h, lab3_competitions c 
            where hr.competition_id = c.competition_id and hr.horse_id = h.horse_id and
            hr.competition_id = :competition_id and hr.horse_id = :horse_id''',
            competition_id = competition_id.upper(),
            horse_id = horse_id.upper()
        )
        return self.__read_horse_result(cursor.fetchone())

    def get_horse_results(self):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            select hr.competition_id, hr.horse_id, h.nickname, c.title, hr.place
            from lab3_horse_results hr, lab3_horses h, lab3_competitions c 
            where hr.competition_id = c.competition_id and hr.horse_id = h.horse_id 
            '''
        )
        horses = [self.__read_horse_result(row) for row in cursor]
        cursor.close()
        return horses

    def clear(self):
        cursor = self.__oracle.cursor()
        cursor.execute('delete from lab3_horse_results')
        cursor.close()

    def delete_horse_result(self, competition_id, horse_id):
        cursor = self.__oracle.cursor()
        cursor.execute('''
            delete from lab3_horse_results
            where competition_id = :competition_id and horse_id = :horse_id''',
            competition_id = competition_id.upper(), horse_id = horse_id.upper()
        )
        cursor.close()

    def __read_horse_result(self, row):
        if row is None:
            return None
        horse_result = HorseResult()
        horse_result.competition_id = row[0]
        horse_result.horse_id = row[1]
        horse_result.horse_name = row[2]
        horse_result.competition_title = row[3]
        horse_result.place = row[4]
        return horse_result