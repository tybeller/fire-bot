CREATE_MESSAGE_TABLE = """
    CREATE TABLE IF NOT EXISTS messages (
        message_id INT PRIMARY KEY,
        channel_id INT,
        fire_count INT
    );
"""

MESSAGE_EXISTS = "SELECT * FROM messages WHERE message_id = ?"

INSERT_MESSAGE = "INSERT INTO messages (message_id, channel_id, fire_count) VALUES (?, ?, ?)"

DELETE_MESSAGE = """
    DELETE FROM messages
    WHERE message_id = ?;
"""

UPDATE_FIRE_COUNT = """
    UPDATE messages
    SET fire_count = ?
    WHERE message_id = ?;
"""

FETCH_TOP_3 = """
    SELECT *
    FROM messages 
    ORDER BY fire_count DESC 
    LIMIT 3;
"""
