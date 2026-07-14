PRAGMA foreign_keys = ON;

-- ==========================================
-- COMPANIES
-- ==========================================
CREATE TABLE IF NOT EXISTS companies (

    id TEXT PRIMARY KEY,

    company_logo TEXT,

    company_name TEXT,

    chart_link TEXT,

    about_company TEXT,

    website TEXT,

    nse_profile TEXT,

    bse_profile TEXT,

    face_value REAL,

    book_value REAL,

    roce_percentage REAL,

    roe_percentage REAL

);
-- ==========================================
-- PROFIT & LOSS
-- ==========================================

CREATE TABLE IF NOT EXISTS profitandloss (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    year INTEGER,
    sales REAL,
    expenses REAL,
    operating_profit REAL,
    operating_profit_margin REAL,
    other_income REAL,
    interest REAL,
    depreciation REAL,
    profit_before_tax REAL,
    tax_percentage REAL,
    net_profit REAL,
    eps REAL,
    dividend_payout REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)
);

-- ==========================================
-- BALANCE SHEET
-- ==========================================

CREATE TABLE IF NOT EXISTS balancesheet (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    year INTEGER,

    equity_capital REAL,

    reserves REAL,

    borrowings REAL,

    other_liabilities REAL,

    total_liabilities REAL,

    fixed_assets REAL,

    cwip REAL,

    investments REAL,

    other_asset REAL,

    total_assets REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);

-- ==========================================
-- CASHFLOW
-- ==========================================

CREATE TABLE IF NOT EXISTS cashflow (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    year INTEGER,

    operating_activity REAL,

    investing_activity REAL,

    financing_activity REAL,

    net_cash_flow REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);

-- ==========================================
-- ANALYSIS
-- ==========================================

CREATE TABLE IF NOT EXISTS analysis (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    compounded_sales_growth TEXT,

    compounded_profit_growth TEXT,

    stock_price_cagr TEXT,

    roe TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);

-- ==========================================
-- DOCUMENTS
-- ==========================================

CREATE TABLE IF NOT EXISTS documents (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    year INTEGER,

    annual_report TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);

-- ==========================================
-- PROS & CONS
-- ==========================================

CREATE TABLE IF NOT EXISTS prosandcons (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    pros TEXT,

    cons TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);

-- ==========================================
-- SECTORS
-- ==========================================

CREATE TABLE IF NOT EXISTS sectors (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    broad_sector TEXT,

    sub_sector TEXT,

    index_weight_pct REAL,

    market_cap_category TEXT,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);

-- ==========================================
-- STOCK PRICES
-- ==========================================

CREATE TABLE IF NOT EXISTS stock_prices (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    date DATE,

    open_price REAL,

    high_price REAL,

    low_price REAL,

    close_price REAL,

    volume INTEGER,

    adjusted_close REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);

-- ==========================================
-- FINANCIAL RATIOS
-- ==========================================

CREATE TABLE IF NOT EXISTS financial_ratios (

    id INTEGER PRIMARY KEY,

    company_id TEXT NOT NULL,

    year INTEGER,

    net_profit_margin_pct REAL,

    operating_profit_margin_pct REAL,

    return_on_equity_pct REAL,

    return_on_capital_employed_pct REAL,

    debt_to_equity REAL,

    interest_coverage REAL,

    current_ratio REAL,

    book_value_per_share REAL,

    earnings_yield REAL,

    dividend_payout_ratio_pct REAL,

    total_debt_cr REAL,

    cash_from_operations_cr REAL,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);

-- ==========================================
-- PEER GROUPS
-- ==========================================

CREATE TABLE IF NOT EXISTS peer_groups (

    id INTEGER PRIMARY KEY,

    peer_group_name TEXT,

    company_id TEXT,

    is_benchmark BOOLEAN,

    FOREIGN KEY(company_id)
        REFERENCES companies(id)

);