CREATE DATABASE temp;
use temp;

CREATE TABLE log_entry (
  temp VARCHAR(10),
  ts VARCHAR(64)
);

INSERT INTO log_entry
  (temp, ts)
VALUES
  ('123.5', '01-01-2021 12:34:56'),
  ('-41.1', '01-01-2021 12:34:57');