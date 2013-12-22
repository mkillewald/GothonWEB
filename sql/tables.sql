CREATE TABLE game_users
(
  id serial NOT NULL,
  username varchar(80) NOT NULL,
  pass char(40) NOT NULL,
  email varchar(100) NOT NULL,
  privilege integer NOT NULL DEFAULT 0,
  CONSTRAINT utilisateur_pkey PRIMARY KEY (id)
);

CREATE TABLE sessions (
    session_id char(128) UNIQUE NOT NULL,
    atime timestamp NOT NULL default current_timestamp,
    data text
);