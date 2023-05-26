CREATE TABLE Business (
	bID VARCHAR(22) PRIMARY KEY,
	bname VARCHAR(100) NOT NULL,
	address VARCHAR(100),
	city VARCHAR(50),
	state CHAR(2),
	zip CHAR(9),
	stars DECIMAL(8,1),
	reviewCount INTEGER,
	numCheckins INTEGER DEFAULT 0, 
	reviewRating DECIMAL(8,5) DEFAULT 0.0
);

CREATE TABLE Attributes (
	bID VARCHAR(22) NOT NULL,
	attName VARCHAR(100) NOT NULL,
	attValue BOOLEAN,
	PRIMARY KEY (attName, bID),
	FOREIGN KEY (bID) REFERENCES Business
);

CREATE TABLE Categories (
	bID VARCHAR(22) NOT NULL,
	CName VARCHAR(50) NOT NULL,
	PRIMARY KEY (CName, bID),
	FOREIGN KEY (bID) REFERENCES Business
);

CREATE TABLE Checkin (
	bID VARCHAR(22) NOT NULL,
	day VARCHAR(10) NOT NULL,
	hour TIME NOT NULL,
	checkCount INTEGER,
	PRIMARY KEY (bID, day, hour),
	FOREIGN KEY (bID) REFERENCES Business
);

CREATE TABLE Users (
	userID VARCHAR(22) PRIMARY KEY,
	userReviewCount INTEGER,
	userAvgStars DECIMAL(8,5),
	funny INTEGER,
	useful INTEGER,
	cool INTEGER
);


CREATE TABLE Review (
	reviewID VARCHAR(22) NOT NULL,
	userID VARCHAR(22) NOT NULL,
	bID VARCHAR(22) NOT NULL,
	stars INTEGER,
	Rdate DATE,
	useful INTEGER,
	funny INTEGER,
	cool INTEGER,
	PRIMARY KEY (reviewID, userID, bID),
	FOREIGN KEY (userID) REFERENCES Users,
	FOREIGN KEY (bID) REFERENCES Business
);



