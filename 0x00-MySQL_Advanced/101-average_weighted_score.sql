-- ComputeAverageWeightedScoreForUsers procedure definition
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE done BOOLEAN DEFAULT FALSE;
    DECLARE user_id INT;
    DECLARE avg_score FLOAT;

    -- Declare cursor for looping through users
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open cursor
    OPEN cur;

    -- Loop through users
    user_loop: LOOP
        FETCH cur INTO user_id;
        IF done THEN
            LEAVE user_loop;
        END IF;

        -- Calculate weighted average score for user
        SELECT SUM(score * weight) / SUM(weight) INTO avg_score
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

        -- Update user's average score
        UPDATE users SET average_score = avg_score WHERE id = user_id;
    END LOOP;

    -- Close cursor
    CLOSE cur;
END //

DELIMITER ;
