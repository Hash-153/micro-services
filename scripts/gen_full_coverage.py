import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_comprehensive_migrations():
    # 1. Auth Schema Expanded
    write_file("migrations/001_auth_schema.sql", """-- =============================================================================
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
""")

    # 2. User Schema Expanded
    write_file("migrations/002_user_schema.sql", """-- =============================================================================
-- NovaCommerce User Profiles & Multi-Tenancy Database Schema
-- Database: novacommerce_user_db
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- User Profiles
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(30) NULL,
    avatar_url VARCHAR(1024) NULL,
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    locale VARCHAR(10) NOT NULL DEFAULT 'en-US',
    date_of_birth DATE NULL,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_user ON user_profiles(user_id);

-- Customer Addresses
CREATE TABLE IF NOT EXISTS addresses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    recipient_name VARCHAR(150) NOT NULL,
    company_name VARCHAR(150) NULL,
    street_line1 VARCHAR(255) NOT NULL,
    street_line2 VARCHAR(255) NULL,
    city VARCHAR(100) NOT NULL,
    state_or_province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(30) NOT NULL,
    country_code CHAR(2) NOT NULL,
    is_default_shipping BOOLEAN NOT NULL DEFAULT FALSE,
    is_default_billing BOOLEAN NOT NULL DEFAULT FALSE,
    phone VARCHAR(30) NULL,
    delivery_instructions TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_addresses_user ON addresses(user_id);
CREATE INDEX idx_addresses_country ON addresses(country_code);

-- Organizations (Multi-Tenancy)
CREATE TABLE IF NOT EXISTS organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(150) NOT NULL UNIQUE,
    billing_email VARCHAR(255) NOT NULL,
    tier VARCHAR(50) NOT NULL DEFAULT 'PRO',
    max_seats INT NOT NULL DEFAULT 25,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    tax_identifier VARCHAR(100) NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'MEMBER',
    joined_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(organization_id, user_id)
);

CREATE INDEX idx_org_members_org ON organization_members(organization_id);
CREATE INDEX idx_org_members_user ON organization_members(user_id);
""")

    # 3. Catalog Schema Expanded
    write_file("migrations/003_catalog_schema.sql", """-- =============================================================================
-- NovaCommerce Product Catalog & Pricing Database Schema
-- Database: novacommerce_catalog
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Category Hierarchy
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(150) NOT NULL UNIQUE,
    description TEXT NULL,
    parent_id UUID NULL REFERENCES categories(id) ON DELETE SET NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    meta_title VARCHAR(255) NULL,
    meta_description VARCHAR(500) NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_parent ON categories(parent_id);

-- Product Master Table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    category_id UUID NOT NULL REFERENCES categories(id),
    base_price_cents INT NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_featured BOOLEAN NOT NULL DEFAULT FALSE,
    tags TEXT[] NOT NULL DEFAULT '{}',
    attributes JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX idx_products_sku ON products(sku) WHERE deleted_at IS NULL;
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_tags ON products USING GIN(tags);
CREATE INDEX idx_products_attributes ON products USING GIN(attributes);

-- Product SKU Variants (Size, Color, Edition)
CREATE TABLE IF NOT EXISTS product_variants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sku VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    price_modifier_cents INT NOT NULL DEFAULT 0,
    weight_grams INT NOT NULL DEFAULT 500,
    length_mm INT NOT NULL DEFAULT 100,
    width_mm INT NOT NULL DEFAULT 100,
    height_mm INT NOT NULL DEFAULT 100,
    options JSONB NOT NULL DEFAULT '{}',
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_variants_product ON product_variants(product_id);
CREATE INDEX idx_variants_sku ON product_variants(sku);

-- Product Images
CREATE TABLE IF NOT EXISTS product_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    image_url VARCHAR(1024) NOT NULL,
    alt_text VARCHAR(255) NULL,
    sort_order INT NOT NULL DEFAULT 0,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_product_images_prod ON product_images(product_id);
""")

    # 4. Inventory Schema Expanded
    write_file("migrations/004_inventory_schema.sql", """-- =============================================================================
-- NovaCommerce Real-Time Inventory & Warehouse Storage Schema
-- Database: novacommerce_inventory
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Warehouses
CREATE TABLE IF NOT EXISTS warehouses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    latitude NUMERIC(9,6) NOT NULL,
    longitude NUMERIC(9,6) NOT NULL,
    street_line1 VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state_or_province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(30) NOT NULL,
    country_code CHAR(2) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    capacity_score INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Real-Time Stock Allocations with Optimistic Lock Versioning
CREATE TABLE IF NOT EXISTS inventory_stocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(64) NOT NULL,
    warehouse_id UUID NOT NULL REFERENCES warehouses(id),
    on_hand_quantity INT NOT NULL DEFAULT 0 CHECK (on_hand_quantity >= 0),
    reserved_quantity INT NOT NULL DEFAULT 0 CHECK (reserved_quantity >= 0),
    allocated_quantity INT NOT NULL DEFAULT 0 CHECK (allocated_quantity >= 0),
    safety_stock_threshold INT NOT NULL DEFAULT 5,
    reorder_quantity INT NOT NULL DEFAULT 20,
    bin_location VARCHAR(50) NULL,
    version INT NOT NULL DEFAULT 1,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(sku, warehouse_id)
);

CREATE INDEX idx_inventory_stocks_sku ON inventory_stocks(sku);
CREATE INDEX idx_inventory_stocks_wh ON inventory_stocks(warehouse_id);

-- Distributed Order Reservations
CREATE TABLE IF NOT EXISTS inventory_reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_code VARCHAR(64) NOT NULL UNIQUE,
    order_id UUID NOT NULL,
    sku VARCHAR(64) NOT NULL,
    warehouse_id UUID NOT NULL REFERENCES warehouses(id),
    quantity INT NOT NULL CHECK (quantity > 0),
    is_committed BOOLEAN NOT NULL DEFAULT FALSE,
    is_released BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_reservations_order_id ON inventory_reservations(order_id);
CREATE INDEX idx_reservations_sku ON inventory_reservations(sku);
CREATE INDEX idx_reservations_active ON inventory_reservations(expires_at) WHERE is_released = FALSE AND is_committed = FALSE;
""")

    # 5. Orders Schema Expanded
    write_file("migrations/005_order_schema.sql", """-- =============================================================================
-- NovaCommerce Order State Machine & Checkout Database Schema
-- Database: novacommerce_orders
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Orders Master Table
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(64) NOT NULL UNIQUE,
    user_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING_PAYMENT',
    subtotal_cents INT NOT NULL CHECK (subtotal_cents >= 0),
    tax_cents INT NOT NULL DEFAULT 0 CHECK (tax_cents >= 0),
    shipping_cents INT NOT NULL DEFAULT 0 CHECK (shipping_cents >= 0),
    discount_cents INT NOT NULL DEFAULT 0 CHECK (discount_cents >= 0),
    total_cents INT NOT NULL CHECK (total_cents >= 0),
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    shipping_address JSONB NOT NULL,
    billing_address JSONB NOT NULL,
    coupon_code VARCHAR(50) NULL,
    payment_id UUID NULL,
    shipment_id UUID NULL,
    cancellation_reason VARCHAR(100) NULL,
    notes TEXT NULL,
    idempotency_key VARCHAR(128) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at);

-- Order Items
CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    sku VARCHAR(64) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    variant_name VARCHAR(255) NULL,
    unit_price_cents INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    subtotal_cents INT NOT NULL,
    tax_cents INT NOT NULL DEFAULT 0,
    discount_cents INT NOT NULL DEFAULT 0,
    total_cents INT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_sku ON order_items(sku);
""")

    # 6. Payment & Ledger Schema Expanded
    write_file("migrations/006_payment_schema.sql", """-- =============================================================================
-- NovaCommerce Payment Processing & Double-Entry Ledger Schema
-- Database: novacommerce_payments
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Payment Transactions
CREATE TABLE IF NOT EXISTS payment_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_reference VARCHAR(64) NOT NULL UNIQUE,
    order_id UUID NOT NULL,
    user_id UUID NOT NULL,
    amount_cents INT NOT NULL CHECK (amount_cents > 0),
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(50) NOT NULL,
    method_type VARCHAR(50) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    provider_transaction_id VARCHAR(255) NULL,
    failure_reason TEXT NULL,
    idempotency_key VARCHAR(128) NOT NULL UNIQUE,
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_payments_order ON payment_transactions(order_id);
CREATE INDEX idx_payments_user ON payment_transactions(user_id);
CREATE INDEX idx_payments_status ON payment_transactions(status);

-- Chart of Accounts
CREATE TABLE IF NOT EXISTS ledger_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_number VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    type VARCHAR(50) NOT NULL, -- ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    balance_cents BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Journal Entries (Header)
CREATE TABLE IF NOT EXISTS ledger_journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_number VARCHAR(64) NOT NULL UNIQUE,
    description VARCHAR(255) NOT NULL,
    transaction_id UUID NULL REFERENCES payment_transactions(id),
    reference_type VARCHAR(50) NOT NULL,
    reference_id VARCHAR(128) NOT NULL,
    posted_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Journal Lines (Debits and Credits)
CREATE TABLE IF NOT EXISTS ledger_lines (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    journal_entry_id UUID NOT NULL REFERENCES ledger_journal_entries(id) ON DELETE CASCADE,
    account_id UUID NOT NULL REFERENCES ledger_accounts(id),
    entry_type VARCHAR(10) NOT NULL CHECK (entry_type IN ('DEBIT', 'CREDIT')),
    amount_cents BIGINT NOT NULL CHECK (amount_cents > 0),
    memo VARCHAR(255) NULL
);

CREATE INDEX idx_ledger_lines_entry ON ledger_lines(journal_entry_id);
CREATE INDEX idx_ledger_lines_account ON ledger_lines(account_id);
""")

    # 7. Fulfillment Schema Expanded
    write_file("migrations/007_fulfillment_schema.sql", """-- =============================================================================
-- NovaCommerce Multi-Carrier Fulfillment & Shipping Schema
-- Database: novacommerce_fulfillment
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS shipments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shipment_number VARCHAR(64) NOT NULL UNIQUE,
    order_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL,
    carrier VARCHAR(50) NOT NULL,
    service_level VARCHAR(50) NOT NULL,
    tracking_number VARCHAR(128) NULL,
    tracking_url VARCHAR(1024) NULL,
    shipping_label_url VARCHAR(1024) NULL,
    origin_warehouse_id VARCHAR(64) NOT NULL,
    destination_address JSONB NOT NULL,
    weight_grams INT NOT NULL,
    dimensions_mm JSONB NOT NULL,
    dispatched_at TIMESTAMP WITH TIME ZONE NULL,
    delivered_at TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_shipments_order ON shipments(order_id);
CREATE INDEX idx_shipments_tracking ON shipments(tracking_number);
CREATE INDEX idx_shipments_status ON shipments(status);
""")

    # 8. Notification Schema Expanded
    write_file("migrations/008_notification_schema.sql", """-- =============================================================================
-- NovaCommerce Omni-Channel Notification Schema
-- Database: novacommerce_notifications
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS notification_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipient VARCHAR(255) NOT NULL,
    channel VARCHAR(50) NOT NULL,
    template_id VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    payload JSONB NOT NULL,
    error_details TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_notifications_recipient ON notification_logs(recipient);
CREATE INDEX idx_notifications_status ON notification_logs(status);
CREATE INDEX idx_notifications_created ON notification_logs(created_at);
""")

    # 9. Analytics Schema Expanded
    write_file("migrations/009_analytics_schema.sql", """-- =============================================================================
-- NovaCommerce Real-Time Clickstream & Compliance Audit Schema
-- Database: novacommerce_analytics
-- =============================================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS analytics_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_name VARCHAR(150) NOT NULL,
    user_id VARCHAR(128) NULL,
    session_id VARCHAR(128) NULL,
    properties JSONB NOT NULL DEFAULT '{}',
    ip_address VARCHAR(45) NULL,
    user_agent VARCHAR(512) NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_analytics_event_name ON analytics_events(event_name);
CREATE INDEX idx_analytics_timestamp ON analytics_events(timestamp);
CREATE INDEX idx_analytics_user ON analytics_events(user_id) WHERE user_id IS NOT NULL;

CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    service_name VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    actor_id VARCHAR(128) NOT NULL,
    actor_role VARCHAR(50) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(128) NOT NULL,
    changes JSONB NULL,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_actor ON audit_logs(actor_id);
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
""")

    print("Generated comprehensive PostgreSQL migrations.")

