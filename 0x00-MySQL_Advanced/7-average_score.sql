-- ComputeAverageScoreForUser procedure definition
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(
    IN p_user_id INT
)
BEGIN
    DECLARE avg_score FLOAT;

    -- Calculate average score
    SELECT AVG(score) INTO avg_score FROM corrections WHERE user_id = p_user_id;

    -- Update user's average score
    UPDATE users SET average_score = avg_score WHERE id = p_user_id;
END //

DELIMITER ;