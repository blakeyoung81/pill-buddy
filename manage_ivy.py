import json
import os
import sys
import subprocess

print("=== IVYSPROUTS PIPELINE RECOVERY & LAUNCH ===")

state_file = "/root/ivysprouts/data/ivysprouts_state.json"
with open(state_file) as f:
    state = json.load(f)

print(f"Total entries in state: {len(state)}")

unparked = []
for title, info in state.items():
    if title.startswith("Letter Names & Sounds:"):
        continue
    if info.get("fail_count", 0) > 0:
        print(f"Resetting fail_count for: {title} (was {info['fail_count']})")
        info["fail_count"] = 0
        unparked.append(title)

with open(state_file, "w") as f:
    json.dump(state, f, indent=2)
print(f"Total unparked lessons: {len(unparked)}")

lock_file = "/root/ivysprouts/data/ivysprouts.lock"
if os.path.exists(lock_file):
    os.remove(lock_file)
    print(f"Removed stale lock: {lock_file}")
else:
    print("No stale lock file found.")

# Verify feelings song
for k, v in state.items():
    if "Feelings" in k:
        print(f"Feelings song status: {v.get('status')}, fail_count: {v.get('fail_count')}")

# Check pre-rendered video
video_cand = "/root/ivysprouts/output/tiny-tunes/My_Feelings_Song_for_Kids_Happy_Sad_Mad_Calm_/runs/20260804_230005/final_video_karaoke_sub.mp4"
if os.path.exists(video_cand):
    print(f"Found pre-rendered video: {video_cand} ({os.path.getsize(video_cand)} bytes)")
else:
    print("Checking glob for feelings video...")
    import glob
    matches = glob.glob("/root/ivysprouts/output/**/final_video_karaoke_sub.mp4", recursive=True)
    for m in matches:
        print(f"  Existing render: {m} ({os.path.getsize(m)} bytes)")

res = subprocess.run(["bash", "/root/spark_tunnel.sh"], capture_output=True, text=True)
print(f"Spark tunnel health code: {res.stdout.strip()}")
print("=== SETUP COMPLETE ===")
