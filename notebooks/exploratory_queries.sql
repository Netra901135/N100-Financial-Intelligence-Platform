---------------------------------------------------------
-- Query 1
-- Total Companies
---------------------------------------------------------

SELECT COUNT(*) AS total_companies
FROM companies;

---------------------------------------------------------
-- Query 2
-- Total Profit & Loss Records
---------------------------------------------------------

SELECT COUNT(*) AS total_profit_rows
FROM profitandloss;

---------------------------------------------------------
-- Query 3
-- Total Balance Sheet Records
---------------------------------------------------------

SELECT COUNT(*) AS total_balance_rows
FROM balancesheet;

---------------------------------------------------------
-- Query 4
-- Total Cash Flow Records
---------------------------------------------------------

SELECT COUNT(*) AS total_cashflow_rows
FROM cashflow;

---------------------------------------------------------
-- Query 5
-- Companies having more than 10 years of data
---------------------------------------------------------

SELECT
company_id,
COUNT(DISTINCT year) AS years
FROM profitandloss
GROUP BY company_id
ORDER BY years DESC;

---------------------------------------------------------
-- Query 6
-- Top 10 Companies by Average Net Profit
---------------------------------------------------------

SELECT
company_id,
ROUND(AVG(net_profit),2) AS avg_profit
FROM profitandloss
GROUP BY company_id
ORDER BY avg_profit DESC
LIMIT 10;

---------------------------------------------------------
-- Query 7
-- Highest Stock Price
---------------------------------------------------------

SELECT
company_id,
MAX(close_price) AS highest_price
FROM stock_prices
GROUP BY company_id
ORDER BY highest_price DESC
LIMIT 10;

---------------------------------------------------------
-- Query 8
-- Companies by Sector
---------------------------------------------------------

SELECT
broad_sector,
COUNT(*)
FROM sectors
GROUP BY broad_sector
ORDER BY COUNT(*) DESC;

---------------------------------------------------------
-- Query 9
-- Latest Annual Reports
---------------------------------------------------------

SELECT
company_id,
MAX(year) AS latest_report
FROM documents
GROUP BY company_id;

---------------------------------------------------------
-- Query 10
-- Foreign Key Check
---------------------------------------------------------

PRAGMA foreign_key_check;