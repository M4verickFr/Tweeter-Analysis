DROP TABLE IF EXISTS tweet;
DROP TABLE IF EXISTS word;
DROP TABLE IF EXISTS city;

CREATE TABLE IF NOT EXISTS city (
  osm_id bigint(100) NOT NULL,
  display_name varchar(255) NOT NULL,
  lat varchar(20) NOT NULL,
  lon varchar(20) NOT NULL,
  PRIMARY KEY (osm_id)
);

CREATE TABLE IF NOT EXISTS tweet (
  id int(10) NOT NULL AUTO_INCREMENT,
  id_tweet varchar(19) NOT NULL,
  created_at varchar(100) NOT NULL,
  full_text varchar(280) NOT NULL,
  lang varchar(10) NOT NULL,
  retweet_count int(10) NOT NULL,
  latitude varchar(20),
  longitude varchar(20),
  id_city bigint(100) NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_city) REFERENCES city(osm_id)
);

CREATE TABLE IF NOT EXISTS word (
  id int(10) NOT NULL AUTO_INCREMENT,
  word varchar(19) NOT NULL,
  id_city bigint(100) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_city) REFERENCES city(osm_id)
);