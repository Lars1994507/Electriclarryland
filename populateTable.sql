INSERT INTO curator (curator_id, name, hire_date, specialization)
VALUES
(1, 'Alice Johnson', '2010-05-14', 'Ancient Artifacts'),
(2, 'Mark Roberts', '2012-09-22', 'Sculptures'),
(3, 'Sophie Martinez', '2015-11-01', 'Paintings');

INSERT INTO artifact (artifact_id, name, origin_country, creation_date, material, curator_id)
VALUES
(1, 'Ancient Vase', 'Greece', '0200-05-10', 'Clay', 1),
(2, 'Medieval Sword', 'England', '1300-08-20', 'Steel', 2),
(3, 'Renaissance Painting', 'Italy', '1500-04-14', 'Canvas', 3),
(4, 'Mayan Statue', 'Mexico', '0800-02-25', 'Stone', 1);

INSERT INTO exhibition (exhibition_id, title, start_date, end_date, location)
VALUES
(1, 'The Art of the Renaissance', '2023-06-01', '2023-12-31', 'Main Gallery'),
(2, 'Medieval Weaponry', '2023-08-15', '2023-10-30', 'Exhibition Hall A'),
(3, 'Ancient Civilizations', '2023-09-05', '2023-12-20', 'Exhibition Hall B');

INSERT INTO exhibition_artifact (exhibition_id, artifact_id, display_position)
VALUES
(1, 3, 'Center Wall'),
(2, 2, 'Middle of the Room'),
(3, 1, 'Entrance Display'),
(3, 4, 'Corner Display');

INSERT INTO restoration (restoration_id, artifact_id, restoration_date, details)
VALUES
(1, 1, '2022-03-15', 'Restored cracks and applied new glaze to the surface'),
(2, 2, '2021-11-10', 'Sharpened blade and polished handle'),
(3, 4, '2023-01-20', 'Repaired missing pieces of the statue');

INSERT INTO artifact_location (artifact_location_id, artifact_id, move_date, from_location, to_location)
VALUES
(1, 1, '2023-05-30', 'Storage Room A', 'Main Gallery'),
(2, 2, '2023-08-10', 'Storage Room B', 'Exhibition Hall A'),
(3, 3, '2023-05-28', 'Storage Room C', 'Main Gallery'),
(4, 4, '2023-09-03', 'Storage Room D', 'Exhibition Hall B');

INSERT INTO curator_exhibition (curator_id, exhibition_id)
VALUES
(1, 3),
(2, 2),
(3, 1);
