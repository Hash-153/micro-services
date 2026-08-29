# NovaCommerce Distributed Platform: Enterprise Data Dictionary

## 1. Overview
This technical data dictionary documents every database entity, table, attribute, data type, relational constraint, and index across all ten autonomous microservice databases in the NovaCommerce platform.

---

## 2. Authentication & Identity Database (`novacommerce_auth`)

### 2.1 Table: `users`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Globally unique identifier for user entity |
| `email` | `VARCHAR(255)` | No | None | Unique Index | Normalized lowercase email address for identity |
| `password_hash` | `VARCHAR(255)` | No | None | None | Cryptographic Argon2id password hash |
| `role` | `VARCHAR(50)` | No | `'CUSTOMER'` | FK -> `user_roles.role_key` | Access control role level |
| `status` | `VARCHAR(50)` | No | `'ACTIVE'` | FK -> `account_statuses` | Current lifecycle state of user account |
| `kyc_status` | `VARCHAR(50)` | No | `'NOT_SUBMITTED'` | None | Identity verification compliance status |
| `organization_id` | `UUID` | Yes | `NULL` | None | Associated enterprise multi-tenant tenant ID |
| `is_mfa_enabled` | `BOOLEAN` | No | `FALSE` | None | Flag indicating if TOTP 2FA is enforced |
| `mfa_secret` | `VARCHAR(255)` | Yes | `NULL` | None | Encrypted Base32 TOTP shared secret key |
| `failed_login_attempts`| `INT` | No | `0` | None | Counter for consecutive invalid credentials |
| `locked_until` | `TIMESTAMPTZ` | Yes | `NULL` | None | Expiry timestamp for temporary security lockout |
| `last_login_at` | `TIMESTAMPTZ` | Yes | `NULL` | None | Timestamp of last successful authentication |
| `password_changed_at` | `TIMESTAMPTZ`| No | `NOW()` | None | Timestamp of last password modification |
| `created_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Initial record creation audit timestamp |
| `updated_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Record modification audit timestamp |
| `deleted_at` | `TIMESTAMPTZ` | Yes | `NULL` | None | Soft-delete timestamp |

### 2.2 Table: `user_sessions`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Unique session identifier |
| `user_id` | `UUID` | No | None | FK -> `users.id` ON DELETE CASCADE | Associated user account |
| `refresh_token_hash`| `VARCHAR(255)`| No | None | Unique Index | SHA-256 hash of issued refresh token |
| `ip_address` | `VARCHAR(45)` | Yes | `NULL` | None | Client IP address at session initiation |
| `user_agent` | `VARCHAR(512)`| Yes | `NULL` | None | Client browser/device user agent string |
| `is_revoked` | `BOOLEAN` | No | `FALSE` | None | Invalidation flag for logged-out sessions |
| `revoked_at` | `TIMESTAMPTZ` | Yes | `NULL` | None | Timestamp when session was terminated |
| `expires_at` | `TIMESTAMPTZ` | No | None | Index | Expiration boundary for refresh validity |
| `created_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Session generation timestamp |
| `last_activity_at` | `TIMESTAMPTZ`| No | `NOW()` | None | Last recorded interaction timestamp |

---

## 3. Product Catalog Database (`novacommerce_catalog`)

### 3.1 Table: `products`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Unique product master identifier |
| `sku` | `VARCHAR(64)` | No | None | Unique Index | Master stock keeping unit code |
| `name` | `VARCHAR(255)` | No | None | None | Display title of merchandise |
| `slug` | `VARCHAR(255)` | No | None | Unique Index | SEO-optimized URL path segment |
| `description` | `TEXT` | No | None | None | Rich text product marketing overview |
| `category_id` | `UUID` | No | None | FK -> `categories.id` | Primary category assignment |
| `base_price_cents` | `INT` | No | None | `CHECK (base_price_cents >= 0)` | Standard MSRP in minor currency units |
| `currency` | `CHAR(3)` | No | `'USD'` | None | ISO 4217 3-letter currency code |
| `is_active` | `BOOLEAN` | No | `TRUE` | None | Visibility flag for customer storefront |
| `is_featured` | `BOOLEAN` | No | `FALSE` | None | Featured merchandising placement flag |
| `tags` | `TEXT[]` | No | `'{}'` | GIN Index | Search and merchandising classification tags |
| `attributes` | `JSONB` | No | `'{}'` | GIN Index | Dynamic technical specifications and metadata |
| `created_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Last modification timestamp |
| `deleted_at` | `TIMESTAMPTZ` | Yes | `NULL` | None | Soft-delete timestamp |

