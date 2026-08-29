import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_proto():
    write_file("proto/common/v1/common.proto", """syntax = "proto3";

package novacommerce.common.v1;

enum Currency {
  CURRENCY_UNSPECIFIED = 0;
  CURRENCY_USD = 1;
  CURRENCY_EUR = 2;
  CURRENCY_GBP = 3;
  CURRENCY_CAD = 4;
  CURRENCY_AUD = 5;
  CURRENCY_JPY = 6;
}

message Money {
  int64 amount = 1; // minor units (e.g. cents)
  Currency currency = 2;
}

message Address {
  string recipient_name = 1;
  string street_line1 = 2;
  string street_line2 = 3;
  string city = 4;
  string state_province = 5;
  string postal_code = 6;
  string country_code = 7;
}

message PaginationRequest {
  int32 page = 1;
  int32 limit = 2;
}

message PaginationMetadata {
  int32 page = 1;
  int32 limit = 2;
  int64 total_items = 3;
  int32 total_pages = 4;
}
""")

    write_file("proto/auth/v1/auth.proto", """syntax = "proto3";

package novacommerce.auth.v1;

service AuthService {
  rpc Register(RegisterRequest) returns (AuthResponse);
  rpc Login(LoginRequest) returns (AuthResponse);
  rpc ValidateToken(ValidateTokenRequest) returns (ValidateTokenResponse);
  rpc RefreshToken(RefreshTokenRequest) returns (AuthResponse);
}

message RegisterRequest {
  string email = 1;
  string password = 2;
  string first_name = 3;
  string last_name = 4;
  string phone_number = 5;
}

message LoginRequest {
  string email = 1;
  string password = 2;
  string mfa_code = 3;
}

message ValidateTokenRequest {
  string token = 1;
}

message ValidateTokenResponse {
  bool is_valid = 1;
  string user_id = 2;
  string email = 3;
  string role = 4;
}

message RefreshTokenRequest {
  string refresh_token = 1;
}

message AuthResponse {
  string access_token = 1;
  string refresh_token = 2;
  int64 expires_in = 3;
  string user_id = 4;
}
""")

    write_file("proto/catalog/v1/catalog.proto", """syntax = "proto3";

package novacommerce.catalog.v1;

import "proto/common/v1/common.proto";

service CatalogService {
  rpc GetProduct(GetProductRequest) returns (ProductResponse);
  rpc ListProducts(ListProductsRequest) returns (ListProductsResponse);
}

message GetProductRequest {
  string product_id = 1;
  string sku = 2;
}

message ListProductsRequest {
  novacommerce.common.v1.PaginationRequest pagination = 1;
  string category_id = 2;
  string search_query = 3;
}

message ProductResponse {
  string id = 1;
  string sku = 2;
  string name = 3;
  string slug = 4;
  string description = 5;
  string category_id = 6;
  novacommerce.common.v1.Money base_price = 7;
  bool is_active = 8;
  repeated string tags = 9;
}

message ListProductsResponse {
  repeated ProductResponse products = 1;
  novacommerce.common.v1.PaginationMetadata pagination = 2;
}
""")

    write_file("proto/inventory/v1/inventory.proto", """syntax = "proto3";

package novacommerce.inventory.v1;

service InventoryService {
  rpc GetStock(GetStockRequest) returns (StockResponse);
  rpc ReserveStock(ReserveStockRequest) returns (ReservationResponse);
  rpc ReleaseStock(ReleaseStockRequest) returns (ReleaseStockResponse);
}

message GetStockRequest {
  string sku = 1;
  string warehouse_id = 2;
}

message StockResponse {
  string sku = 1;
  int32 on_hand_quantity = 2;
  int32 reserved_quantity = 3;
  int32 available_quantity = 4;
}

message ReserveStockRequest {
  string order_id = 1;
  string sku = 2;
  int32 quantity = 3;
}

message ReservationResponse {
  string reservation_id = 1;
  string reservation_code = 2;
  string order_id = 3;
  string sku = 4;
  int32 quantity = 5;
  string expires_at = 6;
}

message ReleaseStockRequest {
  string order_id = 1;
}

message ReleaseStockResponse {
  bool success = 1;
  int32 released_count = 2;
}
""")

    write_file("proto/order/v1/order.proto", """syntax = "proto3";

package novacommerce.order.v1;

import "proto/common/v1/common.proto";

service OrderService {
  rpc CreateOrder(CreateOrderRequest) returns (OrderResponse);
  rpc GetOrder(GetOrderRequest) returns (OrderResponse);
}

message OrderItem {
  string sku = 1;
  int32 quantity = 2;
  novacommerce.common.v1.Money unit_price = 3;
}

message CreateOrderRequest {
  string user_id = 1;
  repeated OrderItem items = 2;
  novacommerce.common.v1.Address shipping_address = 3;
  novacommerce.common.v1.Address billing_address = 4;
  string idempotency_key = 5;
}

message GetOrderRequest {
  string order_id = 1;
}

message OrderResponse {
  string id = 1;
  string order_number = 2;
  string status = 3;
  novacommerce.common.v1.Money total_amount = 4;
  repeated OrderItem items = 5;
  string created_at = 6;
}
""")

    write_file("proto/payment/v1/payment.proto", """syntax = "proto3";

package novacommerce.payment.v1;

import "proto/common/v1/common.proto";

service PaymentService {
  rpc AuthorizePayment(AuthorizePaymentRequest) returns (PaymentResponse);
  rpc RefundPayment(RefundPaymentRequest) returns (PaymentResponse);
}

message AuthorizePaymentRequest {
  string order_id = 1;
  string user_id = 2;
  novacommerce.common.v1.Money amount = 3;
  string payment_method_token = 4;
  string idempotency_key = 5;
}

message RefundPaymentRequest {
  string payment_id = 1;
  novacommerce.common.v1.Money amount = 2;
  string reason = 3;
}

message PaymentResponse {
  string payment_id = 1;
  string status = 2;
  string transaction_reference = 3;
  novacommerce.common.v1.Money amount = 4;
  string created_at = 5;
}
""")

    write_file("proto/fulfillment/v1/fulfillment.proto", """syntax = "proto3";

package novacommerce.fulfillment.v1;

import "proto/common/v1/common.proto";

service FulfillmentService {
  rpc CreateShipment(CreateShipmentRequest) returns (ShipmentResponse);
  rpc GetShipmentStatus(GetShipmentStatusRequest) returns (ShipmentResponse);
}

message CreateShipmentRequest {
  string order_id = 1;
  novacommerce.common.v1.Address destination_address = 2;
  string carrier_code = 3;
}

message GetShipmentStatusRequest {
  string shipment_id = 1;
  string tracking_number = 2;
}

message ShipmentResponse {
  string shipment_id = 1;
  string shipment_number = 2;
  string tracking_number = 3;
  string status = 4;
  string carrier = 5;
  string tracking_url = 6;
}
""")

