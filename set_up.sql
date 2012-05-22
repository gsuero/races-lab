
-- Dropping all tables.

drop table lab3_horse_results;
drop table lab3_horse_jockeys;
drop table lab3_jockeys;
drop table lab3_competitions;
drop table lab3_horses;
drop table lab3_owners;

-- Creating owners table.

create table lab3_owners (
    owner_id raw(16) default sys_guid() primary key,
    fullname varchar2(40) not null,
    address varchar2(40) not null
);

-- Creating horses table.

create table lab3_horses (
    horse_id raw(16) default sys_guid() primary key,
    nickname varchar2(40) not null,
    sex varchar2(1) not null,
    age number not null check (age > 0),
    owner_id raw(16) not null
        constraint horse_owner_fkey 
        references lab3_owners (owner_id)
        on delete cascade
);

-- Creating competitions table.

create table lab3_competitions (
    competition_id raw(16) default sys_guid() primary key,
    starts_on date not null,
    location varchar2(40) not null,
    title varchar2(40) null,
    races_count integer not null check (races_count > 0)
);

-- Creating jockeys table.

create table lab3_jockeys (
    jockey_id raw(16) default sys_guid() primary key,
    address varchar2(40) not null,
    age number not null check (age > 0),
    weight number not null check (weight > 0),
    height number not null check (height > 0),
    fullname varchar2(40) not null
);

-- Creating horse-jockeys mappings table.

create table lab3_horse_jockeys (
    horse_id raw(16) not null
        constraint horse_jockeys_horse
        references lab3_horses (horse_id)
        on delete cascade,
    jockey_id raw(16) not null
        constraint horse_jockeys_jockey
        references lab3_jockeys (jockey_id)
        on delete cascade,
    from_date date not null,
    due_date date null
);

-- Creating horse results table.

create table lab3_horse_results (
    competition_id raw(16) not null
        constraint horse_results_competition
        references lab3_competitions (competition_id)
        on delete cascade,
    horse_id raw(16) not null
        constraint horse_results_horse
        references lab3_horses (horse_id)
        on delete cascade,
    place integer not null check (place > 0)
);

-- Everything is done.
