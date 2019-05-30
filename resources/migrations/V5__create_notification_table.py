from yoyo import step

step(
    """
    CREATE TABLE IF NOT EXISTS notifications
(
    id         SERIAL    NOT NULL PRIMARY KEY,
    song_id    INT       NOT NULL,
    user_id    INT       NOT NULL,
    message    VARCHAR   NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
) 
    """
)