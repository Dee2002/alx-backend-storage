-- AddBonus procedure definition
DELIMITER //

CREATE PROCEDURE AddBonus(
    IN user_id INT,
    IN project_name VARCHAR(255),
    IN score INT
)
BEGIN
    DECLARE project_id INT;

    -- Check if project exists
    SELECT id INTO project_id FROM projects WHERE name = project_name;
    
    -- If project doesn't exist, create it
    IF project_id IS NULL THEN
        INSERT INTO projects (name) VALUES (project_name);
        SET project_id = LAST_INSERT_ID();
    END IF;

    -- Add correction with bonus score
    INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END //

DELIMITER ;
