-- Create users (userid, username, current_pp, topplay, average_pp)
CREATE TABLE IF NOT EXISTS users (
    userid INTEGER PRIMARY KEY,
    username TEXT,
    current_pp INTEGER,
    topplay INTEGER,
    average_pp INTEGER
);

-- Create beatmaps (id (autoincrament), beatmapid, beatmap_setid, difficulty_name, stars, mods, pp90, pp95, pp96, pp97, pp98, pp99, pp995, pp100)
CREATE TABLE IF NOT EXISTS beatmaps (
    id INTEGER AUTO_INCREMENT,
    beatmapid INTEGER,
    beatmap_setid INTEGER,
    difficulty_name TEXT,
    stars REAL,
    mods TEXT,
    pp90 REAL,
    pp95 REAL,
    pp96 REAL,
    pp97 REAL,
    pp98 REAL,
    pp99 REAL,
    pp995 REAL,
    pp100 REAL,
    PRIMARY KEY (id)
);