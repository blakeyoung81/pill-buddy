import json
import os
import subprocess
import time

print("=== IVYSPROUTS STATUS & LAUNCH ===")

state_file = "/root/ivysprouts/data/ivysprouts_state.json"
lessons_file = "/root/ivysprouts/data/ivysprouts_lessons.json"

state = json.load(open(state_file))
lessons = json.load(open(lessons_file))

print(f"Total curriculum lessons: {len(lessons)}")
print(f"Total state entries: {len(state)}")

pending = []
for l in lessons:
    title = l.get("title")
    info = state.get(title, {})
    status = info.get("status")
    fails = info.get("fail_count", 0)
    if status != "done":
        pending.append((title, status, fails))

print(f"Total pending lessons: {len(pending)}")
for i, (t, s, f) in enumerate(pending[:8]):
    print(f"  {i+1}. [{s} | fails={f}] {t}")

# Check DGX Spark ComfyUI tunnel
res = subprocess.run(["bash", "/root/spark_tunnel.sh"], capture_output=True, text=True)
print(f"Spark ComfyUI tunnel (:18288): HTTP {res.stdout.strip()}")

# Launch pipeline in tmux session
print("Launching daily churn pipeline in tmux session 'ivy'...")
subprocess.run(["tmux", "new-session", "-d", "-s", "ivy", "cd /root/ivysprouts && bash ops/run_vps.sh 2>&1 | tee -a manual_run.log"])
time.sleep(2)

# Check tmux status
tmux_check = subprocess.run(["tmux", "ls"], capture_output=True, text=True)
print("Active tmux sessions:")
print(tmux_check.stdout.strip())
print("=== LAUNCHED SUCCESSFULLY ===")
