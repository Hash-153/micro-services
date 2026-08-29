-- =============================================================================
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
