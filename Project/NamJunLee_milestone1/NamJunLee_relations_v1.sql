CREATE TABLE Business (
	bID VARCHAR(22) PRIMARY KEY,
	bname VARCHAR(100) NOT NULL,
	address VARCHAR(100) NOT NULL,
	state CHAR(2) NOT NULL,
	city VARCHAR(50) NOT NULL,
	zip CHAR(9) NOT NULL,
	stars DECIMAL(8,2) NOT NULL,
	reviewCount INTEGER NOT NULL
);

CREATE TABLE Attributes (
	bID VARCHAR(22) NOT NULL,
	attName VARCHAR(100),
	attValue VARCHAR(50),
	PRIMARY KEY (attName, bID),
	FOREIGN KEY (bID) REFERENCES Business
);

CREATE TABLE Categories (
	bID VARCHAR(22) NOT NULL,
	CName VARCHAR(50),
	PRIMARY KEY (CName, bID),
	FOREIGN KEY (bID REFERENCES Business
);

CREATE TABLE Checkin (
	bID VARCHAR(22) NOT NULL,
	day VARCHAR(10),
	hour TIME,
	checkCount INTEGER,
	PRIMARY KEY (bID, day, hour),
	FOREIGN KEY (bID) REFERENCES Business
);

CREATE TABLE User (
	userID VARCHAR(22) PRIMARY KEY,
	userReviewCount INTEGER,
	userAvgStars DECIMAL(8,2),
	useful INTEGER,
	funny INTEGER,
	cool INTEGER
);


CREATE TABLE Review (
	reviewID VARCHAR(22),
	userID VARCHAR(22) NOT NULL,
	bID VARCHAR(22) NOT NULL,
	stars INTEGER,
	Rdate DATE,
	Rtext VARCHAR(500),
	useful INTEGER,
	funny INTEGER,
	cool INTEGER,
	PRIMARY KEY (reviewID, userID, bID),
	FOREIGN KEY (userID) REFERENCES User,
	FOREIGN KEY (bID) REFERENCES Business
);

