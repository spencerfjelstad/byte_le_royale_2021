--createdb ByteLeRoyaleDB;

CREATE TABLE University (
    uniID    serial PRIMARY KEY,
    uniName   varchar(100) NOT NULL CHECK (uniName <> '')
);

CREATE TABLE Team (
    teamID     uuid PRIMARY KEY,
    teamType   varchar(40) NOT NULL CHECK (teamType <> ''),
    teamName   varchar(100) NOT NULL CHECK (teamName <> ''),
    uniID integer REFERENCES University (uniID)
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
)

-- CREATE TABLE Run(
--     SubmissionID REFERENCES Submission (SubmissionID),
--     SubmissionID2 REFERENCES Submission (SubmissionID),
--     RunID integer PRIMARY KEY DEFAULT nextval('serial'),
--     winnerSubmission REFERENCES Submission (SubmissionID)
-- );