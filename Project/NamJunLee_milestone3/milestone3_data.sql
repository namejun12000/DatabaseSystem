-- create zipcode data table
CREATE TABLE zipcodeData (
	zip CHAR(9) PRIMARY KEY,
	medianIncome INTEGER,
	meanIncome INTEGER,
	population INTEGER
);

/* create temporyary table using update 
 (for shortly running time) */

-- insert total business in each zip
CREATE TABLE tempTablezip1
(
	zip CHAR(9) PRIMARY KEY,
	totalbusiness NUMERIC
);

INSERT INTO temptablezip1 (zip, totalbusiness)
SELECT bs.zip, COUNT(bs.bid)
FROM business as bs, zipcodedata as zc
WHERE bs.zip = zc.zip
GROUP BY bs.zip;

-- insert total population in each zip
CREATE TABLE tempTablezip2
(
	zip CHAR(9) PRIMARY KEY,
	totalpopulation NUMERIC
);

INSERT INTO temptablezip2 (zip,totalpopulation)
SELECT bs.zip, zc.population
FROM business as bs, zipcodedata as zc
WHERE bs.zip = zc.zip
GROUP BY bs.zip, zc.population;

-- insert average income in each zip
CREATE TABLE tempTablezip3
(
	zip CHAR(9) PRIMARY KEY,
	avgincome DECIMAL(8,1)
);

INSERT INTO temptablezip3 (zip,avgincome)
SELECT bs.zip, zc.meanincome
FROM business as bs, zipcodedata as zc
WHERE bs.zip = zc.zip
GROUP BY bs.zip, zc.meanincome;

-- create new 3 columns in business table.
ALTER TABLE business ADD totalbusiness NUMERIC;
ALTER TABLE business ADD totalpopulation NUMERIC;
ALTER TABLE business ADD avgincome DECIMAL(8,1);

-- update 3 columns in business table (each zipcode)
UPDATE business
SET totalpopulation = 
(SELECT totalpopulation
FROM temptablezip2
WHERE temptablezip2.zip = business.zip);

UPDATE business
SET totalbusiness = 
(SELECT totalbusiness
FROM temptablezip1
WHERE temptablezip1.zip = business.zip);

UPDATE business
SET avgincome = 
(SELECT avgincome
FROM temptablezip3
WHERE temptablezip3.zip = business.zip);

-- Population

SELECT cs.cname, bs.bname, ROUND(bs.stars,1), bs.numcheckins, bs.reviewrating, bs.reviewcount
FROM business as bs, categories as cs
WHERE cs.bid = bs.bid AND
bs.zip = '85248' AND 
(cs.cname, bs.numcheckins) IN (SELECT cname, MAX(numcheckins)
			FROM business, categories 
						 WHERE business.bid = categories.bid AND
						 business.zip = '85248'
						 GROUP BY cname)		
GROUP BY cname
ORDER BY cs.cname;

-- sucessful

SELECT bs.bname, bs.address, ROUND(bs.stars,1), bs.reviewcount, bs.numcheckins
FROM business as bs, categories as cs
WHERE cs.bid = bs.bid AND
bs.zip = '85248' AND
(bs.numcheckins) > (SELECT AVG(numcheckins)
				 FROM business, categories
				 WHERE business.bid = categories.bid AND
				 business.zip = '85248' AND
					categories.cname = cs.cname
				 GROUP BY cname)
GROUP BY bs.bname, bs.address, bs.stars, bs.reviewcount, bs.numcheckins
ORDER BY bs.numcheckins DESC;