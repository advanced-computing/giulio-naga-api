ATTACH DATABASE 'energy.db';

CREATE TABLE energy AS SELECT * FROM read_csv_auto('energy.csv');

