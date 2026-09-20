-- File: Simon_DBAS27198Assignment2.sql
-- Name: Simon Jaramillo
-- SQL Server Username: jaramisi

-- GuidePerson
CREATE TABLE GuidePerson
(
    GuideNo        INT         IDENTITY(101,1) NOT NULL,
    GuideFirstName VARCHAR(25) NOT NULL,
    GuideLastName  VARCHAR(25) NOT NULL,
    HireDate       DATE        NULL,

    CONSTRAINT PK_GuidePerson PRIMARY KEY (GuideNo)
);

-- Destination
CREATE TABLE Destination
(
    DestinationID   INT         IDENTITY(201,1) NOT NULL,
    DestinationName VARCHAR(30) NOT NULL,

    CONSTRAINT PK_Destination PRIMARY KEY (DestinationID)
);

-- Customer
CREATE TABLE Customer
(
    CustomerID     INT         IDENTITY(301,1) NOT NULL,
    CustFirstName  VARCHAR(25) NOT NULL,
    CustLastName   VARCHAR(25) NOT NULL,
    CustStreet     VARCHAR(20) NULL,
    CustCity       VARCHAR(15) NULL,
    CustStateProv  CHAR(2)     NULL,
    CustPostalCode VARCHAR(10) NULL,
    CustCountry    VARCHAR(15) NULL,

    CONSTRAINT PK_Customer PRIMARY KEY (CustomerID)
);

-- Trip 
CREATE TABLE Trip
(
    GuideNo       INT NOT NULL,
    DestinationID INT NOT NULL,

    CONSTRAINT PK_Trip PRIMARY KEY (GuideNo, DestinationID),

    CONSTRAINT FK_Trip_GuidePerson
        FOREIGN KEY (GuideNo)
        REFERENCES  GuidePerson (GuideNo),

    CONSTRAINT FK_Trip_Destination
        FOREIGN KEY (DestinationID)
        REFERENCES  Destination (DestinationID)
);

-- Booking 
CREATE TABLE Booking
(
    CustomerID    INT   NOT NULL,
    DestinationID INT   NOT NULL,
    TripDate      DATE  NOT NULL,
    TripPrice     MONEY NOT NULL,

    CONSTRAINT PK_Booking PRIMARY KEY (CustomerID, DestinationID, TripDate),

    CONSTRAINT FK_Booking_Customer
        FOREIGN KEY (CustomerID)
        REFERENCES  Customer (CustomerID),

    CONSTRAINT FK_Booking_Destination
        FOREIGN KEY (DestinationID)
        REFERENCES  Destination (DestinationID),

    CONSTRAINT CK_Booking_TripPrice_Positive
        CHECK (TripPrice > 0)
);

DECLARE @GuideNo INT;
DECLARE @DestinationID INT;
DECLARE @CustomerID INT;

INSERT INTO  GuidePerson
    (GuideFirstName, GuideLastName, HireDate)
VALUES
    ('Moe', 'James', '2023-06-10');
SET @GuideNo = CAST(SCOPE_IDENTITY() AS INT);

INSERT INTO  Destination
    (DestinationName)
VALUES
    ('Banff');
SET @DestinationID = CAST(SCOPE_IDENTITY() AS INT);

INSERT INTO  Customer
    (
    CustFirstName, CustLastName, CustStreet, CustCity,
    CustStateProv, CustPostalCode, CustCountry
    )
VALUES
    (
        'Steph', 'Curry', '12 Dundas St', 'Toronto',
        'ON', 'L4M8B2', 'Canada'
);
SET @CustomerID = CAST(SCOPE_IDENTITY() AS INT);

INSERT INTO  Trip
    (GuideNo, DestinationID)
VALUES
    (@GuideNo, @DestinationID);

INSERT INTO  Booking
    (CustomerID, DestinationID, TripDate, TripPrice)
VALUES
    (@CustomerID, @DestinationID, '2025-06-09', 199.99);
