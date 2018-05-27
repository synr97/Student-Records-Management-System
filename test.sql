create table test (
  id integer primary key autoincrement,
  title string not null,
  description string not null,
  content string not null,
  date DATE not null ,
  author string not null,
  tags string not null
);