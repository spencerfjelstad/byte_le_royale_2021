--createdb ByteLeRoyaleDB;

CREATE TABLE University (
    uniID    serial PRIMARY KEY,
    uniName   varchar(100) NOT NULL CHECK (uniName <> '')
);

CREATE TABLE TeamType (
    teamTypeID    serial PRIMARY KEY,
    teamTypeName   varchar(100) NOT NULL CHECK (teamName <> '')
);

CREATE TABLE Team (
    teamID     uuid PRIMARY KEY,
    teamTypeID integer REFERENCES TeamType(teamTypeID),
    teamName   varchar(100) NOT NULL CHECK (teamName <> ''),
    uniID integer REFERENCES University (uniID),
    UNIQUE(teamName)
);

CREATE TABLE Submission (
    teamID    uuid REFERENCES Team (teamID),
    SubmissionID  serial PRIMARY KEY,
    valid  boolean NOT NULL DEFAULT False,
    submitTime "timestamp" DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE CodeFile(
    SubmissionID integer REFERENCES Submission (SubmissionID),
    filetext VARCHAR
);

CREATE TABLE Run(
    SubmissionID integer REFERENCES Submission (SubmissionID),
    RunID serial PRIMARY KEY,
    Score integer
);

CREATE TABLE Logs (
    runID integer REFERENCES Submission (SubmissionID),
    logText VARCHAR
);

-- CREATE TABLE Run(
--     SubmissionID REFERENCES Submission (SubmissionID),
--     SubmissionID2 REFERENCES Submission (SubmissionID),
--     RunID integer PRIMARY KEY DEFAULT nextval('serial'),
--     winnerSubmission REFERENCES Submission (SubmissionID)
-- );

INSERT INTO teamtype (teamname) VALUES ('Graduate'), ('Under Graduate'), ('Alumni');
INSERT INTO university(uniname) VALUES ('NDSU'), ('UND'), ('MSUM');