CREATE_MESSAGE_TABLE = """
    CREATE TABLE IF NOT EXISTS messages (
        message_id INT PRIMARY KEY,
        fire_count INT,
        first_reactor TEXT,
        content TEXT,
        author TEXT,
        jump_url TEXT
    );
"""

CREATE_ATTACHMENT_TABLE = """
    CREATE TABLE IF NOT EXISTS attachments (
        attachment_id INT PRIMARY KEY,
        message_id INT,
        filename TEXT,
        url TEXT
    );
"""

MESSAGE_EXISTS = "SELECT * FROM messages WHERE message_id = ?"

INSERT_MESSAGE = """
    INSERT INTO messages (message_id, fire_count, first_reactor, content, author, jump_url) VALUES (?, ?, ?, ?, ?, ?)
"""

INSERT_ATTACHMENT = """
    INSERT INTO attachments (attachment_id, message_id, filename, url) VALUES (?, ?, ?, ?)
"""

DELETE_MESSAGE = """
    DELETE FROM messages
    WHERE message_id = ?;
"""

DELETE_ATTACHMENTS = """
    DELETE FROM attachments
    WHERE message_id = ?;
"""

UPDATE_FIRE_COUNT = """
    UPDATE messages
    SET fire_count = ?
    WHERE message_id = ?;
"""
