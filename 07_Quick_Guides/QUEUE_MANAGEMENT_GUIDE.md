# IBM Queue Management Guide

## 📊 Current Status

You have access to **2 backends**:
- **ibm_torino** (133 qubits) - **638 jobs** in queue ⭐ BEST CHOICE
- **ibm_brisbane** (127 qubits) - 3,916 jobs in queue ⚠️ VERY BUSY

**Both queues are extremely long right now!**

---

## 🛠️ Three Tools to Help You

### 1️⃣ Check Backend Queues

**Find the backend with the shortest queue:**

```bash
python check_backend_queue.py
```

**Check a specific backend:**

```bash
python check_backend_queue.py ibm_torino
```

**What it does:**
- Shows all available backends
- Displays queue length for each
- Recommends the best backend
- Estimates wait time

---

### 2️⃣ Monitor Queue Status

**Watch queue and get alerted when it drops:**

```bash
python monitor_queue.py --backend ibm_torino --threshold 100 --interval 300
```

**Options:**
- `--backend`: Backend to monitor (default: ibm_brisbane)
- `--threshold`: Alert when queue drops below this (default: 100)
- `--interval`: Check every X seconds (default: 300 = 5 min)

**Watch all backends at once:**

```bash
python monitor_queue.py --watch-all --interval 300
```

**What it does:**
- Checks queue every 5 minutes
- Shows trends (increasing/decreasing)
- Alerts you when queue drops below threshold
- Tracks min/max queue over time

**Example output:**
```
[22:30:15] Check #1  | Queue:  638 jobs | ⏳ Baseline | ✅
[22:35:20] Check #2  | Queue:  592 jobs | 📉 Decreasing | ✅
[22:40:25] Check #3  | Queue:  451 jobs | 📉 Decreasing | ✅
[22:45:30] Check #4  | Queue:   89 jobs | 📉 Decreasing | ✅

🎯 ALERT: Queue dropped to 89 jobs!
   Ready to run experiment!
```

---

### 3️⃣ Schedule Experiment

**Automatically run when conditions are good:**

```bash
python schedule_experiment.py --config 5q-3t --backend ibm_torino --max-queue 100
```

**Options:**
- `--config`: Which configuration to run (default: 5q-3t)
- `--backend`: Which backend to use (default: ibm_brisbane)
- `--max-queue`: Max queue to start (default: 50)
- `--interval`: Check interval in seconds (default: 300)
- `--off-peak`: Only run during 3-8am EST (recommended!)
- `--monitor-only`: Just monitor, don't auto-run

**Schedule for tonight (off-peak):**

```bash
python schedule_experiment.py \
  --config 5q-3t \
  --backend ibm_torino \
  --max-queue 50 \
  --interval 300 \
  --off-peak
```

**What it does:**
- Monitors queue continuously
- Waits for queue to drop below threshold
- Optionally waits for off-peak hours (3-8am EST)
- Automatically runs experiment when ready
- You can leave it running overnight!

---

## 💡 Recommendations

### Current Situation:
- **ibm_torino**: 638 jobs → Est. wait 21-53 hours 😱
- **ibm_brisbane**: 3,916 jobs → Est. wait 131-327 hours 😱😱😱

### Best Strategy:

#### Option A: Wait for Off-Peak (Recommended 🌟)
Run tonight during US nighttime (3-8am EST):

```bash
# Start this now, it will wait and auto-run when ready
python schedule_experiment.py \
  --config 5q-3t \
  --backend ibm_torino \
  --max-queue 50 \
  --off-peak
```

**Why?** Queue typically drops to 50-200 jobs during US night.

#### Option B: Monitor and Run Manually
Keep terminal open and watch:

```bash
python monitor_queue.py --backend ibm_torino --threshold 100
```

When alerted, run:

```bash
python ibm_hardware_noise_experiment.py --config 5q-3t --backend ibm_torino
```

#### Option C: Use Simulator Instead
Test everything locally first:

```bash
# This works right now, no queue!
python test_noise_experiment_local.py --qubits 5 --t-depth 3
```

---

## ⏰ Typical Queue Patterns

### Best Times (Low Queue):
- **3am-8am EST** (US nighttime) - 50-200 jobs
- **Weekends** - Generally lower
- **Holidays** - Significantly lower

### Worst Times (High Queue):
- **9am-5pm EST** (US business hours) - 500-5000+ jobs
- **Weekdays** - Generally higher
- **After major announcements** - Can spike to 10,000+

### Current Time:
Your current time is **10:21 PM EST** (October 9, 2025)
- In **~5 hours** (3am) - Queue should drop significantly
- Good time to schedule overnight run!

---

## 🎯 Recommended Workflow

### Tonight's Plan:

1. **Start scheduler now** (10:21 PM):
   ```bash
   python schedule_experiment.py \
     --config 5q-3t \
     --backend ibm_torino \
     --max-queue 50 \
     --off-peak
   ```

2. **Go to sleep** 😴

3. **Check results tomorrow morning**:
   ```bash
   ls -lrt ibm_noise_measurement_results_*.csv | tail -1
   ```

4. **If it didn't run** (queue still too long):
   - Check results: `python check_backend_queue.py`
   - Try again next night
   - Or lower threshold: `--max-queue 200`

---

## 📊 Quick Commands Reference

```bash
# Check all backends
python check_backend_queue.py

# Check specific backend
python check_backend_queue.py ibm_torino

# Monitor queue (alert at 100 jobs)
python monitor_queue.py --backend ibm_torino --threshold 100

# Watch all backends
python monitor_queue.py --watch-all

# Schedule for tonight (auto-run)
python schedule_experiment.py --config 5q-3t --backend ibm_torino --off-peak

# Just monitor (no auto-run)
python schedule_experiment.py --monitor-only --backend ibm_torino --off-peak

# Run immediately (if queue is acceptable)
python ibm_hardware_noise_experiment.py --config 5q-3t --backend ibm_torino
```

---

## ⚠️ Current Queue Status

Based on your check:
- ✅ **ibm_torino**: 638 jobs (BEST option)
- ❌ **ibm_brisbane**: 3,916 jobs (TOO BUSY)

**Recommendation**: Use **ibm_torino** and wait for off-peak hours

---

## 🚀 Start Now!

Best command to run right now:

```bash
cd /Users/giadang/my_qiskitenv && source bin/activate && cd AUX-QHE

# Option 1: Schedule for tonight (recommended)
python schedule_experiment.py --config 5q-3t --backend ibm_torino --max-queue 100 --off-peak

# Option 2: Just monitor and run manually
python monitor_queue.py --backend ibm_torino --threshold 100

# Option 3: Test locally now (no queue!)
python test_noise_experiment_local.py --qubits 5 --t-depth 3
```

---

**Good luck! 🎉**
