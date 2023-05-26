/* Running the update statement take a long time. 
Therefore using tempory table and update the business table. */

-- reviewcount
CREATE TABLE temptable1 
(
	bid VARCHAR(22) PRIMARY KEY,
	reviewcount INTEGER
);

INSERT INTO temptable1 (bid, reviewcount)
SELECT business.bid, COUNT(review.bid)
FROM review, business
WHERE review.bid = business.bid
GROUP BY business.bid;

UPDATE business
SET reviewcount = 
(SELECT reviewcount
FROM temptable1
WHERE temptable1.bid = business.bid);

-- numCheckins
CREATE TABLE temptable2
(
	bid VARCHAR(22) PRIMARY KEY,
	numCheckins INTEGER
);

INSERT INTO temptable2 (bid, numcheckins)
SELECT business.bid, SUM(checkin.checkcount)
FROM checkin, business
WHERE checkin.bid = business.bid
GROUP BY business.bid;

UPDATE business
SET numcheckins = 
(SELECT numcheckins
FROM temptable2
WHERE temptable2.bid = business.bid);

UPDATE business
SET numcheckins = 0 WHERE numcheckins IS NULL;

-- reviewrating
CREATE TABLE temptable3 (
	bid VARCHAR(22) PRIMARY KEY,
	reviewrating DECIMAL(8,5)
);

INSERT INTO temptable3 (bid, reviewrating)
SELECT business.bid, AVG(review.stars)
FROM review, business
WHERE review.bid = business.bid
GROUP BY business.bid;

UPDATE business
SET reviewrating =
(SELECT reviewrating
FROM temptable3
WHERE temptable3.bid = business.bid);