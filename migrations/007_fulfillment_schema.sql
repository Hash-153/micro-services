-- =============================================================================
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
