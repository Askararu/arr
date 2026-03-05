import re
import json

with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()


prices = [float(p.replace(" ", "").replace(",", ".")) 
          for p in re.findall(r"\d{1,3}(?: \d{3})*,\d{2}", text)]

products = [line.strip() for line in re.findall(r"\d+\.\n(.+)", text)]

date_time = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s*(\d{2}:\d{2}:\d{2})", text)
date, time = date_time.groups() if date_time else (None, None)

payment = re.search(r"(Банковская карта|Наличные)", text)
payment_method = payment.group(1) if payment else None

total_match = re.search(r"ИТОГО:\n([\d\s,]+)", text)
total = float(total_match.group(1).replace(" ", "").replace(",", ".")) if total_match else None

data = {
    "products": products,
    "prices": prices,
    "total": total,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(data, ensure_ascii=False, indent=4))