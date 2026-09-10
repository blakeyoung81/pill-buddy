import json

state_file = "/root/ivysprouts/data/ivysprouts_state.json"
lessons_file = "/root/ivysprouts/data/ivysprouts_lessons.json"

state = json.load(open(state_file))
lessons = json.load(open(lessons_file))

print(f"Total lessons in curriculum: {len(lessons)}")
print(f"Total entries in state: {len(state)}")

pending = []
for l in lessons:
    title = l.get("title")
    info = state.get(title, {})
    status = info.get("status")
    fails = info.get("fail_count", 0)
    if status != "done":
        pending.append((title, status, fails))

print(f"Pending lessons count: {len(pending)}")
print("First 5 pending lessons:")
for t, s, f in pending[:5]:
    print(f"  [{s} | fails={f}] {t}")
