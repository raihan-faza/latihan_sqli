drop table if exists user;
drop table if exists post;
drop table if exists admins;

create table user(
  id integer primary key autoincrement,
  username text unique not null,
  password text not null
);
create table post(
  id integer primary key autoincrement,
  author_id integer not null,
  created_at timestamps not null default current_timestamp,
  title text not null,
  body text not null,
  foreign key (author_id) references user (id)
);
create table admins(
  id integer primary key autoincrement,
  username text unique not null,
  password text not null
)