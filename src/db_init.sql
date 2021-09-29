
CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY,
  first_name TEXT NOT NULL,
  username TEXT
);

CREATE TABLE IF NOT EXISTS topic (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER NOT NULL,
    "name" TEXT NOT NULL,
    UNIQUE("user_id", "name"),
    FOREIGN KEY ("user_id") REFERENCES user (id)
);



CREATE TABLE IF NOT EXISTS note (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "topic_id" INTEGER NOT NULL,
    "text" TEXT NOT NULL,
    FOREIGN KEY ("topic_id") REFERENCES topic (id)
);
