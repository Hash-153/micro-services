-- =============================================================================
-- NovaCommerce Authentication & Identity Access Management (IAM) Database Schema
-- Database: novacommerce_auth
-- Engine: PostgreSQL 16+
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Function to automatically update timestamp on entity mutation
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Enum Tables for Strict Relational Integrity
CREATE TABLE IF NOT EXISTS user_roles (
    role_key VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

INSERT INTO user_roles (role_key, description) VALUES
('SUPER_ADMIN', 'Platform Administrator with unrestricted cross-tenant access'),
('ADMIN', 'Organization Administrator with tenant management privileges'),
('OPERATIONS_MANAGER', 'Fulfillment and warehouse operational lead'),
('INVENTORY_MANAGER', 'Stock allocation and procurement supervisor'),
('FINANCE_ANALYST', 'Financial ledger, payouts, and revenue auditor'),
('SUPPORT_AGENT', 'Customer support representative with order update permissions'),
('CUSTOMER', 'Standard verified e-commerce customer account'),
('GUEST', 'Anonymous guest checkout visitor'),
('SYSTEM_INTERNAL', 'Service-to-service internal gRPC daemon account')
ON CONFLICT (role_key) DO NOTHING;

CREATE TABLE IF NOT EXISTS account_statuses (
    status_key VARCHAR(50) PRIMARY KEY,
    description TEXT NOT NULL
);

INSERT INTO account_statuses (status_key, description) VALUES
('ACTIVE', 'Account is active in good standing'),
('PENDING_VERIFICATION', 'Account registered awaiting email/phone verification'),
('SUSPENDED', 'Account temporarily suspended by fraud/security rule'),
('DEACTIVATED', 'Account closed per customer request'),
('LOCKED', 'Account locked due to excessive failed login attempts')
ON CONFLICT (status_key) DO NOTHING;

-- Core Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL REFERENCES user_roles(role_key) DEFAULT 'CUSTOMER',
    status VARCHAR(50) NOT NULL REFERENCES account_statuses(status_key) DEFAULT 'ACTIVE',
    kyc_status VARCHAR(50) NOT NULL DEFAULT 'NOT_SUBMITTED',
    organization_id UUID NULL,
    is_mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_secret VARCHAR(255) NULL,
    failed_login_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE NULL,
    last_login_at TIMESTAMP WITH TIME ZONE NULL,
    password_changed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE NULL,
    CONSTRAINT uq_users_email_active UNIQUE (email)
);

CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_org ON users(organization_id) WHERE organization_id IS NOT NULL;

CREATE TRIGGER trg_users_updated_at
BEFORE UPDATE ON users
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- User Sessions & Refresh Tokens
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL UNIQUE,
    ip_address VARCHAR(45) NULL,
    user_agent VARCHAR(512) NULL,
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    revoked_at TIMESTAMP WITH TIME ZONE NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    last_activity_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_token ON user_sessions(refresh_token_hash) WHERE is_revoked = FALSE;
CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);

-- Password Reset Tokens
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL UNIQUE,
    is_used BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_pwd_tokens_user ON password_reset_tokens(user_id);

-- Outbox Events Table for Transactional Consistency
CREATE TABLE IF NOT EXISTS outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id VARCHAR(128) NOT NULL,
    event_type VARCHAR(150) NOT NULL,
    payload JSONB NOT NULL,
    correlation_id VARCHAR(128) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
    retry_count INT NOT NULL DEFAULT 0,
    last_error TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    processed_at TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX idx_auth_outbox_pending ON outbox_events(status, created_at) WHERE status = 'PENDING';
