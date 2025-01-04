-- Drop all tables to avoid redundancy
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UploadedFile;
DROP TABLE IF EXISTS FastaSequences;
DROP TABLE IF EXISTS Distances;
DROP TABLE IF EXISTS GenotypeAssignments;
DROP TABLE IF EXISTS AnalysisResults;

-- Users Table
CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL COLLATE NOCASE,
    password TEXT NOT NULL
);

-- Uploaded Files Table
CREATE TABLE UploadedFile (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    file_name TEXT NOT NULL,
    file_data BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

-- Fasta Sequences Table
CREATE TABLE FastaSequences (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    header TEXT NOT NULL,
    sequence_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES UploadedFile(file_id) ON DELETE CASCADE
);

-- Consolidated Distances Table
CREATE TABLE Distances (
    distance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id_1 INTEGER,
    sequence_id_2 INTEGER,
    distance FLOAT NOT NULL,
    model TEXT NOT NULL,
    FOREIGN KEY (sequence_id_1) REFERENCES FastaSequences(sequence_id) ON DELETE CASCADE,
    FOREIGN KEY (sequence_id_2) REFERENCES FastaSequences(sequence_id) ON DELETE CASCADE,
    UNIQUE (sequence_id_1, sequence_id_2, model)
);

-- Genotype Assignments Table
CREATE TABLE GenotypeAssignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id INTEGER,
    genotype TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sequence_id) REFERENCES FastaSequences(sequence_id) ON DELETE CASCADE
);

-- Generalized Analysis Results Table
CREATE TABLE AnalysisResults (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    analysis_id TEXT UNIQUE NOT NULL,  -- Store the UUID as a string
    user_id INTEGER,
    file_id INTEGER,
    analysis_type TEXT NOT NULL,      
    result_data TEXT NOT NULL,        
    plot_url TEXT,                   
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (file_id) REFERENCES UploadedFile(file_id) ON DELETE CASCADE
);