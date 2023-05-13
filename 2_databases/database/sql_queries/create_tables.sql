CREATE TABLE items (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  manufacturer VARCHAR(255) NOT NULL,
  cost NUMERIC(10,2) NOT NULL,
  weight NUMERIC(10,2) NOT NULL
);

CREATE TABLE transactions (
  id SERIAL PRIMARY KEY,
  membership_id INTEGER NOT NULL,
  item_ids INTEGER[] NOT NULL,
  total_price NUMERIC(10,2) NOT NULL,
  total_weight NUMERIC(10,2) NOT NULL
);
