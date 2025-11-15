#!/usr/bin/env python3
"""
Schedule AUX-QHE Experiment for Off-Peak Hours
Waits until queue is low, then runs experiment automatically
"""

import time
import subprocess
from datetime import datetime, time as dt_time
from qiskit_ibm_runtime import QiskitRuntimeService

def is_off_peak(current_time=None):
    """
    Check if current time is during off-peak hours
    Off-peak: 3am-8am EST (US nighttime)
    """
    if current_time is None:
        current_time = datetime.now().time()

    off_peak_start = dt_time(3, 0)  # 3am
    off_peak_end = dt_time(8, 0)    # 8am

    return off_peak_start <= current_time <= off_peak_end


def wait_for_best_time(backend_name='ibm_brisbane', max_queue=50, check_interval=300, wait_for_off_peak=False):
    """
    Wait until conditions are good, then run experiment

    Args:
        backend_name: Backend to use
        max_queue: Max acceptable queue length
        check_interval: Seconds between checks
        wait_for_off_peak: If True, only run during off-peak hours
    """
    print("\n" + "="*80)
    print("⏰ EXPERIMENT SCHEDULER")
    print("="*80)
    print(f"Backend: {backend_name}")
    print(f"Max queue: {max_queue} jobs")
    print(f"Off-peak only: {wait_for_off_peak}")
    if wait_for_off_peak:
        print(f"Off-peak hours: 3am-8am EST")
    print("="*80 + "\n")

    try:
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    print("🔍 Monitoring queue status...")
    print("Press Ctrl+C to cancel\n")

    check_count = 0

    try:
        while True:
            check_count += 1
            now = datetime.now()
            timestamp = now.strftime("%H:%M:%S")

            try:
                status = backend.status()
                queue = status.pending_jobs
                operational = status.operational

                # Check conditions
                queue_ok = queue <= max_queue
                time_ok = not wait_for_off_peak or is_off_peak(now.time())
                ready = queue_ok and time_ok and operational

                # Status message
                print(f"[{timestamp}] Check #{check_count:3d}")
                print(f"  Queue: {queue:4d} jobs {'✅' if queue_ok else '❌'} (target: ≤{max_queue})")
                print(f"  Time: {'✅ Off-peak' if time_ok else '⏳ Peak hours'}")
                print(f"  Status: {'✅ Operational' if operational else '❌ Down'}")
                print(f"  Ready: {'🎯 YES!' if ready else '⏳ Not yet'}")

                if ready:
                    print("\n" + "="*80)
                    print("🚀 CONDITIONS MET! Starting experiment...")
                    print("="*80 + "\n")
                    return True

                # Wait before next check
                print(f"  Next check in {check_interval}s...\n")
                time.sleep(check_interval)

            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"⚠️  Error: {e}")
                time.sleep(60)

    except KeyboardInterrupt:
        print("\n\n🛑 Scheduling cancelled\n")
        return False


def run_experiment_when_ready(config='5q-3t', backend='ibm_brisbane', max_queue=50, check_interval=300, wait_for_off_peak=False):
    """
    Wait for good conditions, then automatically run experiment
    """
    print("\n" + "="*80)
    print("🤖 AUTOMATED EXPERIMENT RUNNER")
    print("="*80)
    print(f"Configuration: {config}")
    print(f"Backend: {backend}")
    print(f"Will start when queue ≤ {max_queue} jobs")
    if wait_for_off_peak:
        print(f"Waiting for off-peak hours (3am-8am EST)")
    print("="*80)

    # Wait for good conditions
    if wait_for_best_time(backend, max_queue, check_interval, wait_for_off_peak):
        # Run experiment
        print(f"Launching experiment...")
        cmd = [
            'python', 'ibm_hardware_noise_experiment.py',
            '--config', config,
            '--backend', backend
        ]

        print(f"Command: {' '.join(cmd)}\n")

        try:
            # Run experiment
            result = subprocess.run(cmd, check=True)

            print("\n" + "="*80)
            print("✅ EXPERIMENT COMPLETED!")
            print("="*80 + "\n")
            return True

        except subprocess.CalledProcessError as e:
            print("\n" + "="*80)
            print(f"❌ EXPERIMENT FAILED")
            print("="*80)
            print(f"Error: {e}\n")
            return False
    else:
        print("\nExperiment not started (cancelled)\n")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Schedule AUX-QHE experiment')
    parser.add_argument('--config', type=str, default='5q-3t',
                       help='Configuration to run (default: 5q-3t)')
    parser.add_argument('--backend', type=str, default='ibm_brisbane',
                       help='Backend to use (default: ibm_brisbane)')
    parser.add_argument('--max-queue', type=int, default=50,
                       help='Max queue length to start (default: 50)')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds (default: 300 = 5 min)')
    parser.add_argument('--off-peak', action='store_true',
                       help='Only run during off-peak hours (3-8am EST)')
    parser.add_argument('--monitor-only', action='store_true',
                       help='Only monitor, don\'t run experiment')

    args = parser.parse_args()

    if args.monitor_only:
        # Just monitor, don't run
        wait_for_best_time(
            backend_name=args.backend,
            max_queue=args.max_queue,
            check_interval=args.interval,
            wait_for_off_peak=args.off_peak
        )
    else:
        # Monitor and run when ready
        run_experiment_when_ready(
            config=args.config,
            backend=args.backend,
            max_queue=args.max_queue,
            check_interval=args.interval,
            wait_for_off_peak=args.off_peak
        )
