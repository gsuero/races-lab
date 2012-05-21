
-- Delete all existing data.

delete from lab3_horse_results;
delete from lab3_horse_jockeys;
delete from lab3_jockeys;
delete from lab3_competitions;
delete from lab3_horses;
delete from lab3_owners;

-- Filling up the owners.

insert into lab3_owners (fullname, address) 
    values ('Agent Smith', '12, Red str.');
insert into lab3_owners (fullname, address) 
    values ('Bill Gates', 'Redmond City');
insert into lab3_owners (fullname, address)
    values ('Johny', 'Somewhere');

-- Filling up the horses.

insert into lab3_horses (nickname, sex, age, owner_id)
    values ('Villy', 'F', 10.5, 
        (select owner_id from lab3_owners where fullname = 'Agent Smith'));
insert into lab3_horses (nickname, sex, age, owner_id)
    values ('Felix', 'M', 9, 
        (select owner_id from lab3_owners where fullname = 'Bill Gates'));
insert into lab3_horses (nickname, sex, age, owner_id)
    values ('Bob', 'M', 2, 
        (select owner_id from lab3_owners where fullname = 'Johny'));

-- Filling up the competitions.

insert into lab3_competitions (starts_on, location, title, races_count)
    values (to_date('20120315', 'yyyymmdd'), 'Central Square', 'Trololo', 3);
insert into lab3_competitions (starts_on, location, title, races_count)
    values (to_date('20121221', 'yyyymmdd'), 'Earth', 'Nibiru Racing', 10);

-- Filling up the jockeys.

insert into lab3_jockeys (address, age, weight, height, fullname)
    values ('24, Yellow str.', 25, 65, 180, 'David');
insert into lab3_jockeys (address, age, weight, height, fullname)
    values ('1, Green str.', 23, 70, 173, 'Mathew');

-- Filling up the horse-jockeys mappings.

insert into lab3_horse_jockeys (horse_id, jockey_id, from_date, due_date)
    values (
        (select horse_id from lab3_horses where nickname = 'Villy'),
        (select jockey_id from lab3_jockeys where fullname = 'David'),
        to_date('20100101', 'yyyymmdd'),
        to_date('20110101', 'yyyymmdd')
        );
insert into lab3_horse_jockeys (horse_id, jockey_id, from_date, due_date)
    values (
        (select horse_id from lab3_horses where nickname = 'Villy'),
        (select jockey_id from lab3_jockeys where fullname = 'Mathew'),
        to_date('20110101', 'yyyymmdd'),
        null
        );

-- Filling up the horses results.

insert into lab3_horse_results (competition_id, horse_id, place)
    values (
        (select competition_id from lab3_competitions where title = 'Trololo'),
        (select horse_id from lab3_horses where nickname = 'Villy'),
        1
        );
insert into lab3_horse_results (competition_id, horse_id, place)
    values (
        (select competition_id from lab3_competitions where title = 'Trololo'),
        (select horse_id from lab3_horses where nickname = 'Felix'),
        2
        );

-- Everything is done.
