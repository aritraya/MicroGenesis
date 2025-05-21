-- Technical/Layered Inventory Management System Database Schema
-- Traditional layered architecture (controller, service, repository)

-- Product schema
CREATE TABLE products (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    sku VARCHAR(50) NOT NULL UNIQUE,
    category VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    minimum_stock_level INT NOT NULL DEFAULT 0,
    reorder_quantity INT NOT NULL DEFAULT 0,
    lead_time_days INT NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

-- Product dimensions (one-to-one relationship)
CREATE TABLE product_dimensions (
    product_id BIGINT PRIMARY KEY,
    length DECIMAL(10, 2),
    width DECIMAL(10, 2),
    height DECIMAL(10, 2),
    weight_kg DECIMAL(10, 2),
    CONSTRAINT fk_product_dimensions FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
);

-- Warehouse schema
CREATE TABLE warehouses (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'USA',
    contact_name VARCHAR(100),
    contact_email VARCHAR(255),
    contact_phone VARCHAR(20),
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

-- Inventory schema (product in warehouse)
CREATE TABLE inventory (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    warehouse_id BIGINT NOT NULL,
    quantity INT NOT NULL DEFAULT 0,
    location VARCHAR(50),
    last_counted_at TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_inventory_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_inventory_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(id) ON DELETE CASCADE,
    CONSTRAINT uk_product_warehouse UNIQUE (product_id, warehouse_id)
);

-- Inventory transactions history
CREATE TABLE inventory_transactions (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    warehouse_id BIGINT NOT NULL,
    quantity_change INT NOT NULL,
    new_quantity INT NOT NULL,
    transaction_type VARCHAR(50) NOT NULL, -- ADJUSTMENT, PURCHASE_ORDER, SALES_ORDER, TRANSFER
    reference_id BIGINT,
    reference_type VARCHAR(50),
    notes TEXT,
    transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    CONSTRAINT fk_inventory_transaction_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_inventory_transaction_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- Supplier schema
CREATE TABLE suppliers (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    contact_name VARCHAR(100),
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    street VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    postal_code VARCHAR(20),
    country VARCHAR(100) DEFAULT 'USA',
    payment_terms VARCHAR(50),
    lead_time_days INT DEFAULT 0,
    minimum_order_value DECIMAL(10, 2) DEFAULT 0.00,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL
);

-- Product supplier relationship (many-to-many)
CREATE TABLE product_suppliers (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    supplier_id BIGINT NOT NULL,
    supplier_sku VARCHAR(50),
    cost DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    is_preferred BOOLEAN NOT NULL DEFAULT FALSE,
    lead_time_days INT DEFAULT 0,
    minimum_order_quantity INT DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_product_supplier_product FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    CONSTRAINT fk_product_supplier_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(id) ON DELETE CASCADE,
    CONSTRAINT uk_product_supplier UNIQUE (product_id, supplier_id)
);

-- Purchase order schema
CREATE TABLE purchase_orders (
    id BIGSERIAL PRIMARY KEY,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    supplier_id BIGINT NOT NULL,
    warehouse_id BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'DRAFT', -- DRAFT, SUBMITTED, APPROVED, SHIPPED, RECEIVED, CANCELLED
    order_date DATE NOT NULL,
    expected_delivery_date DATE,
    received_date DATE,
    total_cost DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    CONSTRAINT fk_purchase_order_supplier FOREIGN KEY (supplier_id) REFERENCES suppliers(id),
    CONSTRAINT fk_purchase_order_warehouse FOREIGN KEY (warehouse_id) REFERENCES warehouses(id)
);

-- Purchase order item schema
CREATE TABLE purchase_order_items (
    id BIGSERIAL PRIMARY KEY,
    purchase_order_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    quantity INT NOT NULL,
    unit_cost DECIMAL(10, 2) NOT NULL,
    received_quantity INT NOT NULL DEFAULT 0,
    notes TEXT,
    CONSTRAINT fk_purchase_order_item_po FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(id) ON DELETE CASCADE,
    CONSTRAINT fk_purchase_order_item_product FOREIGN KEY (product_id) REFERENCES products(id)
);

-- Receiving schema for purchase orders
CREATE TABLE purchase_order_receipts (
    id BIGSERIAL PRIMARY KEY,
    purchase_order_id BIGINT NOT NULL,
    receipt_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    CONSTRAINT fk_receipt_purchase_order FOREIGN KEY (purchase_order_id) REFERENCES purchase_orders(id) ON DELETE CASCADE
);

-- Receipt item schema
CREATE TABLE purchase_receipt_items (
    id BIGSERIAL PRIMARY KEY,
    receipt_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    purchase_order_item_id BIGINT NOT NULL,
    received_quantity INT NOT NULL,
    location VARCHAR(50),
    notes TEXT,
    CONSTRAINT fk_receipt_item_receipt FOREIGN KEY (receipt_id) REFERENCES purchase_order_receipts(id) ON DELETE CASCADE,
    CONSTRAINT fk_receipt_item_product FOREIGN KEY (product_id) REFERENCES products(id),
    CONSTRAINT fk_receipt_item_po_item FOREIGN KEY (purchase_order_item_id) REFERENCES purchase_order_items(id)
);

-- User schema
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    role VARCHAR(20) NOT NULL DEFAULT 'USER', -- ADMIN, MANAGER, USER, READONLY
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    last_login TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Audit log schema
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(50) NOT NULL,
    entity_id BIGINT NOT NULL,
    action VARCHAR(20) NOT NULL, -- CREATE, UPDATE, DELETE
    user_id BIGINT,
    username VARCHAR(50) NOT NULL,
    old_values JSONB,
    new_values JSONB,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_audit_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

-- Create indexes for better query performance
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_inventory_warehouse ON inventory(warehouse_id);
CREATE INDEX idx_inventory_qty ON inventory(quantity) WHERE quantity <= 5;
CREATE INDEX idx_inventory_transactions_product ON inventory_transactions(product_id);
CREATE INDEX idx_inventory_transactions_date ON inventory_transactions(transaction_date);
CREATE INDEX idx_purchase_orders_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_purchase_orders_status ON purchase_orders(status);
CREATE INDEX idx_purchase_orders_date ON purchase_orders(order_date);
CREATE INDEX idx_suppliers_name ON suppliers(name);
CREATE INDEX idx_suppliers_active ON suppliers(is_active);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_audit_entity ON audit_logs(entity_type, entity_id);
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp);

-- Create views for common queries
CREATE VIEW vw_inventory_summary AS
SELECT 
    p.id AS product_id,
    p.name AS product_name,
    p.sku AS product_sku,
    p.category,
    p.minimum_stock_level,
    p.reorder_quantity,
    COALESCE(SUM(i.quantity), 0) AS total_quantity,
    COUNT(DISTINCT i.warehouse_id) AS warehouse_count,
    CASE 
        WHEN COALESCE(SUM(i.quantity), 0) <= 0 THEN 'OUT_OF_STOCK'
        WHEN COALESCE(SUM(i.quantity), 0) < p.minimum_stock_level THEN 'LOW_STOCK'
        ELSE 'OK'
    END AS status
FROM 
    products p
LEFT JOIN 
    inventory i ON p.id = i.product_id
WHERE 
    p.is_active = TRUE
GROUP BY 
    p.id, p.name, p.sku, p.category, p.minimum_stock_level, p.reorder_quantity;

CREATE VIEW vw_product_suppliers_info AS
SELECT 
    ps.product_id,
    p.name AS product_name,
    p.sku AS product_sku,
    ps.supplier_id,
    s.name AS supplier_name,
    ps.supplier_sku,
    ps.cost,
    ps.is_preferred,
    COALESCE(ps.lead_time_days, s.lead_time_days) AS lead_time_days
FROM 
    product_suppliers ps
JOIN 
    products p ON ps.product_id = p.id
JOIN 
    suppliers s ON ps.supplier_id = s.id
WHERE
    p.is_active = TRUE AND s.is_active = TRUE;

CREATE VIEW vw_inventory_value AS
SELECT 
    w.id AS warehouse_id,
    w.name AS warehouse_name,
    p.category,
    SUM(i.quantity) AS total_quantity,
    SUM(i.quantity * p.cost) AS total_cost_value,
    SUM(i.quantity * p.price) AS total_retail_value
FROM 
    inventory i
JOIN 
    products p ON i.product_id = p.id
JOIN 
    warehouses w ON i.warehouse_id = w.id
WHERE
    p.is_active = TRUE
GROUP BY 
    w.id, w.name, p.category;

-- Create functions/procedures for common operations
CREATE OR REPLACE FUNCTION adjust_inventory(
    p_product_id BIGINT, 
    p_warehouse_id BIGINT, 
    p_quantity_change INT, 
    p_transaction_type VARCHAR, 
    p_reference_id BIGINT, 
    p_reference_type VARCHAR, 
    p_notes TEXT,
    p_username VARCHAR
) RETURNS VOID AS $$
DECLARE
    v_current_qty INT;
    v_new_qty INT;
BEGIN
    -- Get current quantity
    SELECT COALESCE(quantity, 0) INTO v_current_qty
    FROM inventory
    WHERE product_id = p_product_id AND warehouse_id = p_warehouse_id;
    
    -- Calculate new quantity
    v_new_qty := v_current_qty + p_quantity_change;
    
    -- Update or insert inventory record
    IF v_current_qty IS NULL THEN
        INSERT INTO inventory(product_id, warehouse_id, quantity, updated_at)
        VALUES(p_product_id, p_warehouse_id, p_quantity_change, CURRENT_TIMESTAMP);
    ELSE
        UPDATE inventory 
        SET quantity = v_new_qty, updated_at = CURRENT_TIMESTAMP
        WHERE product_id = p_product_id AND warehouse_id = p_warehouse_id;
    END IF;
    
    -- Record the transaction
    INSERT INTO inventory_transactions(
        product_id, warehouse_id, quantity_change, new_quantity, 
        transaction_type, reference_id, reference_type, notes, created_by
    ) VALUES (
        p_product_id, p_warehouse_id, p_quantity_change, v_new_qty, 
        p_transaction_type, p_reference_id, p_reference_type, p_notes, p_username
    );
END;
$$ LANGUAGE plpgsql;
