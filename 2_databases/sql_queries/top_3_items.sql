SELECT items.id, items.name, COUNT(*) AS total_purchases
FROM items
JOIN transactions
ON items.id = ANY (transactions.item_ids)
GROUP BY items.id, items.name
ORDER BY total_purchases DESC
LIMIT 3;
