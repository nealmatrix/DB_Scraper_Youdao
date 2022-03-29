/* Create table words */
--CREATE TABLE--
CREATE TABLE WORDS (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    word varchar(255),
    pron_us varchar(255),
    collins_meaning varchar(255),
    collins_example varchar(255),
    episode varchar(255)
);

--UPDATE
UPDATE WORDS
SET word = 'exchange'
WHERE id = 4292 AND word = 'foreign exchange';

UPDATE WORDS
SET pron_us = '[ɪnˈtɪmədeɪt]'
WHERE id = 4290 AND word = 'intimidate';

UPDATE WORDS
SET collins_meaning = '1.1. ADV You use merely to emphasize that something is only what you say and not better, more important, or more exciting. 仅仅; 只不过 (用来强调某事物不是很重要或很有价值) [强调]' 
WHERE id = 4256 AND word = 'merely';

UPDATE WORDS
SET collins_example = 'He asked if he might conduct us to the ball which was to bring the proceedings to an end.
他问他是否可以带领我们参加将结束诉讼程序的舞会。(google translate)'
WHERE id = 3930 AND word = 'conduct';

UPDATE WORDS
SET episode = 'Other'
WHERE id = 4095 AND word = 'advance';

--DELETE ALL THE RECORDS
-- DELETE FROM WORDS2;

--DELETE THE SPECIFIC RECORD
-- DELETE FROM WORDS WHERE id = 3076;

/* Exchange two rows id */
-- DECLARE @ID INT; -- sqlite not supported

UPDATE WORDS
SET id = 0
WHERE id = 1120; -- row1 id, row1 word

UPDATE WORDS
SET id = 1120   --row1 id
WHERE id = 1121 AND word = 'penis'; --row2 id, row 2 word

UPDATE WORDS
SET id = 1121  --row2 id
WHERE id = 0 AND word = '-'; --row1 word

/* Update id in WORDS */
CREATE TABLE WORDS2 (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    word varchar(255),
    pron_us varchar(255),
    collins_meaning varchar(255),
    collins_example varchar(255),
    episode varchar(255)
);

--INSERT
INSERT INTO WORDS2(word, pron_us, collins_meaning, collins_example, episode)
SELECT word, pron_us, collins_meaning, collins_example, episode
FROM WORDS;

--DROP
DROP TABLE WORDS;

--RENAME
ALTER TABLE WORDS2 RENAME TO WORDS;

/* COCA60000 */
-- CHANGE AUTOINCREMENT FROM 0 (sqlite3 not supported)
-- ALTER TABLE COCA60000 SET AUTOINCREMENT = 0;

/* For test functions */
--CREATE TEST TABLE--
CREATE TABLE TEST (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    word varchar(255),
    pron_us varchar(255),
    collins_meaning varchar(255),
    collins_example varchar(255),
    episode varchar(255)
);

--DELETE THE SPECIFIC RECORD
DELETE FROM TEST WHERE id = 2;

--INSERT INTO TEST DATA
INSERT INTO TEST1 (collins_meaning) VALUES ('"''"');

--CHANGE EPISODE COLUMN POSITION (SQLITE not supported)
--ALTER TABLE TEST ALTER EPISODE varchar(255) FIRST;

--UPDATE ID COLOUMN (SQLITE not supported)
-- ALTER TABLE TEST DROP id;
-- ALTER TABLE TEST ADD id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT FIRST;

-- UPDATE id 
UPDATE TEST1
SET id = id - 1;

--RENAME
ALTER TABLE TEST RENAME TO TEST1;