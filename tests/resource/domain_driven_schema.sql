-- Domain-Driven Design Database Schema for E-commerce System
-- Organized around business domains and bounded contexts

-- Product Catalog Bounded Context
CREATE TABLE categories (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    parent_category_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_parent_category FOREIGN KEY (parent_category_id) REFERENCES categories(id)
);

CREATE TABLE products (
    id UUID PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    sku VARCHAR(50) NOT NULL UNIQUE,
    price_amount DECIMAL(10, 2) NOT NULL,
    price_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    stock_quantity INT NOT NULL DEFAULT 0,
    category_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_category FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE product_details (
    product_id UUID PRIMARY KEY,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_details FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE product_specifications (
    id UUID PRIMARY KEY,
    product_id UUID NOT NULL,
    name VARCHAR(100) NOT NULL,
    value VARCHAR(200) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_specs FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

CREATE TABLE product_images (
    id UUID PRIMARY KEY,
    product_id UUID NOT NULL,
    url VARCHAR(500) NOT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_images FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Customer Bounded Context
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE customer_addresses (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    address_type VARCHAR(20) NOT NULL, -- 'SHIPPING', 'BILLING', 'BOTH'
    street_line1 VARCHAR(255) NOT NULL,
    street_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    is_default BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_customer_address FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE
);

-- Shopping Cart Bounded Context
CREATE TABLE shopping_carts (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cart_customer FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE,
    CONSTRAINT uk_customer_active_cart UNIQUE (customer_id, status)
);

CREATE TABLE cart_items (
    id UUID PRIMARY KEY,
    cart_id UUID NOT NULL,
    product_id UUID NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    price_at_addition DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cart_item_cart FOREIGN KEY (cart_id) REFERENCES shopping_carts(id) ON DELETE CASCADE,
    CONSTRAINT fk_cart_item_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT uk_cart_product UNIQUE (cart_id, product_id)
);

-- Order Bounded Context
CREATE TABLE orders (
    id UUID PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    customer_id UUID NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PLACED',
    subtotal_amount DECIMAL(10, 2) NOT NULL,
    subtotal_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    shipping_cost_amount DECIMAL(10, 2) NOT NULL,
    shipping_cost_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    tax_amount DECIMAL(10, 2) NOT NULL,
    tax_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    total_amount DECIMAL(10, 2) NOT NULL,
    total_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    payment_method VARCHAR(50) NOT NULL,
    shipping_address_line1 VARCHAR(255) NOT NULL,
    shipping_address_line2 VARCHAR(255),
    shipping_city VARCHAR(100) NOT NULL,
    shipping_state VARCHAR(100) NOT NULL,
    shipping_postal_code VARCHAR(20) NOT NULL,
    shipping_country VARCHAR(100) NOT NULL,
    billing_address_line1 VARCHAR(255) NOT NULL,
    billing_address_line2 VARCHAR(255),
    billing_city VARCHAR(100) NOT NULL,
    billing_state VARCHAR(100) NOT NULL,
    billing_postal_code VARCHAR(20) NOT NULL,
    billing_country VARCHAR(100) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY,
    order_id UUID NOT NULL,
    product_id UUID NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price_amount DECIMAL(10, 2) NOT NULL,
    unit_price_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    total_price_amount DECIMAL(10, 2) NOT NULL,
    total_price_currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_item_order FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_order_item_product FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Payment Bounded Context
CREATE TABLE payments (
    id UUID PRIMARY KEY,
    order_id UUID NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    payment_method VARCHAR(50) NOT NULL,
    payment_reference VARCHAR(100),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_order FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Shipping Bounded Context
CREATE TABLE shipments (
    id UUID PRIMARY KEY,
    order_id UUID NOT NULL,
    tracking_number VARCHAR(100),
    carrier VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PREPARING',
    shipped_at TIMESTAMP,
    delivered_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_shipment_order FOREIGN KEY (order_id) REFERENCES orders(id)
);

-- Create necessary indexes
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_status ON products(status);
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_payments_order ON payments(order_id);
CREATE INDEX idx_shipments_order ON shipments(order_id);

-- Domain events table for event sourcing
CREATE TABLE domain_events (
    id UUID PRIMARY KEY,
    aggregate_type VARCHAR(100) NOT NULL,
    aggregate_id UUID NOT NULL,
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    processed_at TIMESTAMP
);

CREATE INDEX idx_domain_events_aggregate ON domain_events(aggregate_type, aggregate_id);
CREATE INDEX idx_domain_events_processed ON domain_events(processed_at) WHERE processed_at IS NULL;
