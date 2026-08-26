import extract_transactions
from datetime import datetime

records = extract_transactions.parse_eml_files()
start_dt = datetime(2026, 7, 24, 0, 0, 0)

filtered = [r for r in records if r['dt'] >= start_dt]

total_expense = 0
total_refund = 0

print(f"Total transactions from 24/07/2026 to today (26/08/2026): {len(filtered)}\n")
for idx, r in enumerate(filtered, 1):
    amt_str = r['amount'].replace('VND', '').replace(',', '').strip()
    is_neg = '-' in amt_str
    is_pos = '+' in amt_str
    amt_val = float(amt_str.replace('-', '').replace('+', '').strip())
    
    if is_neg:
        total_expense += amt_val
        print(f"{idx:2d}. {r['time']} | -{amt_val:10,.0f} VND | {r['content']}")
    elif is_pos:
        total_refund += amt_val
        print(f"{idx:2d}. {r['time']} | +{amt_val:10,.0f} VND (Refund) | {r['content']}")

net_spending = total_expense - total_refund
print("-" * 55)
print(f"Tổng tiền chi tiêu (Gross Spending): {total_expense:,.0f} VND")
print(f"Tổng tiền hoàn (Refunds/Credits):   +{total_refund:,.0f} VND")
print(f"Tổng chi tiêu thực tế (Net Total):  {net_spending:,.0f} VND")