def generate_adrs_21_to_40():
    adrs = [
        ("021", "Polyglot Microservices vs Unified TypeScript Stack", "Standardization on TypeScript with Node.js 22 LTS for core microservices and Python for ML/analytics clients."),
        ("022", "Zero-Trust Service-to-Service mTLS and JWT Forwarding", "All internal microservice RPC calls must validate mutual TLS and forward user identity context."),
        ("023", "Continuous Deployment Strategy using Canary Releases with Argo Rollouts", "Implement canary deployments with 10% traffic increments and automated metric rollback."),
        ("024", "Redis Caching Topologies and Eviction Policies", "Standardize on Redis cluster with volatile-lru eviction for transient tokens and rate limits."),
        ("025", "Schema Evolution and Protobuf Backward Compatibility Rules", "Enforce strict Protobuf field numbering and additive-only schema evolution."),
        ("026", "Centralized Log Aggregation and Structured JSON Format", "All logs must adhere to ECS (Elastic Common Schema) JSON formatted output."),
        ("027", "Disaster Recovery RTO and RPO Targets", "Target Recovery Time Objective (RTO) of 15 minutes and Recovery Point Objective (RPO) of zero data loss."),
        ("028", "Dynamic Feature Flagging using Redis and Remote Config", "Evaluate feature toggles in memory with sub-millisecond local Redis caches."),
        ("029", "Secret Management via Kubernetes Secrets and Cloud KMS", "Zero plain-text credentials in repository; runtime injection via Kubernetes Secrets."),
        ("030", "Prometheus Metric Naming Conventions and Alerting Thresholds", "Standardize metric naming `novacommerce_<service>_<metric>_<unit>`.")
    ]

    for num, title, summary in adrs:
        content = f"""# ADR-{num}: {title}

## Status
**ACCEPTED** (Date: 2026-08-29)

## Context
As NovaCommerce expands horizontally to support millions of monthly active shoppers, clear architectural standardization across all engineering squads is essential to ensure operational stability, security, and developer velocity.

## Summary & Decision
{summary}

### Key Principles:
1. **Consistency**: All microservices follow identical design patterns and coding conventions.
2. **Measurability**: Every architectural decision is monitored through real-time Prometheus SLIs.
3. **Resilience**: Failures are isolated to bounded contexts without cascading service degradation.

## Consequences
- **Positive**: High predictability in production operations and rapid onboarding.
- **Negative**: Strict architectural review requirements for cross-cutting modifications.
"""
        write_file(f"docs/adr/ADR-{num}-{title.lower().replace(' ', '-').replace('/', '-')}.md", content)

    print("Generated ADRs 021 through 030.")

if __name__ == "__main__":
    generate_comprehensive_migrations()
    generate_adrs_21_to_40()
    print("Full coverage generation completed.")
