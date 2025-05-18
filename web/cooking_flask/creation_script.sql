-- Create Tables

CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    user_email TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    password TEXT NOT NULL,
    date_joined TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS login_attempt (
    login_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_exists INTEGER NOT NULL, -- 1 for true, 0 for false
    date_time TEXT NOT NULL,
    attempt_num INTEGER NOT NULL,
    ip_address TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS login_session (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_time TEXT NOT NULL,
    cookie TEXT NOT NULL,
    active INTEGER NOT NULL, -- 1 for true, 0 for false
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS recipe (
    recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_name TEXT NOT NULL,
    date_created TEXT NOT NULL,
    recipe_image BLOB,  -- NULL for now, can store image data later
    recipe_description TEXT,
    instructions TEXT NOT NULL,
    tags TEXT,  -- JSON array stored as TEXT
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (user_id)
);

CREATE TABLE IF NOT EXISTS personal_cookbook_entry (
    user_id INTEGER,
    recipe_id INTEGER,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY (user_id) REFERENCES user (user_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (recipe_id)
);

CREATE TABLE IF NOT EXISTS to_try_entry (
    user_id INTEGER,
    recipe_id INTEGER,
    PRIMARY KEY (user_id, recipe_id),
    FOREIGN KEY (user_id) REFERENCES user (user_id),
    FOREIGN KEY (recipe_id) REFERENCES recipe (recipe_id)
);

-- Insert Data

INSERT INTO user VALUES (1, 'admin', 'admin@admin.com', 'AdminFirst', 'AdminLast', 'byuctf{pl34s3_p4r4m3t3r1z3_y0ur_1nputs_4nd_h4sh_p4ssw0rds}', '2024-03-01');
INSERT INTO user VALUES (2, 'steve_and_alex', 'steve@minecraft.net', 'Steve', 'Herobrine', 'robloxistheworst', '2024-03-01');
INSERT INTO user VALUES (3, 'cosmo', 'cosmo_cougar@byu.edu', 'cosmopolitan', 'cougar', 'gobyu84', '2024-03-01');

INSERT INTO login_attempt VALUES (80, 1, '2024-03-01 08:45 AM', 5, '192.168.255.255', 1);
INSERT INTO login_attempt VALUES (81, 0, '2024-03-01 08:48 AM', 1, '192.168.246.255', 2);
INSERT INTO login_attempt VALUES (82, 1, '2024-03-01 08:50 AM', 3, '192.168.245.255', 3);

INSERT INTO login_session VALUES (9, '2024-03-01 08:45 AM', 'hsfksfdsfsdlfldsj', 1, 1);
INSERT INTO login_session VALUES (10, '2024-03-01 08:48 AM', 'fjdkjfkajsfiewkf', 0, 2);
INSERT INTO login_session VALUES (11, '2024-03-01 08:50 AM', 'luerhjnndeurf', 1, 3);

INSERT INTO recipe VALUES (70, 'Pasta', '2024-03-01', NULL, 'It is so good with parm.', 'Boil the pasta', '["Spicy", "Italian"]', 1);
INSERT INTO recipe VALUES (71, 'Omlete', '2024-03-01', NULL, 'Eggman does not approve', 'Crack the eggs', '["Breakfast", "Romantic"]', 2);
INSERT INTO recipe VALUES (72, 'Cake', '2024-03-01', NULL, 'Square cake from minecraft', 'Mix the flour and egg', '["Sweet", "Dessert", "Baking"]', 3);

INSERT INTO personal_cookbook_entry VALUES (1, 70);
INSERT INTO personal_cookbook_entry VALUES (2, 70);
INSERT INTO personal_cookbook_entry VALUES (3, 71);

INSERT INTO to_try_entry VALUES (1, 71);
INSERT INTO to_try_entry VALUES (2, 71);
INSERT INTO to_try_entry VALUES (3, 72);
