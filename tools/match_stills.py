"""Find the timestamp in each video where each numbered still appears.
Used to time the existing detailed stills from the five-day course (Day 1 was done this way).
Usage: python3 match_stills.py <videos_dir> <stills_dir> <day> <out.json>
Stills are named D-V-S.jpg (day, video, sub-step). Videos are 'Day D - V - Title-....mov'."""
import sys, os, re, glob, json, subprocess
import numpy as np
W, H, FPS = 240, 135, 4
Y0,Y1,X0,X1 = int(H*.30), int(H*.74), int(W*.15), int(W*.86)
def norm(a):
    a = a[..., Y0:Y1, X0:X1]
    m = a.mean(axis=(-2,-1), keepdims=True); sd = a.std(axis=(-2,-1), keepdims=True)+1e-3
    return (a-m)/sd
def frames(path):
    cmd = ["ffmpeg","-v","error","-i",path,"-map","0:v:0","-vf",f"fps={FPS},scale={W}:{H},format=gray","-f","rawvideo","-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return norm(np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32))
def still(path):
    cmd = ["ffmpeg","-v","error","-i",path,"-vf",f"scale={W}:{H},format=gray","-f","rawvideo","-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return norm(np.frombuffer(raw, np.uint8).reshape(H, W).astype(np.float32))
def monotonic(cost):
    # cost: S x F. choose f_1 <= f_2 <= ... minimizing total cost (DP).
    S, F = cost.shape; dp = cost[0].copy(); back = []
    for s in range(1, S):
        best_idx = np.zeros(F, int); run = dp.copy(); idx = np.arange(F)
        for f in range(1, F):
            if run[f-1] < run[f]: run[f] = run[f-1]; idx[f] = idx[f-1]
        back.append(idx); dp = run + cost[s]
    f = int(np.argmin(dp)); path = [f]
    for s in range(S-2, -1, -1): f = int(back[s][f]); path.append(f)
    return path[::-1]
vdir, sdir, day, out = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
result = []
for vpath in sorted(glob.glob(os.path.join(vdir, f"Day {day} - *.mov")), key=lambda p: int(re.search(r"Day \d+ - (\d+) - ", p).group(1))):
    m = re.search(r"Day \d+ - (\d+) - (.*?)-HD", os.path.basename(vpath)); v, title = int(m.group(1)), m.group(2).strip()
    fr = frames(vpath)
    sp = sorted(glob.glob(os.path.join(sdir, f"{day}-{v}-*.jpg")), key=lambda p: int(p.rsplit("-",1)[1].split(".")[0]))
    cost = np.array([(np.abs(fr-st) > 0.9).mean(axis=(1,2))*100 for st in map(still, sp)])
    path = monotonic(cost)
    subs = [{"still": os.path.basename(p), "t": round(f/FPS, 2), "diff": round(float(cost[k, f]), 2), "best_unordered_t": round(int(np.argmin(cost[k]))/FPS, 2)} for k, (p, f) in enumerate(zip(sp, path))]
    result.append({"video": v, "title": title, "file": os.path.basename(vpath), "duration": round(len(fr)/FPS, 2), "subs": subs})
    print(v, title, [(s["still"], s["t"], s["diff"]) for s in subs], flush=True)
json.dump(result, open(out, "w"), indent=1)
