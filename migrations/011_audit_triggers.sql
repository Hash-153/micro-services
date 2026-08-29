-- =============================================================================
-- NovaCommerce Automated Compliance Audit Trail Triggers
-- =============================================================================

CREATE OR REPLACE FUNCTION audit_record_change_trigger()
RETURNS TRIGGER AS $$
DECLARE
    actor_id_val VARCHAR(128);
    action_type VARCHAR(50);
    record_id_val VARCHAR(128);
BEGIN
    action_type := TG_OP;
    
    IF (TG_OP = 'DELETE') THEN
        record_id_val := OLD.id::TEXT;
        INSERT INTO audit_logs (
            id, service_name, action, actor_id, actor_role,
            resource_type, resource_id, changes, timestamp
        ) VALUES (
            gen_random_uuid(), TG_TABLE_NAME, action_type, 'SYSTEM_TRIGGER', 'INTERNAL',
            TG_TABLE_NAME, record_id_val, row_to_json(OLD), NOW()
        );
        RETURN OLD;
    ELSIF (TG_OP = 'UPDATE') THEN
        record_id_val := NEW.id::TEXT;
        INSERT INTO audit_logs (
            id, service_name, action, actor_id, actor_role,
            resource_type, resource_id, changes, timestamp
        ) VALUES (
            gen_random_uuid(), TG_TABLE_NAME, action_type, 'SYSTEM_TRIGGER', 'INTERNAL',
            TG_TABLE_NAME, record_id_val, json_build_object('old', row_to_json(OLD), 'new', row_to_json(NEW)), NOW()
        );
        RETURN NEW;
    ELSIF (TG_OP = 'INSERT') THEN
        record_id_val := NEW.id::TEXT;
        INSERT INTO audit_logs (
            id, service_name, action, actor_id, actor_role,
            resource_type, resource_id, changes, timestamp
        ) VALUES (
            gen_random_uuid(), TG_TABLE_NAME, action_type, 'SYSTEM_TRIGGER', 'INTERNAL',
            TG_TABLE_NAME, record_id_val, row_to_json(NEW), NOW()
        );
        RETURN NEW;
    END IF;
    
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;
