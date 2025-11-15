#!/usr/bin/env python3
"""
Monitor IBM Quantum Queue Status
Periodically checks queue and alerts when it's ready
"""

import time
from datetime import datetime
from qiskit_ibm_runtime import QiskitRuntimeService

def monitor_queue(backend_name='ibm_brisbane', threshold=100, check_interval=300):
    """
    Monitor backend queue and alert when below threshold

    Args:
        backend_name: Backend to monitor
        threshold: Alert when queue drops below this number
        check_interval: Seconds between checks (default: 300 = 5 minutes)
    """
    print("\n" + "="*80)
    print("📊 IBM QUANTUM QUEUE MONITOR")
    print("="*80)
    print(f"Backend: {backend_name}")
    print(f"Alert threshold: {threshold} jobs")
    print(f"Check interval: {check_interval}s ({check_interval//60} minutes)")
    print("="*80 + "\n")
    print("Press Ctrl+C to stop\n")

    try:
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)
    except Exception as e:
        print(f"❌ Error: {e}")
        return

    check_count = 0
    min_queue = float('inf')
    max_queue = 0

    try:
        while True:
            check_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")

            try:
                status = backend.status()
                queue = status.pending_jobs
                operational = status.operational

                # Track min/max
                min_queue = min(min_queue, queue)
                max_queue = max(max_queue, queue)

                # Status icon
                status_icon = "✅" if operational else "❌"

                # Trend indicator
                if check_count > 1:
                    if queue < prev_queue:
                        trend = "📉 Decreasing"
                    elif queue > prev_queue:
                        trend = "📈 Increasing"
                    else:
                        trend = "➡️  Stable"
                else:
                    trend = "⏳ Baseline"

                print(f"[{timestamp}] Check #{check_count:3d} | Queue: {queue:4d} jobs | {trend} | {status_icon}")

                # Alert if below threshold
                if queue <= threshold and operational:
                    print("\n" + "="*80)
                    print(f"🎯 ALERT: Queue dropped to {queue} jobs!")
                    print(f"   Backend: {backend_name}")
                    print(f"   Time: {timestamp}")
                    print(f"   Status: Operational")
                    print(f"\n   Ready to run experiment!")
                    print(f"   python ibm_hardware_noise_experiment.py --config 5q-3t --backend {backend_name}")
                    print("="*80 + "\n")

                    # Ask if user wants to continue monitoring
                    try:
                        response = input("Continue monitoring? (y/n): ")
                        if response.lower() != 'y':
                            break
                    except:
                        break

                prev_queue = queue

                # Wait before next check
                time.sleep(check_interval)

            except KeyboardInterrupt:
                raise
            except Exception as e:
                print(f"⚠️  Error checking status: {e}")
                time.sleep(60)  # Wait 1 minute on error

    except KeyboardInterrupt:
        print("\n\n" + "="*80)
        print("🛑 Monitoring stopped")
        print("="*80)
        print(f"Total checks: {check_count}")
        print(f"Min queue: {min_queue} jobs")
        print(f"Max queue: {max_queue} jobs")
        print(f"Last queue: {queue} jobs")
        print("="*80 + "\n")


def watch_multiple_backends(backend_list=None, check_interval=300):
    """
    Watch multiple backends and show which has shortest queue

    Args:
        backend_list: List of backend names (default: all available)
        check_interval: Seconds between checks
    """
    print("\n" + "="*80)
    print("👀 WATCHING MULTIPLE BACKENDS")
    print("="*80 + "\n")

    try:
        service = QiskitRuntimeService()

        if backend_list is None:
            backends = [b for b in service.backends() if not b.simulator]
            backend_list = [b.name for b in backends]

        print(f"Monitoring {len(backend_list)} backends:")
        for name in backend_list:
            print(f"  - {name}")
        print(f"\nCheck interval: {check_interval}s")
        print("Press Ctrl+C to stop\n")

        check_count = 0

        try:
            while True:
                check_count += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"\n[{timestamp}] Check #{check_count}")
                print("-" * 60)

                queue_info = []
                for backend_name in backend_list:
                    try:
                        backend = service.backend(backend_name)
                        status = backend.status()
                        queue_info.append({
                            'name': backend_name,
                            'queue': status.pending_jobs,
                            'operational': status.operational
                        })
                    except:
                        continue

                # Sort by queue length
                queue_info.sort(key=lambda x: x['queue'])

                # Display top 5 shortest queues
                print(f"{'Backend':<20} {'Queue':<10} {'Status'}")
                for info in queue_info[:5]:
                    status_icon = "✅" if info['operational'] else "❌"
                    print(f"{info['name']:<20} {info['queue']:<10} {status_icon}")

                best = queue_info[0]
                print(f"\n🏆 Best: {best['name']} ({best['queue']} jobs)")

                time.sleep(check_interval)

        except KeyboardInterrupt:
            print("\n\n🛑 Monitoring stopped\n")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Monitor IBM Quantum queue status')
    parser.add_argument('--backend', type=str, default='ibm_brisbane',
                       help='Backend to monitor (default: ibm_brisbane)')
    parser.add_argument('--threshold', type=int, default=100,
                       help='Alert when queue drops below this (default: 100)')
    parser.add_argument('--interval', type=int, default=300,
                       help='Check interval in seconds (default: 300 = 5 min)')
    parser.add_argument('--watch-all', action='store_true',
                       help='Watch all backends and show shortest queue')

    args = parser.parse_args()

    if args.watch_all:
        watch_multiple_backends(check_interval=args.interval)
    else:
        monitor_queue(
            backend_name=args.backend,
            threshold=args.threshold,
            check_interval=args.interval
        )
