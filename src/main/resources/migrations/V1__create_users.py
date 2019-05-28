from yoyo import step

step(
    """
    CREATE TABLE IF NOT EXISTS users
(
    id         SERIAL    NOT NULL UNIQUE PRIMARY KEY,
    name       VARCHAR   NOT NULL,
    mail       VARCHAR   NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
)
""",
    """
    CREATE INDEX users_mail_idx ON users (name)
    """
)
