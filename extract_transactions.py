import glob
import os
import email
from email import policy
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def parse_eml_files(folder_path="emails"):
    files = glob.glob(os.path.join(folder_path, "*.eml"))
    records = []
    
    for f in files:
        with open(f, "rb") as fp:
            msg = email.message_from_binary_file(fp, policy=policy.default)
        
        body = msg.get_body(preferencelist=("html", "plain"))
        html_content = body.get_content() if body else ""
        soup = BeautifulSoup(html_content, "html.parser")
        
        record = {
            "file": os.path.basename(f),
            "amount": "",
            "content": "",
            "time": "",
            "limit": "",
            "card": "",
            "txn_code": ""
        }
        
        h5_list = soup.find_all("h5")
        for h5 in h5_list:
            text_h5 = h5.get_text(strip=True)
            p = h5.find_next_sibling("p")
            if not p:
                continue
            label = p.get_text(strip=True)
            
            if "tiền thay đổi" in label or "Changed Amount" in label:
                record["amount"] = text_h5
            elif "Nội dung" in label or "Transaction Content" in label:
                record["content"] = text_h5
            elif "Thời gian" in label or "Time" in label:
                record["time"] = text_h5
            elif "Hạn mức" in label or "Available Limit" in label:
                record["limit"] = text_h5
            elif "Thẻ" in label or "Card" in label:
                record["card"] = text_h5
            elif "Mã giao dịch" in label or "Transaction Code" in label:
                record["txn_code"] = text_h5
        
        try:
            record["dt"] = datetime.strptime(record["time"], "%d/%m/%Y %H:%M:%S")
        except Exception:
            record["dt"] = datetime.min
            
        records.append(record)
    
    # Sort chronologically (newest first)
    records.sort(key=lambda x: x["dt"], reverse=True)
    return records

def export_csv(records, output_file="transactions.csv"):
    fieldnames = [
        "STT",
        "Thời gian (Time)",
        "Số tiền thay đổi (Amount)",
        "Nội dung (Content)",
        "Thẻ (Card)",
        "Hạn mức còn lại (Available Limit)",
        "Mã giao dịch (Txn Code)",
        "Tên file (File Name)"
    ]
    
    with open(output_file, "w", newline="", encoding="utf-8-sig") as fp:
        writer = csv.writer(fp)
        writer.writerow(fieldnames)
        for idx, r in enumerate(records, start=1):
            writer.writerow([
                idx,
                r["time"],
                r["amount"],
                r["content"],
                r["card"],
                r["limit"],
                f"'{r['txn_code']}",
                r["file"]
            ])

if __name__ == "__main__":
    records = parse_eml_files()
    export_csv(records, "transactions.csv")
    print(f"Successfully extracted {len(records)} transactions to transactions.csv")
