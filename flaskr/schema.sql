DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS UploadedFile;
DROP TABLE IF EXISTS PrototypeSequences;
DROP TABLE IF EXISTS FastaSequences;
DROP TABLE IF EXISTS PairwiseDistances;
DROP TABLE IF EXISTS OverallMeanDistances;
DROP TABLE IF EXISTS GenotypeAssignments;
DROP TABLE IF EXISTS GenotypeFrequencies;
DROP TABLE IF EXISTS PhylogeneticTrees;
DROP TABLE IF EXISTS SNPCounts;
DROP TABLE IF EXISTS PDistances;
DROP TABLE IF EXISTS JukesCantorDistances;
DROP TABLE IF EXISTS Kimura2PDistances;
DROP TABLE IF EXISTS Tamura3PDistances;



CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL COLLATE NOCASE,
    password TEXT NOT NULL
);

CREATE TABLE UploadedFile (
    file_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    file_name TEXT NOT NULL,
    file_data BLOB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

CREATE TABLE FastaSequences (
    sequence_id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER,
    header TEXT NOT NULL,
    sequence_data TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES UploadedFile(file_id)
);



CREATE TABLE PairwiseDistances (
    distance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id_1 INTEGER,
    sequence_id_2 INTEGER,
    distance FLOAT NOT NULL,
    FOREIGN KEY (sequence_id_1) REFERENCES FastaSequences(sequence_id),
    FOREIGN KEY (sequence_id_2) REFERENCES FastaSequences(sequence_id),
    UNIQUE (sequence_id_1, sequence_id_2)
);



CREATE TABLE OverallMeanDistances (
    mean_distance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_name TEXT,
    model TEXT NOT NULL,
    mean_distance FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE GenotypeAssignments (
    assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id INTEGER,
    genotype TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sequence_id) REFERENCES FastaSequences(sequence_id)
);


CREATE TABLE GenotypeFrequencies (
    frequency_id INTEGER PRIMARY KEY AUTOINCREMENT,
    genotype TEXT,
    frequency FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE PhylogeneticTrees (
    tree_id INTEGER PRIMARY KEY AUTOINCREMENT,
    tree_data TEXT NOT NULL,
    creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE SNPCounts (
    snp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sequence_id INTEGER,
    snp_count INTEGER NOT NULL,
    FOREIGN KEY (sequence_id) REFERENCES FastaSequences(sequence_id)
);

CREATE TABLE PDistances (
    p_distance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_sequence_id INTEGER,
    reference_sequence_id INTEGER,
    p_distance FLOAT NOT NULL,
    FOREIGN KEY (query_sequence_id) REFERENCES FastaSequences(sequence_id),
    FOREIGN KEY (reference_sequence_id) REFERENCES FastaSequences(sequence_id)
);

CREATE TABLE JukesCantorDistances (
    jc_distance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_sequence_id INTEGER,
    reference_sequence_id INTEGER,
    jc_distance FLOAT NOT NULL,
    FOREIGN KEY (query_sequence_id) REFERENCES FastaSequences(sequence_id),
    FOREIGN KEY (reference_sequence_id) REFERENCES FastaSequences(sequence_id)
);

CREATE TABLE Kimura2PDistances (
    k2p_distance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_sequence_id INTEGER,
    reference_sequence_id INTEGER,
    k2p_distance FLOAT NOT NULL,
    FOREIGN KEY (query_sequence_id) REFERENCES FastaSequences(sequence_id),
    FOREIGN KEY (reference_sequence_id) REFERENCES FastaSequences(sequence_id)
);

CREATE TABLE Tamura3PDistances (
    tamura3p_distance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    query_sequence_id INTEGER,
    reference_sequence_id INTEGER,
    tamura3p_distance FLOAT NOT NULL,
    FOREIGN KEY (query_sequence_id) REFERENCES FastaSequences(sequence_id),
    FOREIGN KEY (reference_sequence_id) REFERENCES FastaSequences(sequence_id)
);

