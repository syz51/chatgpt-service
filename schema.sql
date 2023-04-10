CREATE
EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE users
(
    user_id    UUID PRIMARY KEY     DEFAULT gen_random_uuid(),
    username   TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversations
(
    conversation_id UUID PRIMARY KEY     DEFAULT gen_random_uuid(),
    user_id         UUID        NOT NULL,
    title           TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at      TIMESTAMPTZ NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE INDEX idx_conversations_user_id_deleted_at
    ON conversations (user_id) WHERE deleted_at IS NULL;

CREATE TABLE conversation_versions
(
    conversation_id UUID        NOT NULL,
    version         INTEGER     NOT NULL,
    messages        JSONB       NOT NULL DEFAULT '[]',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (conversation_id, version),
    FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
);

CREATE INDEX idx_conversation_versions_conversation_id_version
    ON conversation_versions (conversation_id, version DESC);
