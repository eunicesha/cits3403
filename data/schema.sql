CREATE TABLE IF NOT EXISTS userdata (username TEXT PRIMARY KEY, email TEXT, password TEXT, score INT);
CREATE TABLE IF NOT EXISTS game (user1 TEXT, user1move TEXT, user2 TEXT, user2move TEXT, winner TEXT, FOREIGN KEY (user1) REFERENCES userdata (username), FOREIGN KEY (user2) REFERENCES userdata (username));
CREATE TABLE IF NOT EXISTS psr (option TEXT PRIMARY KEY, beats TEXT);
INSERT INTO psr VALUES ('paper','rock'), ('scissors','paper'), ('rock','scissors');
