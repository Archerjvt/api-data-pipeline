-- API Data Pipeline - Target Database Schema
-- Author: Vijay Teli

CREATE TABLE API_Users (
    UserID INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Username VARCHAR(50),
    Email VARCHAR(100),
    Phone VARCHAR(50),
    Website VARCHAR(100),
    Street VARCHAR(200),
    City VARCHAR(100),
    Zipcode VARCHAR(20),
    Latitude VARCHAR(20),
    Longitude VARCHAR(20),
    CompanyName VARCHAR(100),
    CompanyBS VARCHAR(200),
    ExtractedDate DATE,
    Source VARCHAR(50)
);

CREATE TABLE API_Posts (
    PostID INT PRIMARY KEY,
    UserID INT FOREIGN KEY REFERENCES API_Users(UserID),
    Title VARCHAR(500),
    Body TEXT,
    TitleWordCount INT,
    BodyWordCount INT,
    TotalUserPosts INT,
    ExtractedDate DATE
);

CREATE INDEX IX_Posts_UserID ON API_Posts(UserID);
CREATE INDEX IX_Posts_ExtractDate ON API_Posts(ExtractedDate);
