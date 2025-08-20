-- Query 1: Identify transactions with negative or zero amounts
SELECT 
    transaction_id,
    account_id,
    amount,
    transaction_date,
    type
FROM transactions
WHERE amount <= 0
ORDER BY transaction_date DESC;

-- Query 2: Detect transactions linked to non-existent accounts
SELECT 
    t.transaction_id,
    t.account_id,
    t.transaction_date,
    t.type
FROM transactions t
LEFT JOIN accounts a ON t.account_id = a.account_id
WHERE a.account_id IS NULL;

-- Query 3: Find pending transactions older than 24 hours
SELECT 
    transaction_id,
    account_id,
    transaction_date,
    status
FROM transactions
WHERE 
    status = 'PENDING'
    AND transaction_date < NOW() - INTERVAL '24 hours'
ORDER BY transaction_date;

-- Query 4: Summarize transaction issues by type
SELECT 
    type,
    COUNT(*) AS issue_count,
    SUM(amount) AS total_amount
FROM transactions
WHERE 
    amount <= 0 
    OR status = 'PENDING' 
    AND transaction_date < NOW() - INTERVAL '24 hours'
GROUP BY type;
