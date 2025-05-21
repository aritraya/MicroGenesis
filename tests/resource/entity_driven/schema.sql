-- Entity-Driven Design Database Schema for Banking System
-- Centered around data entities and their relationships

-- Customer entity - stores customer information
CREATE TABLE customers (
    id UUID PRIMARY KEY,
    customer_number VARCHAR(20) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_number VARCHAR(20),
    date_of_birth DATE NOT NULL,
    tax_id VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Customer address entity - related to customers
CREATE TABLE customer_addresses (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    address_type VARCHAR(20) NOT NULL DEFAULT 'PRIMARY', -- PRIMARY, MAILING, WORK, etc.
    street VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL DEFAULT 'USA',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_customer_address FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Account entity - stores account information
CREATE TABLE accounts (
    id UUID PRIMARY KEY,
    account_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id UUID NOT NULL,
    account_type VARCHAR(20) NOT NULL, -- CHECKING, SAVINGS, CREDIT, LOAN, INVESTMENT
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    current_balance DECIMAL(16, 2) NOT NULL DEFAULT 0.00,
    available_balance DECIMAL(16, 2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    interest_rate DECIMAL(6, 4), -- Applicable for savings, loans, etc.
    overdraft_limit DECIMAL(16, 2) DEFAULT 0.00,
    minimum_balance DECIMAL(16, 2) DEFAULT 0.00,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_account_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Transaction entity - stores banking transactions
CREATE TABLE transactions (
    id UUID PRIMARY KEY,
    transaction_number VARCHAR(30) UNIQUE NOT NULL,
    account_id UUID NOT NULL,
    target_account_id UUID,
    transaction_type VARCHAR(20) NOT NULL, -- DEPOSIT, WITHDRAWAL, TRANSFER, PAYMENT, FEE, INTEREST, ADJUSTMENT
    amount DECIMAL(16, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED', -- PENDING, COMPLETED, FAILED, REVERSED
    description VARCHAR(255),
    reference_number VARCHAR(50),
    transaction_date TIMESTAMP NOT NULL,
    running_balance DECIMAL(16, 2),
    card_id UUID,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_transaction_account FOREIGN KEY (account_id) REFERENCES accounts(id),
    CONSTRAINT fk_transaction_target_account FOREIGN KEY (target_account_id) REFERENCES accounts(id)
);

-- Card entity - stores payment card information
CREATE TABLE cards (
    id UUID PRIMARY KEY,
    card_number VARCHAR(30) NOT NULL,
    card_type VARCHAR(20) NOT NULL, -- DEBIT, CREDIT, PREPAID
    customer_id UUID NOT NULL,
    account_id UUID NOT NULL,
    name_on_card VARCHAR(100) NOT NULL,
    expiration_date VARCHAR(5) NOT NULL, -- MM/YY format
    cvv VARCHAR(4) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE', -- ACTIVE, INACTIVE, EXPIRED, BLOCKED
    credit_limit DECIMAL(16, 2), -- For credit cards only
    available_credit DECIMAL(16, 2), -- For credit cards only
    issued_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_card_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_card_account FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- Loan entity - stores loan information
CREATE TABLE loans (
    id UUID PRIMARY KEY,
    loan_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id UUID NOT NULL,
    account_id UUID NOT NULL,
    loan_type VARCHAR(30) NOT NULL, -- PERSONAL, MORTGAGE, AUTO, STUDENT, BUSINESS
    amount DECIMAL(16, 2) NOT NULL,
    outstanding_amount DECIMAL(16, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    interest_rate DECIMAL(6, 4) NOT NULL,
    term_months INT NOT NULL,
    payment_frequency VARCHAR(20) NOT NULL DEFAULT 'MONTHLY', -- WEEKLY, BIWEEKLY, MONTHLY
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    origination_date DATE NOT NULL,
    maturity_date DATE NOT NULL,
    next_payment_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_loan_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_loan_account FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- Loan payment entity - stores loan payment history
CREATE TABLE loan_payments (
    id UUID PRIMARY KEY,
    loan_id UUID NOT NULL,
    transaction_id UUID,
    payment_date DATE NOT NULL,
    amount DECIMAL(16, 2) NOT NULL,
    principal_amount DECIMAL(16, 2) NOT NULL,
    interest_amount DECIMAL(16, 2) NOT NULL,
    outstanding_balance DECIMAL(16, 2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED', -- PENDING, COMPLETED, FAILED
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_payment_loan FOREIGN KEY (loan_id) REFERENCES loans(id),
    CONSTRAINT fk_payment_transaction FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);

-- Investment entity - stores investment information
CREATE TABLE investments (
    id UUID PRIMARY KEY,
    investment_number VARCHAR(20) UNIQUE NOT NULL,
    customer_id UUID NOT NULL,
    account_id UUID NOT NULL,
    investment_type VARCHAR(30) NOT NULL, -- STOCK, BOND, MUTUAL_FUND, ETF, CD, IRA, 401K
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    value_amount DECIMAL(16, 2) NOT NULL,
    cost_basis DECIMAL(16, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    acquisition_date DATE NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_investment_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_investment_account FOREIGN KEY (account_id) REFERENCES accounts(id)
);

-- Security holdings - stores individual security positions
CREATE TABLE security_holdings (
    id UUID PRIMARY KEY,
    investment_id UUID NOT NULL,
    security_symbol VARCHAR(20) NOT NULL,
    security_name VARCHAR(100) NOT NULL,
    quantity DECIMAL(16, 6) NOT NULL,
    purchase_price DECIMAL(16, 2) NOT NULL,
    current_price DECIMAL(16, 2) NOT NULL,
    purchase_date DATE NOT NULL,
    last_updated_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_holding_investment FOREIGN KEY (investment_id) REFERENCES investments(id)
);

-- Beneficiary entity - stores beneficiary information
CREATE TABLE beneficiaries (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    account_id UUID NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    relationship VARCHAR(50) NOT NULL,
    percentage DECIMAL(5, 2) NOT NULL,
    contact_information VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_beneficiary_customer FOREIGN KEY (customer_id) REFERENCES customers(id),
    CONSTRAINT fk_beneficiary_account FOREIGN KEY (account_id) REFERENCES accounts(id),
    CONSTRAINT check_percentage CHECK (percentage > 0 AND percentage <= 100)
);

-- Authentication entity - stores user authentication information
CREATE TABLE authentication (
    id UUID PRIMARY KEY,
    customer_id UUID UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    last_login TIMESTAMP,
    failed_attempts INT NOT NULL DEFAULT 0,
    locked_until TIMESTAMP,
    recovery_email VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_auth_customer FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- Security question entity - stores security questions for password recovery
CREATE TABLE security_questions (
    id UUID PRIMARY KEY,
    authentication_id UUID NOT NULL,
    question VARCHAR(255) NOT NULL,
    answer_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_question_auth FOREIGN KEY (authentication_id) REFERENCES authentication(id)
);

-- MFA entity - stores multi-factor authentication settings
CREATE TABLE mfa_settings (
    id UUID PRIMARY KEY,
    authentication_id UUID NOT NULL,
    method VARCHAR(20) NOT NULL, -- SMS, EMAIL, APP
    identifier VARCHAR(255) NOT NULL, -- phone number, email, or app identifier
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mfa_auth FOREIGN KEY (authentication_id) REFERENCES authentication(id)
);

-- Create necessary indexes for query performance
CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_name ON customers(last_name, first_name);
CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_accounts_number ON accounts(account_number);
CREATE INDEX idx_transactions_account ON transactions(account_id);
CREATE INDEX idx_transactions_date ON transactions(transaction_date);
CREATE INDEX idx_transactions_type ON transactions(transaction_type);
CREATE INDEX idx_cards_customer ON cards(customer_id);
CREATE INDEX idx_cards_account ON cards(account_id);
CREATE INDEX idx_loans_customer ON loans(customer_id);
CREATE INDEX idx_investments_customer ON investments(customer_id);
CREATE INDEX idx_authentication_username ON authentication(username);
CREATE INDEX idx_beneficiaries_account ON beneficiaries(account_id);
