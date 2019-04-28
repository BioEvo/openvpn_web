PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE "t_admin" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"username"  TEXT NOT NULL,
"password"  TEXT NOT NULL,
"token"  TEXT
);
INSERT INTO "t_admin" VALUES(1,'admin','e10adc3949ba59abbe56e057f20f883e','');

CREATE TABLE "t_user" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"username"  TEXT NOT NULL,
"password"  TEXT NOT NULL,
"active"  INTEGER NOT NULL,
"expire"  TEXT NOT NULL,
"firewall"  TEXT
);

CREATE TABLE "t_logs" (
"id"  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
"username"  TEXT NOT NULL,
"timeunix"  TEXT NOT NULL,
"local"  TEXT NOT NULL,
"remote"  TEXT NOT NULL,
"trusted_ip"  TEXT NOT NULL,
"trusted_port"  TEXT NOT NULL,
"logintime"  TEXT,
"logouttime"  TEXT,
"received"  INTEGER,
"sent"  INTEGER
);

DELETE FROM sqlite_sequence;
INSERT INTO "sqlite_sequence" VALUES('t_admin',1);
INSERT INTO "sqlite_sequence" VALUES('t_user',1);
INSERT INTO "sqlite_sequence" VALUES('t_logs',1);
COMMIT;