import extract_transactions

records = extract_transactions.parse_eml_files()
# sort oldest to newest
records.sort(key=lambda x: x['dt'])

def parse_num(s):
    return float(s.replace('VND', '').replace(',', '').replace('+', '').replace('-', '').strip())

for i in range(len(records)):
    r = records[i]
    time_str = r['dt'].strftime('%d/%m/%Y %H:%M')
    amt = r['amount']
    limit = parse_num(r['limit'])
    
    diff_str = ""
    if i > 0:
        prev_limit = parse_num(records[i-1]['limit'])
        cur_amt = parse_num(amt)
        expected_limit = prev_limit - cur_amt if '-' in amt else prev_limit + cur_amt
        diff = limit - expected_limit
        if abs(diff) > 1:
            diff_str = f" [GAP DETECTED: expected {expected_limit:,.0f}, actual {limit:,.0f}, diff: {diff:,.0f}]"
            
    print(f"{time_str} | {amt:>15} | Limit: {limit:>12,.0f} | {r['content']:<22} {diff_str}")
