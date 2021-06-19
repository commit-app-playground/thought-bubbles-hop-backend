DROP TABLE IF EXISTS thoughts;
DROP TABLE IF EXISTS thought_classifications;

CREATE TABLE thoughts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content VARCHAR(255) NOT NULL,
    created_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE thought_classifications(
    thought_id INTEGER NOT NULL,
    classification_id INTEGER NOT NULL,
    FOREIGN KEY (thought_id) REFERENCES thoughts(thought_id)
);