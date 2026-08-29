-- =============================================================================
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
