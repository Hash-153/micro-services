import os

def ensure_dir(path):
    if path:
        os.makedirs(path, exist_ok=True)

def write_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_full_openapi_specs():
    specs = {
        "auth": ("NovaCommerce Authentication & IAM API", "8001", [
            ("/api/v1/auth/register", "post", "Register User", "RegisterUserRequest", "AuthTokenResponse", "Registers a new user account with argon2id password hashing and fires UserRegisteredEvent."),
            ("/api/v1/auth/login", "post", "User Login", "LoginRequest", "AuthTokenResponse", "Authenticates credentials and returns JWT access/refresh token pair."),
            ("/api/v1/auth/refresh", "post", "Refresh Access Token", "RefreshTokenRequest", "AuthTokenResponse", "Exchanges valid refresh token for a new access token."),
            ("/api/v1/auth/me", "get", "Get Current User", None, "UserProfileResponse", "Returns identity claims and permissions for the authenticated token."),
            ("/api/v1/auth/mfa/enroll", "post", "Enroll in MFA", None, "MfaEnrollResponse", "Generates TOTP secret key and QR code string for authenticator apps."),
            ("/api/v1/auth/mfa/verify", "post", "Verify MFA Code", "MfaVerifyRequest", "SuccessResponse", "Validates 6-digit TOTP token to activate two-factor authentication."),
            ("/api/v1/auth/mfa/disable", "post", "Disable MFA", "MfaDisableRequest", "SuccessResponse", "Disables two-factor authentication with password re-verification."),
            ("/api/v1/auth/password/reset-request", "post", "Request Password Reset", "PasswordResetRequest", "SuccessResponse", "Sends cryptographic password reset token to user's registered email."),
            ("/api/v1/auth/password/reset-confirm", "post", "Confirm Password Reset", "PasswordResetConfirmRequest", "SuccessResponse", "Updates user password with valid reset token."),
            ("/api/v1/auth/sessions", "get", "List Active Sessions", None, "SessionListResponse", "Returns list of active login sessions and device fingerprints."),
            ("/api/v1/auth/sessions/{id}/revoke", "post", "Revoke Session", None, "SuccessResponse", "Terminates specific user session and revokes refresh token.")
        ]),
        "user": ("NovaCommerce User Profile & Multi-Tenancy API", "8002", [
            ("/api/v1/users/profile", "get", "Get User Profile", None, "UserProfileResponse", "Retrieves complete user profile, preferences, and locale."),
            ("/api/v1/users/profile", "put", "Update User Profile", "UpdateProfileRequest", "UserProfileResponse", "Updates name, avatar, timezone, and custom metadata."),
            ("/api/v1/users/addresses", "get", "List Addresses", None, "AddressListResponse", "Lists saved shipping and billing address book entries."),
            ("/api/v1/users/addresses", "post", "Create Address", "CreateAddressRequest", "AddressResponse", "Adds a new delivery address to the customer's address book."),
            ("/api/v1/users/addresses/{id}", "get", "Get Address Details", None, "AddressResponse", "Retrieves specific address by ID."),
            ("/api/v1/users/addresses/{id}", "put", "Update Address", "UpdateAddressRequest", "AddressResponse", "Modifies street lines, postal code, or default flags."),
            ("/api/v1/users/addresses/{id}", "delete", "Delete Address", None, "SuccessResponse", "Removes address entry from customer record."),
            ("/api/v1/users/organizations", "get", "List Organizations", None, "OrgListResponse", "Lists multi-tenant organizations the user belongs to."),
            ("/api/v1/users/organizations", "post", "Create Organization", "CreateOrgRequest", "OrgResponse", "Provisions new enterprise organization tenant."),
            ("/api/v1/users/organizations/{id}/members", "get", "List Organization Members", None, "OrgMemberListResponse", "Returns list of member users and assigned RBAC roles."),
            ("/api/v1/users/organizations/{id}/members", "post", "Add Member", "AddMemberRequest", "OrgMemberResponse", "Invites or adds a user to organization tenant.")
        ]),
        "catalog": ("NovaCommerce Product Catalog & Pricing API", "8003", [
            ("/api/v1/catalog/products", "get", "List Products", None, "PaginatedProductResponse", "Searches and filters products by category, price, and tags."),
            ("/api/v1/catalog/products", "post", "Create Product", "CreateProductRequest", "ProductResponse", "Provisions a new product SKU with pricing and attributes."),
            ("/api/v1/catalog/products/{id}", "get", "Get Product Details", None, "ProductResponse", "Returns product entity, pricing, variants, and image gallery."),
            ("/api/v1/catalog/products/{id}", "put", "Update Product", "UpdateProductRequest", "ProductResponse", "Updates product descriptions, categories, and tags."),
            ("/api/v1/catalog/products/{id}", "delete", "Delete Product", None, "SuccessResponse", "Soft deletes product and marks SKU as inactive."),
            ("/api/v1/catalog/products/{id}/variants", "get", "List Variants", None, "VariantListResponse", "Retrieves size/color variants for a product."),
            ("/api/v1/catalog/products/{id}/variants", "post", "Create Variant", "CreateVariantRequest", "VariantResponse", "Adds SKU variant with dimensional weights."),
            ("/api/v1/catalog/categories", "get", "List Categories", None, "CategoryTreeResponse", "Returns nested category hierarchy with parent/child links."),
            ("/api/v1/catalog/categories", "post", "Create Category", "CreateCategoryRequest", "CategoryResponse", "Creates new catalog category node."),
            ("/api/v1/catalog/search", "get", "Search Catalog", None, "SearchResultsResponse", "Executes full-text token search with faceted filtering.")
        ]),
        "inventory": ("NovaCommerce Inventory & Warehouse API", "8009", [
            ("/api/v1/inventory/stock", "get", "Query Stock Levels", None, "StockListResponse", "Returns real-time on-hand and reserved quantities per SKU."),
            ("/api/v1/inventory/stock", "post", "Update Stock Level", "SetStockRequest", "StockResponse", "Adjusts warehouse stock level with optimistic locking."),
            ("/api/v1/inventory/reserve", "post", "Reserve Stock", "ReserveStockRequest", "ReservationResponse", "Locks inventory stock for an in-flight order saga."),
            ("/api/v1/inventory/release", "post", "Release Reservation", "ReleaseStockRequest", "SuccessResponse", "Releases reserved stock back to on-hand pool."),
            ("/api/v1/inventory/warehouses", "get", "List Warehouses", None, "WarehouseListResponse", "Returns fulfillment centers and geographic coordinates."),
            ("/api/v1/inventory/reorder-advice", "get", "Reorder Forecast", None, "ReorderAdviceResponse", "Computes EOQ and safety stock replenishment recommendations.")
        ]),
        "order": ("NovaCommerce Order Lifecycle & Saga API", "8004", [
            ("/api/v1/orders", "post", "Create Order", "CreateOrderRequest", "OrderResponse", "Initializes customer order in PENDING_PAYMENT status."),
            ("/api/v1/orders", "get", "List Orders", None, "PaginatedOrderResponse", "Returns customer order history with pagination."),
            ("/api/v1/orders/{id}", "get", "Get Order by ID", None, "OrderResponse", "Returns full order breakdown with line items and taxes."),
            ("/api/v1/orders/{id}/checkout-saga", "post", "Execute Checkout Saga", "CheckoutSagaRequest", "SagaResponse", "Executes distributed multi-service checkout workflow."),
            ("/api/v1/orders/{id}/cancel", "post", "Cancel Order", "CancelOrderRequest", "OrderResponse", "Cancels order and triggers compensating refunds/unreservations."),
            ("/api/v1/orders/{id}/invoice", "get", "Get Invoice HTML", None, "InvoiceResponse", "Renders official commercial invoice for accounting."),
            ("/api/v1/orders/{id}/return", "post", "Submit Return Request", "ReturnRequestInput", "ReturnResponse", "Submits items for return RMA inspection.")
        ]),
        "payment": ("NovaCommerce Payments & Financial Ledger API", "8005", [
            ("/api/v1/payments/authorize", "post", "Authorize Payment", "AuthorizePaymentRequest", "PaymentResponse", "Authorizes charge and posts balanced double-entry ledger journal."),
            ("/api/v1/payments/capture", "post", "Capture Payment", "CapturePaymentRequest", "PaymentResponse", "Settles authorized transaction into clearing account."),
            ("/api/v1/payments/refund", "post", "Execute Refund", "RefundPaymentRequest", "PaymentResponse", "Processes full or partial refund with ledger reversal entries."),
            ("/api/v1/payments/ledger/accounts", "get", "Chart of Accounts", None, "AccountListResponse", "Returns double-entry general ledger chart of accounts."),
            ("/api/v1/payments/ledger/journal", "get", "Journal Entries", None, "JournalEntryListResponse", "Returns immutable double-entry journal entry log."),
            ("/api/v1/payments/webhooks/stripe", "post", "Stripe Webhook", "StripeWebhookPayload", "SuccessResponse", "Processes asynchronous webhook events from Stripe gateway.")
        ]),
        "fulfillment": ("NovaCommerce Fulfillment & Carrier Logistics API", "8006", [
            ("/api/v1/fulfillment/shipments", "post", "Create Shipment", "CreateShipmentRequest", "ShipmentResponse", "Generates carrier shipping label and tracking number."),
            ("/api/v1/fulfillment/shipments/{id}", "get", "Get Shipment Details", None, "ShipmentResponse", "Returns tracking status, carrier milestones, and ETA."),
            ("/api/v1/fulfillment/rates", "post", "Calculate Carrier Rates", "CalculateRatesRequest", "RateListResponse", "Compares real-time quotes across FedEx, UPS, DHL, and USPS."),
            ("/api/v1/fulfillment/pack", "post", "Optimize Bin Packing", "PackingRequest", "PackingPlanResponse", "Calculates 3D box selection and dimensional weight optimization.")
        ]),
        "notification": ("NovaCommerce Omni-Channel Notification API", "8007", [
            ("/api/v1/notifications/send", "post", "Send Notification", "SendNotificationRequest", "NotificationResponse", "Dispatches email, SMS, push, or webhook notification."),
            ("/api/v1/notifications/logs", "get", "Notification Logs", None, "NotificationLogListResponse", "Queries delivery receipts and bounce statuses."),
            ("/api/v1/notifications/templates", "get", "List Templates", None, "TemplateListResponse", "Lists registered transactional HTML and SMS templates.")
        ]),
        "analytics": ("NovaCommerce Clickstream & Compliance Audit API", "8008", [
            ("/api/v1/analytics/events", "post", "Ingest Event", "AnalyticsEventInput", "SuccessResponse", "Streams clickstream and user interaction events."),
            ("/api/v1/analytics/summary", "get", "Event Summary", None, "SummaryResponse", "Aggregates event counts by category and timeframe."),
            ("/api/v1/analytics/revenue-rollup", "get", "Revenue Rollup", None, "RevenueRollupResponse", "Returns daily GMV, AOV, and net revenue metrics."),
            ("/api/v1/analytics/audit-logs", "get", "Audit Logs", None, "AuditLogResponse", "Queries tamper-evident compliance audit trail logs.")
        ])
    }

    for svc_key, (title, port, endpoints) in specs.items():
        doc = f"""openapi: 3.0.3
info:
  title: {title}
  version: 1.0.0
  description: |
    Production-grade enterprise OpenAPI 3.0 specification for {title}.
    Adheres strictly to RFC-7807 problem details, ISO 8601 timestamps, and JSON-Schema Draft 7 validation.
  contact:
    name: NovaCommerce Core Platform Engineering
    email: api-platform@novacommerce.io
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: http://localhost:8000
    description: API Gateway Proxy Router
  - url: http://localhost:{port}
    description: Direct Microservice Local Container

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

        # Components section
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
        write_file(f"docs/api/{svc_key}-service.openapi.yaml", doc)

    print("Generated full OpenAPI 3.0 specifications for all services.")

if __name__ == "__main__":
    generate_full_openapi_specs()
