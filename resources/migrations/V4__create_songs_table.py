from yoyo import step

step(
    """
    CREATE TABLE IF NOT EXISTS songs
(
    id          SERIAL    NOT NULL PRIMARY KEY,
    name        VARCHAR   NOT NULL,
    instruments TEXT[]    NOT NULL,
    created_at  TIMESTAMP NOT NULL DEFAULT now(),
    updated_at  TIMESTAMP NOT NULL DEFAULT now()
)
    """
)
