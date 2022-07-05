-- Create users (userid, username, current_pp, topplay, average_pp)
CREATE TABLE users (
userid INTEGER PRIMARY KEY,
username TEXT,
current_pp INTEGER,
topplay INTEGER,
average_pp INTEGER
);

-- Create beatmaps (beatmapid, beatmap_setid, difficulty_name, stars, length, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100)
CREATE TABLE beatmaps (
beatmapid INTEGER PRIMARY KEY,
beatmap_setid INTEGER,
difficulty_name TEXT,
stars FLOAT,
length FLOAT,
pp90 FLOAT,
pp95 FLOAT,
pp96 FLOAT,
pp97 FLOAT,
pp98 FLOAT,
pp99 FLOAT,
pp995 FLOAT,
pp100 FLOAT
);
