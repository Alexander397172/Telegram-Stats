import json
from collections import defaultdict

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

with open(config["telegram_export_path"], "r", encoding="utf-8") as f:
    data = json.load(f)

names = {}
try:
    with open("names.txt", "r", encoding="utf-8") as f:
        for line in f:
            uid, name = line.strip().split(":", 1)
            names[uid] = name
except FileNotFoundError:
    pass

daily_counts = defaultdict(lambda: defaultdict(int))

for msg in data.get("messages", []):
    if msg.get("type") != "message":
        continue #игнор сервисных сообщений

    uid = msg.get("from_id")
    if not uid:
        continue

    if uid.startswith("user"):
        uid = uid[4:]

    if uid.startswith("channel"):
        continue

    date = msg["date"].split("T")[0]
    daily_counts[date][uid] += 1

    if uid not in names and msg.get("from"):
        names[uid] = msg["from"]

with open("names.txt", "w", encoding="utf-8") as f:
    for uid, name in sorted(names.items()):
        f.write(f"{uid}:{name}\n")

with open("message_stats.txt", "w", encoding="utf-8") as f:
    for date in sorted(daily_counts):
        f.write(f"Дата: {date}\n")
        for uid, count in daily_counts[date].items():
            f.write(f"  {uid}:{count}\n")
        f.write("\n")

print("Готово")
