-- SQL script that creates a stored procedure AddBonus
-- that adds a new correction for a student.

DELIMITER ##

DROP PROCEDURE IF EXISTS AddBonus;
CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score FLOAT
)
BEGIN
DECLARE project_id INT;

-- Check to verify if project exists
SELECT id INTO project_id FROM projects WHERE name = project_name;

-- If the project does not exist create one
IF project_id IS NULL THEN
    INSERT INTO projects (name) VALUES (project_name);
    SET project_id = LAST_INSERT_ID();
END IF;

-- Insert correction
INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END;
##

DELIMITER ;
