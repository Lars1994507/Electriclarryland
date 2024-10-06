DROP TABLE IF EXISTS curator_exhibition;
DROP TABLE IF EXISTS artifact_location;
DROP TABLE IF EXISTS restoration;
DROP TABLE IF EXISTS exhibition_artifact;
DROP TABLE IF EXISTS exhibition;
DROP TABLE IF EXISTS artifact;
DROP TABLE IF EXISTS curator;
CREATE TABLE curator (
    curator_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    hire_date DATE,
    specialization VARCHAR(50)
);

CREATE TABLE artifact (
    artifact_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    origin_country VARCHAR(50),
    creation_date DATE,
    material VARCHAR(50),
    curator_id INTEGER NOT NULL,
    FOREIGN KEY (curator_id) REFERENCES curator (curator_id)
);

CREATE TABLE exhibition (
    exhibition_id INTEGER PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    location VARCHAR(100)
);

CREATE TABLE exhibition_artifact (
    exhibition_id INTEGER NOT NULL,
    artifact_id INTEGER NOT NULL,
    display_position VARCHAR(50),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition (exhibition_id),
    FOREIGN KEY (artifact_id) REFERENCES artifact (artifact_id),
    PRIMARY KEY (exhibition_id, artifact_id)
);

CREATE TABLE restoration (
    restoration_id INTEGER PRIMARY KEY,
    artifact_id INTEGER NOT NULL,
    restoration_date DATE NOT NULL,
    details TEXT,
    FOREIGN KEY (artifact_id) REFERENCES artifact (artifact_id)
);

CREATE TABLE artifact_location (
    artifact_location_id INTEGER PRIMARY KEY,
    artifact_id INTEGER NOT NULL,
    move_date DATE NOT NULL,
    from_location VARCHAR(100),
    to_location VARCHAR(100) NOT NULL,
    FOREIGN KEY (artifact_id) REFERENCES artifact (artifact_id)
);

CREATE TABLE curator_exhibition (
    curator_id INTEGER NOT NULL,
    exhibition_id INTEGER NOT NULL,
    FOREIGN KEY (curator_id) REFERENCES curator (curator_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition (exhibition_id),
    PRIMARY KEY (curator_id, exhibition_id)
);

