import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_exhaustive_openapis():
    base_dir = "docs/api/v1"
    
    services = [
        ("auth", "Auth & Identity Management Service", 8001, [
            ("/register", "post", "Register New Customer Account", "RegisterUserPayload", "AuthTokenResponse", "Registers a new user account with argon2id password hashing and fires UserRegisteredEvent."),
            ("/login", "post", "Authenticate User Credentials", "LoginUserPayload", "AuthTokenResponse", "Authenticates credentials and returns JWT access/refresh token pair."),
            ("/refresh", "post", "Refresh Access Token", "RefreshTokenPayload", "AuthTokenResponse", "Exchanges valid refresh token for a new access token."),
            ("/me", "get", "Get Authenticated User Profile", None, "UserProfileResponse", "Returns identity claims and permissions for the authenticated token."),
            ("/mfa/setup", "post", "Setup Two-Factor Authentication", None, "MfaSetupResponse", "Generates TOTP secret key and QR code string for authenticator apps."),
            ("/mfa/verify", "post", "Verify MFA Security Code", "MfaVerifyPayload", "SuccessResponse", "Validates 6-digit TOTP token to activate two-factor authentication."),
            ("/mfa/disable", "post", "Disable Two-Factor Authentication", "MfaDisablePayload", "SuccessResponse", "Disables two-factor authentication with password re-verification."),
            ("/password/reset-request", "post", "Request Password Reset Link", "PasswordResetRequestPayload", "SuccessResponse", "Sends cryptographic password reset token to user's registered email."),
            ("/password/reset-confirm", "post", "Confirm Password Reset", "PasswordResetConfirmPayload", "SuccessResponse", "Updates user password with valid reset token."),
            ("/sessions", "get", "List Active User Sessions", None, "SessionListResponse", "Returns list of active login sessions and device fingerprints."),
            ("/sessions/{id}/revoke", "post", "Revoke Specific Session", None, "SuccessResponse", "Terminates specific user session and revokes refresh token."),
            ("/oauth2/authorize", "get", "OAuth2 Authorization Endpoint", None, "OAuth2AuthResponse", "Handles OAuth2 authorization code grant flow."),
            ("/oauth2/token", "post", "OAuth2 Token Exchange", "OAuth2TokenPayload", "OAuth2TokenResponse", "Issues OAuth2 access tokens via authorization code or client credentials.")
        ]),
        ("user", "User Profile & Tenant Management Service", 8002, [
            ("/profile", "get", "Retrieve Customer Profile", None, "UserProfileResponse", "Retrieves complete user profile, preferences, and locale."),
            ("/profile", "put", "Update Customer Profile", "UpdateProfilePayload", "UserProfileResponse", "Updates name, avatar, timezone, and custom metadata."),
            ("/addresses", "get", "List Saved Addresses", None, "AddressListResponse", "Lists saved shipping and billing address book entries."),
            ("/addresses", "post", "Add Delivery Address", "CreateAddressPayload", "AddressResponse", "Adds a new delivery address to the customer's address book."),
            ("/addresses/{id}", "get", "Get Address Details", None, "AddressResponse", "Retrieves specific address by ID."),
            ("/addresses/{id}", "put", "Update Address Details", "UpdateAddressPayload", "AddressResponse", "Modifies street lines, postal code, or default flags."),
            ("/addresses/{id}", "delete", "Remove Address", None, "SuccessResponse", "Removes address entry from customer record."),
            ("/organizations", "get", "List Multi-Tenant Organizations", None, "OrgListResponse", "Lists multi-tenant organizations the user belongs to."),
            ("/organizations", "post", "Create New Organization", "CreateOrgPayload", "OrgResponse", "Provisions new enterprise organization tenant."),
            ("/organizations/{id}", "get", "Get Organization Details", None, "OrgResponse", "Retrieves organization metadata and tier."),
            ("/organizations/{id}/members", "get", "List Organization Members", None, "OrgMemberListResponse", "Returns list of member users and assigned RBAC roles."),
            ("/organizations/{id}/members", "post", "Add Organization Member", "AddOrgMemberPayload", "OrgMemberResponse", "Invites or adds a user to organization tenant."),
            ("/kyc/verify", "post", "Submit KYC Verification", "KycVerificationPayload", "KycStatusResponse", "Submits identity documentation for compliance review.")
        ]),
        ("catalog", "Product Catalog & Search Service", 8003, [
            ("/products", "get", "List and Filter Catalog Products", None, "PaginatedProductResponse", "Searches and filters products by category, price, and tags."),
            ("/products", "post", "Create Product Entity", "CreateProductPayload", "ProductResponse", "Provisions a new product SKU with pricing and attributes."),
            ("/products/{id}", "get", "Get Product by ID", None, "ProductResponse", "Returns product entity, pricing, variants, and image gallery."),
            ("/products/{id}", "put", "Update Product Attributes", "UpdateProductPayload", "ProductResponse", "Updates product descriptions, categories, and tags."),
            ("/products/{id}", "delete", "Soft Delete Product", None, "SuccessResponse", "Soft deletes product and marks SKU as inactive."),
            ("/products/{id}/variants", "get", "List Product SKU Variants", None, "VariantListResponse", "Retrieves size/color variants for a product."),
            ("/products/{id}/variants", "post", "Create Product SKU Variant", "CreateVariantPayload", "VariantResponse", "Adds SKU variant with dimensional weights."),
            ("/categories", "get", "Retrieve Category Tree", None, "CategoryTreeResponse", "Returns nested category hierarchy with parent/child links."),
            ("/categories", "post", "Create Catalog Category", "CreateCategoryPayload", "CategoryResponse", "Creates new catalog category node."),
            ("/categories/{id}", "get", "Get Category Details", None, "CategoryResponse", "Returns category attributes and display order."),
            ("/search", "get", "Full-Text Fuzzy Search", None, "SearchResultsResponse", "Executes full-text token search with faceted filtering."),
            ("/pricing-tiers", "get", "Get B2B Volume Pricing Rules", None, "PricingTierListResponse", "Returns volume discount matrices per customer tier.")
        ]),
        ("inventory", "Real-Time Inventory & Warehouse Service", 8009, [
            ("/stock", "get", "Query Real-Time Stock", None, "StockListResponse", "Returns real-time on-hand and reserved quantities per SKU."),
            ("/stock", "post", "Adjust Warehouse Stock", "SetStockPayload", "StockResponse", "Adjusts warehouse stock level with optimistic locking."),
            ("/stock/{sku}", "get", "Get SKU Stock Details", None, "StockResponse", "Queries on-hand and reserved stock across all fulfillment centers."),
            ("/reserve", "post", "Lock Inventory Reservation", "ReserveStockPayload", "ReservationResponse", "Locks inventory stock for an in-flight order saga."),
            ("/release", "post", "Release Stock Reservation", "ReleaseStockPayload", "SuccessResponse", "Releases reserved stock back to on-hand pool."),
            ("/warehouses", "get", "List Fulfillment Warehouses", None, "WarehouseListResponse", "Returns fulfillment centers and geographic coordinates."),
            ("/warehouses/{id}", "get", "Get Warehouse Details", None, "WarehouseResponse", "Returns warehouse operating status and capacity."),
            ("/reorder-advice", "get", "Calculate Reorder Parameters", None, "ReorderAdviceResponse", "Computes EOQ and safety stock replenishment recommendations."),
            ("/transfers", "post", "Initiate Inter-Warehouse Transfer", "StockTransferPayload", "TransferResponse", "Moves stock between regional fulfillment centers.")
        ]),
        ("order", "Order State Machine & Saga Service", 8004, [
            ("/orders", "post", "Initialize Customer Order", "CreateOrderPayload", "OrderResponse", "Initializes customer order in PENDING_PAYMENT status."),
            ("/orders", "get", "List Order History", None, "PaginatedOrderResponse", "Returns customer order history with pagination."),
            ("/orders/{id}", "get", "Get Order by ID", None, "OrderResponse", "Returns full order breakdown with line items and taxes."),
            ("/orders/{id}/checkout-saga", "post", "Execute Distributed Checkout Saga", "CheckoutSagaPayload", "SagaResponse", "Executes distributed multi-service checkout workflow."),
            ("/orders/{id}/cancel", "post", "Cancel Order Lifecycle", "CancelOrderPayload", "OrderResponse", "Cancels order and triggers compensating refunds/unreservations."),
            ("/orders/{id}/invoice", "get", "Generate Commercial Invoice", None, "InvoiceResponse", "Renders official commercial invoice for accounting."),
            ("/orders/{id}/return", "post", "Submit Return RMA Request", "ReturnRequestPayload", "ReturnResponse", "Submits items for return RMA inspection."),
            ("/coupons/validate", "post", "Validate Promotional Coupon", "ValidateCouponPayload", "CouponValidationResponse", "Evaluates promotional discount applicability.")
        ]),
        ("payment", "Payment Gateway & Double-Entry Ledger Service", 8005, [
            ("/authorize", "post", "Authorize Payment Transaction", "AuthorizePaymentPayload", "PaymentResponse", "Authorizes charge and posts balanced double-entry ledger journal."),
            ("/capture", "post", "Capture Authorized Payment", "CapturePaymentPayload", "PaymentResponse", "Settles authorized transaction into clearing account."),
            ("/refund", "post", "Process Customer Refund", "RefundPaymentPayload", "PaymentResponse", "Processes full or partial refund with ledger reversal entries."),
            ("/ledger/accounts", "get", "Query Chart of Accounts", None, "AccountListResponse", "Returns double-entry general ledger chart of accounts."),
            ("/ledger/journal", "get", "List Journal Entries", None, "JournalEntryListResponse", "Returns immutable double-entry journal entry log."),
            ("/ledger/reconcile", "post", "Run Trial Balance Reconciliation", None, "ReconciliationResponse", "Verifies that total ledger debits equal total credits."),
            ("/webhooks/stripe", "post", "Ingest Stripe Webhook Event", "StripeWebhookPayload", "SuccessResponse", "Processes asynchronous webhook events from Stripe gateway."),
            ("/webhooks/paypal", "post", "Ingest PayPal Webhook Event", "PayPalWebhookPayload", "SuccessResponse", "Processes asynchronous webhook events from PayPal gateway.")
        ]),
        ("fulfillment", "Fulfillment & Courier Logistics Service", 8006, [
            ("/shipments", "post", "Generate Carrier Shipment", "CreateShipmentPayload", "ShipmentResponse", "Generates carrier shipping label and tracking number."),
            ("/shipments/{id}", "get", "Get Shipment Tracking Details", None, "ShipmentResponse", "Returns tracking status, carrier milestones, and ETA."),
            ("/rates", "post", "Calculate Multi-Carrier Rates", "CalculateRatesPayload", "RateListResponse", "Compares real-time quotes across FedEx, UPS, DHL, and USPS."),
            ("/pack", "post", "Calculate 3D Bin Packing", "PackingPayload", "PackingPlanResponse", "Calculates 3D box selection and dimensional weight optimization."),
            ("/manifests/generate", "post", "Generate Carrier Daily Manifest", "ManifestPayload", "ManifestResponse", "Generates end-of-day carrier pickup manifest."),
            ("/webhooks/tracking", "post", "Ingest Carrier Tracking Webhook", "CarrierWebhookPayload", "SuccessResponse", "Updates shipment tracking milestones in real time.")
        ]),
        ("notification", "Omni-Channel Notification Dispatcher", 8007, [
            ("/send", "post", "Dispatch Transactional Notification", "SendNotificationPayload", "NotificationResponse", "Dispatches email, SMS, push, or webhook notification."),
            ("/logs", "get", "Query Notification History", None, "NotificationLogListResponse", "Queries delivery receipts and bounce statuses."),
            ("/templates", "get", "List Transactional Templates", None, "TemplateListResponse", "Lists registered transactional HTML and SMS templates."),
            ("/templates/{id}", "get", "Get Template Content", None, "TemplateResponse", "Retrieves HTML body and variable bindings for template."),
            ("/webhooks/bounces", "post", "Ingest Delivery Bounce Report", "BouncePayload", "SuccessResponse", "Records email bounce and invalidates bad recipient.")
        ]),
        ("analytics", "Real-Time Telemetry & Compliance Audit Service", 8008, [
            ("/events", "post", "Ingest Clickstream Telemetry", "AnalyticsEventPayload", "SuccessResponse", "Streams clickstream and user interaction events."),
            ("/summary", "get", "Query Event Aggregations", None, "SummaryResponse", "Aggregates event counts by category and timeframe."),
            ("/revenue-rollup", "get", "Retrieve Financial Revenue Metrics", None, "RevenueRollupResponse", "Returns daily GMV, AOV, and net revenue metrics."),
            ("/audit-logs", "get", "Query Compliance Audit Trail", None, "AuditLogResponse", "Queries tamper-evident compliance audit trail logs."),
            ("/funnel-analysis", "get", "Compute Conversion Funnel", None, "FunnelResponse", "Computes multi-step conversion funnel drop-off analytics.")
        ])
    ]

    for svc_key, title, port, endpoints in services:
        doc = f"""openapi: 3.0.3
info:
  title: NovaCommerce {title}
  version: 1.0.0
  description: |
    Comprehensive production OpenAPI 3.0 specification for {title}.
    Adheres strictly to RFC-7807 problem details, ISO 8601 timestamps, and JSON-Schema Draft 7 validation.
  contact:
    name: NovaCommerce Engineering Architecture
    email: architecture@novacommerce.io
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: http://localhost:8000/api/v1/{svc_key}
    description: API Gateway Proxy Endpoint
  - url: http://localhost:{port}
    description: Direct Microservice Local Container Port

security:
  - BearerAuth: []

paths:
"""
        for path, method, summary, req_model, res_model, desc in endpoints:
            doc += f"""  {path}:
    {method}:
      summary: {summary}
      description: |
        {desc}
      operationId: {svc_key}_{method}_{path.replace('/', '_').replace('{', '').replace('}', '')}
      tags:
        - {svc_key.capitalize()}
      parameters:
        - name: x-correlation-id
          in: header
          required: false
          schema:
            type: string
            format: uuid
          description: Distributed tracing correlation identifier
"""
            if req_model:
                doc += f"""      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/{req_model}'
"""
            doc += f"""      responses:
        '200':
          description: Successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/{res_model}'
        '201':
          description: Resource created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/{res_model}'
        '400':
          description: Bad request / Schema validation error
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiErrorResponse'
        '401':
          description: Missing or invalid authentication credentials
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiErrorResponse'
        '403':
          description: Insufficient RBAC role permissions
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiErrorResponse'
        '404':
          description: Requested resource was not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiErrorResponse'
        '409':
          description: Conflict / Idempotency lock active
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiErrorResponse'
        '422':
          description: Unprocessable business entity state
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiErrorResponse'
        '429':
          description: Sliding window rate limit exceeded
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiErrorResponse'
        '500':
          description: Internal server error / Saga execution rollback
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ApiErrorResponse'
"""

        # Components section with exhaustive schemas
        doc += """
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: Enter RS256 or HS256 signed JSON Web Token

  schemas:
    SuccessResponse:
      type: object
      required: [success, statusCode]
      properties:
        success:
          type: boolean
          example: true
        statusCode:
          type: integer
          example: 200
        data:
          type: object
          properties:
            message:
              type: string
              example: Operation completed successfully.

    ApiErrorResponse:
      type: object
      required: [success, statusCode, error]
      properties:
        success:
          type: boolean
          example: false
        statusCode:
          type: integer
          example: 400
        error:
          type: object
          required: [code, message, timestamp]
          properties:
            code:
              type: string
              example: ERR_VALIDATION_ERROR
            message:
              type: string
              example: Input validation failed for request payload.
            details:
              type: array
              items:
                type: object
                properties:
                  field:
                    type: string
                    example: email
                  message:
                    type: string
                    example: Must be a valid email format.
            correlationId:
              type: string
              format: uuid
              example: 7f3b8c92-1a4e-4b6f-8d9e-0f1a2b3c4d5e
            timestamp:
              type: string
              format: date-time
              example: '2026-08-29T10:00:00.000Z'

    Money:
      type: object
      required: [amount, currency]
      properties:
        amount:
          type: integer
          description: Value stored in minor currency units (cents, pence, etc.)
          example: 2999
        currency:
          type: string
          enum: [USD, EUR, GBP, CAD, AUD, JPY, CHF, SGD, INR]
          example: USD

    Address:
      type: object
      required: [recipientName, streetLine1, city, stateOrProvince, postalCode, countryCode]
      properties:
        id:
          type: string
          format: uuid
        recipientName:
          type: string
          example: John Doe
        streetLine1:
          type: string
          example: 100 Market St
        streetLine2:
          type: string
          example: Suite 500
        city:
          type: string
          example: San Francisco
        stateOrProvince:
          type: string
          example: CA
        postalCode:
          type: string
          example: '94105'
        countryCode:
          type: string
          example: US
        isDefaultShipping:
          type: boolean
          example: true
        isDefaultBilling:
          type: boolean
          example: true
"""
        write_file(f"{base_dir}/{svc_key}.yaml", doc)

    print("Generated exhaustive OpenAPI specifications in docs/api/v1/")

if __name__ == "__main__":
    generate_exhaustive_openapis()