def generate_migrations():
    write_file("migrations/001_auth_schema.sql", """-- NovaCommerce Auth & Identity Database Schema
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'CUSTOMER',
    status VARCHAR(50) NOT NULL DEFAULT 'ACTIVE',
    kyc_status VARCHAR(50) NOT NULL DEFAULT 'NOT_SUBMITTED',
    organization_id UUID NULL,
    is_mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    mfa_secret VARCHAR(255) NULL,
    failed_login_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMP WITH TIME ZONE NULL,
    last_login_at TIMESTAMP WITH TIME ZONE NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE NULL
);

CREATE INDEX idx_users_email ON users(email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_status ON users(status);

CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    refresh_token_hash VARCHAR(255) NOT NULL,
    user_agent VARCHAR(512) NULL,
    ip_address VARCHAR(45) NULL,
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);
""")

    write_file("migrations/002_user_schema.sql", """-- NovaCommerce User Profiles & Addresses Database Schema
CREATE TABLE IF NOT EXISTS user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(30) NULL,
    avatar_url VARCHAR(1024) NULL,
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    locale VARCHAR(10) NOT NULL DEFAULT 'en-US',
    metadata JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);

CREATE TABLE IF NOT EXISTS addresses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    recipient_name VARCHAR(150) NOT NULL,
    street_line1 VARCHAR(255) NOT NULL,
    street_line2 VARCHAR(255) NULL,
    city VARCHAR(100) NOT NULL,
    state_or_province VARCHAR(100) NOT NULL,
    postal_code VARCHAR(30) NOT NULL,
    country_code CHAR(2) NOT NULL,
    is_default_shipping BOOLEAN NOT NULL DEFAULT FALSE,
    is_default_billing BOOLEAN NOT NULL DEFAULT FALSE,
    phone VARCHAR(30) NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_addresses_user_id ON addresses(user_id);
""")

    write_file("migrations/003_catalog_schema.sql", """-- NovaCommerce Product Catalog Database Schema
CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    slug VARCHAR(150) NOT NULL UNIQUE,
    description TEXT NULL,
    parent_id UUID NULL REFERENCES categories(id) ON DELETE SET NULL,
    display_order INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_parent ON categories(parent_id);

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
""")

    write_file("migrations/004_inventory_schema.sql", """-- NovaCommerce Inventory Management Database Schema
CREATE TABLE IF NOT EXISTS warehouses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    address_id UUID NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    capacity_score INT NOT NULL DEFAULT 100,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS inventory_stocks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sku VARCHAR(64) NOT NULL,
    warehouse_id UUID NOT NULL REFERENCES warehouses(id),
    on_hand_quantity INT NOT NULL DEFAULT 0,
    reserved_quantity INT NOT NULL DEFAULT 0,
    allocated_quantity INT NOT NULL DEFAULT 0,
    safety_stock_threshold INT NOT NULL DEFAULT 5,
    reorder_quantity INT NOT NULL DEFAULT 20,
    bin_location VARCHAR(50) NULL,
    version INT NOT NULL DEFAULT 1,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    UNIQUE(sku, warehouse_id)
);

CREATE INDEX idx_inventory_stocks_sku ON inventory_stocks(sku);

CREATE TABLE IF NOT EXISTS inventory_reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    reservation_code VARCHAR(64) NOT NULL UNIQUE,
    order_id UUID NOT NULL,
    sku VARCHAR(64) NOT NULL,
    warehouse_id UUID NOT NULL REFERENCES warehouses(id),
    quantity INT NOT NULL,
    is_committed BOOLEAN NOT NULL DEFAULT FALSE,
    is_released BOOLEAN NOT NULL DEFAULT FALSE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_reservations_order_id ON inventory_reservations(order_id);
CREATE INDEX idx_reservations_expires ON inventory_reservations(expires_at) WHERE is_released = FALSE AND is_committed = FALSE;
""")

    write_file("migrations/005_order_schema.sql", """-- NovaCommerce Orders and Order Items Database Schema
CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_number VARCHAR(64) NOT NULL UNIQUE,
    user_id UUID NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'PENDING_PAYMENT',
    subtotal_cents INT NOT NULL,
    tax_cents INT NOT NULL,
    shipping_cents INT NOT NULL,
    discount_cents INT NOT NULL DEFAULT 0,
    total_cents INT NOT NULL,
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
CREATE INDEX idx_orders_idempotency ON orders(idempotency_key);

CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    sku VARCHAR(64) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    variant_name VARCHAR(255) NULL,
    unit_price_cents INT NOT NULL,
    quantity INT NOT NULL,
    subtotal_cents INT NOT NULL,
    tax_cents INT NOT NULL DEFAULT 0,
    discount_cents INT NOT NULL DEFAULT 0,
    total_cents INT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'
);

CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_sku ON order_items(sku);
""")

    write_file("migrations/006_payment_schema.sql", """-- NovaCommerce Payments and Double-Entry Ledger Database Schema
CREATE TABLE IF NOT EXISTS payment_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    transaction_reference VARCHAR(64) NOT NULL UNIQUE,
    order_id UUID NOT NULL,
    user_id UUID NOT NULL,
    amount_cents INT NOT NULL,
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

CREATE INDEX idx_payments_order_id ON payment_transactions(order_id);
CREATE INDEX idx_payments_user_id ON payment_transactions(user_id);

CREATE TABLE IF NOT EXISTS ledger_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_number VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    type VARCHAR(50) NOT NULL,
    currency CHAR(3) NOT NULL DEFAULT 'USD',
    balance_cents BIGINT NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ledger_journal_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entry_number VARCHAR(64) NOT NULL UNIQUE,
    description VARCHAR(255) NOT NULL,
    transaction_id UUID NULL REFERENCES payment_transactions(id),
    reference_type VARCHAR(50) NOT NULL,
    reference_id VARCHAR(128) NOT NULL,
    posted_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

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

    write_file("migrations/007_fulfillment_schema.sql", """-- NovaCommerce Fulfillment and Shipments Database Schema
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

CREATE INDEX idx_shipments_order_id ON shipments(order_id);
CREATE INDEX idx_shipments_tracking ON shipments(tracking_number);
""")

    write_file("migrations/008_notification_schema.sql", """-- NovaCommerce Notification Service Database Schema
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
""")

    write_file("migrations/009_analytics_schema.sql", """-- NovaCommerce Analytics & Audit Database Schema
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
""")

if __name__ == "__main__":
    generate_proto()
    generate_migrations()
    print("Protobuf and Migration files generated successfully.")
