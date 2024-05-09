-- ComputeAverageWeightedScoreForUser procedure definition
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(
    IN user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;

    -- Calculate weighted average score
    SELECT SUM(score * weight) / SUM(weight) INTO avg_score
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Update user's average score
    UPDATE users SET average_score = avg_score WHERE id = user_id;
END //

DELIMITER ;
