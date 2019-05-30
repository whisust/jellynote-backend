from yoyo import step

step(
    """
    ALTER TABLE users RENAME COLUMN mail TO email;
    """
)
