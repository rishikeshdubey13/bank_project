-- USERS
CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
);


-- ACCOUNTS
CREATE TABLE IF NOT EXISTS accounts (
    account_number BIGINT PRIMARY KEY,
    name VARCHAR(255),
    balance NUMERIC(12, 2) DEFAULT 0,
    user_id UUID,
    CONSTRAINT fk_user_account 
        FOREIGN KEY (user_id) 
        REFERENCES users(id)
);

-- TRANSACTIONS
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    account_number BIGINT,
    amount NUMERIC(12, 2),
    type VARCHAR(50),
    time TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_account 
        FOREIGN KEY (account_number) 
        REFERENCES accounts(account_number) 
        ON DELETE CASCADE
);

-- REFRESH TOKENS
CREATE TABLE IF NOT EXISTS refresh_tokens (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    token_hash TEXT NOT NULL UNIQUE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    revoked BOOLEAN DEFAULT FALSE,
    device_type VARCHAR(50),
    CONSTRAINT refresh_tokens_user_id_fkey 
        FOREIGN KEY (user_id) 
        REFERENCES users(id) 
        ON DELETE CASCADE
);