### 3.2 Table: `product_variants`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Unique SKU variant identifier |
| `product_id` | `UUID` | No | None | FK -> `products.id` ON DELETE CASCADE | Parent product relationship |
| `sku` | `VARCHAR(64)` | No | None | Unique Index | Specific variant SKU code |
| `name` | `VARCHAR(255)` | No | None | None | Specific variant descriptor |
| `price_modifier_cents`| `INT` | No | `0` | None | Price delta relative to product base price |
| `weight_grams` | `INT` | No | `500` | None | Physical shipping scale weight |
| `length_mm` | `INT` | No | `100` | None | Package physical length |
| `width_mm` | `INT` | No | `100` | None | Package physical width |
| `height_mm` | `INT` | No | `100` | None | Package physical height |
| `options` | `JSONB` | No | `'{}'` | None | Key-value options map (e.g. size, color) |
| `is_active` | `BOOLEAN` | No | `TRUE` | None | Variant availability status |
| `created_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Update timestamp |

---

## 4. Real-Time Inventory Database (`novacommerce_inventory`)

### 4.1 Table: `inventory_stocks`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Stock balance identifier |
| `sku` | `VARCHAR(64)` | No | None | Unique with `warehouse_id` | Product SKU code |
| `warehouse_id` | `UUID` | No | None | FK -> `warehouses.id` | Fulfillment center location |
| `on_hand_quantity` | `INT` | No | `0` | `CHECK (on_hand_quantity >= 0)` | Physical units present in warehouse |
| `reserved_quantity`| `INT` | No | `0` | `CHECK (reserved_quantity >= 0)`| Units locked for in-flight checkout sagas |
| `allocated_quantity`| `INT` | No | `0` | `CHECK (allocated_quantity >= 0)`| Units committed for picking and packing |
| `safety_stock_threshold`| `INT` | No | `5` | None | Low stock alert trigger boundary |
| `reorder_quantity` | `INT` | No | `20` | None | Standard replenishment order batch size |
| `bin_location` | `VARCHAR(50)`| Yes | `NULL` | None | Warehouse aisle/shelf/bin coordinate |
| `version` | `INT` | No | `1` | None | Optimistic locking concurrency counter |
| `updated_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Timestamp of last stock modification |

---

## 5. Order Management Database (`novacommerce_orders`)

### 5.1 Table: `orders`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Unique order identifier |
| `order_number` | `VARCHAR(64)` | No | None | Unique Index | Human-readable order reference code |
| `user_id` | `UUID` | No | None | Index | Customer identity reference |
| `status` | `VARCHAR(50)` | No | `'PENDING_PAYMENT'`| Index | State machine lifecycle status |
| `subtotal_cents` | `INT` | No | None | `CHECK (subtotal_cents >= 0)` | Sum of all line item subtotals |
| `tax_cents` | `INT` | No | `0` | `CHECK (tax_cents >= 0)` | Calculated regional sales/VAT tax |
| `shipping_cents` | `INT` | No | `0` | `CHECK (shipping_cents >= 0)` | Freight and courier delivery charge |
| `discount_cents` | `INT` | No | `0` | `CHECK (discount_cents >= 0)` | Promotional coupon discount deduction |
| `total_cents` | `INT` | No | None | `CHECK (total_cents >= 0)` | Final net settlement amount |
| `currency` | `CHAR(3)` | No | `'USD'` | None | ISO 4217 settlement currency |
| `shipping_address`| `JSONB` | No | None | None | Snapshot of delivery address |
| `billing_address` | `JSONB` | No | None | None | Snapshot of cardholder billing address |
| `coupon_code` | `VARCHAR(50)` | Yes | `NULL` | None | Applied promotional code |
| `payment_id` | `UUID` | Yes | `NULL` | None | Settled payment transaction ID |
| `shipment_id` | `UUID` | Yes | `NULL` | None | Dispatched courier shipment ID |
| `idempotency_key` | `VARCHAR(128)`| No | None | Unique Index | Client UUID preventing duplicate submission |
| `created_at` | `TIMESTAMPTZ` | No | `NOW()` | Index | Order placement timestamp |
| `updated_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Last status update timestamp |

---

## 6. Financial Ledger Database (`novacommerce_payments`)

### 6.1 Table: `ledger_accounts`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Ledger account identifier |
| `account_number` | `VARCHAR(50)` | No | None | Unique Index | Chart of accounts code (e.g. 1010, 4010) |
| `name` | `VARCHAR(150)` | No | None | None | Account descriptive name |
| `type` | `VARCHAR(50)` | No | None | None | Category: ASSET, LIABILITY, EQUITY, REVENUE, EXPENSE |
| `currency` | `CHAR(3)` | No | `'USD'` | None | Accounting denomination currency |
| `balance_cents` | `BIGINT` | No | `0` | None | Current cumulative posted balance |
| `created_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Account creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Balance update timestamp |

### 6.2 Table: `ledger_journal_entries`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Journal entry header identifier |
| `entry_number` | `VARCHAR(64)` | No | None | Unique Index | Sequential journal voucher number |
| `description` | `VARCHAR(255)` | No | None | None | Business memo explaining the entry |
| `transaction_id` | `UUID` | Yes | `NULL` | FK -> `payment_transactions` | Associated payment charge reference |
| `reference_type` | `VARCHAR(50)` | No | None | None | Originating domain entity type |
| `reference_id` | `VARCHAR(128)`| No | None | None | Originating domain entity UUID |
| `posted_at` | `TIMESTAMPTZ` | No | `NOW()` | None | Immutable ledger posting timestamp |

### 6.3 Table: `ledger_lines`
| Column Name | Data Type | Nullable | Default | Constraints / References | Business Description |
|:---|:---|:---|:---|:---|:---|
| `id` | `UUID` | No | `gen_random_uuid()` | Primary Key | Journal entry line identifier |
| `journal_entry_id`| `UUID` | No | None | FK -> `ledger_journal_entries.id` ON DELETE CASCADE | Parent journal entry |
| `account_id` | `UUID` | No | None | FK -> `ledger_accounts.id` | Targeted chart of account |
| `entry_type` | `VARCHAR(10)` | No | None | `CHECK (entry_type IN ('DEBIT', 'CREDIT'))` | Posting direction |
| `amount_cents` | `BIGINT` | No | None | `CHECK (amount_cents > 0)` | Monetary magnitude in cents |
| `memo` | `VARCHAR(255)` | Yes | `NULL` | None | Line-level audit memo |
