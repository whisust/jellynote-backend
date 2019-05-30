from yoyo import step

step(
"""
ALTER TABLE users
    ADD COLUMN instruments text[];
"""
)
