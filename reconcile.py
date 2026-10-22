import json


def parse_amount(amount):
    """Amounts come as numbers or as strings, sometimes with thousands commas."""
    if isinstance(amount, (int, float)):
        return float(amount)
    return float(str(amount).replace(",", ""))



latest = {}

with open("payments.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except ValueError:
            continue  
        if not isinstance(event, dict):
            continue
        txn_id = event.get("txn_id")
        if not txn_id:
            continue  

        current = latest.get(txn_id)
        if current is None or event.get("ts", "") > current.get("ts", ""):
            latest[txn_id] = event

count = 0
total = 0.0
for event in latest.values():
    if event.get("status") == "success":
        count += 1
        total += parse_amount(event.get("amount"))

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")