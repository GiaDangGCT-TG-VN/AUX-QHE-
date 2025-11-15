#!/usr/bin/env python3
"""
Check IBM Quantum Backend Queue Status
Helps you find the best backend with shortest queue
"""

from qiskit_ibm_runtime import QiskitRuntimeService
import sys

def check_all_backends(account_name=None):
    """Check queue status for all available backends"""
    print("\n" + "="*80)
    print("🔍 IBM QUANTUM BACKEND QUEUE STATUS")
    print("="*80 + "\n")

    try:
        # Try to load specific account or default
        if account_name:
            service = QiskitRuntimeService(name=account_name)
            print(f"✅ Account loaded: {account_name}\n")
        else:
            service = QiskitRuntimeService()
            print("✅ Default account loaded\n")
    except Exception as e:
        print(f"❌ Error loading account: {e}")
        print("\n💡 Try one of these:")
        print("   1. Update your account: python edit_ibm_account.py")
        print("   2. Specify account: python check_backend_queue.py --account GiaDang_AUX")
        print("   3. Check guide: cat UPDATE_IBM_ACCOUNT_GUIDE.md")
        return

    # Get all backends
    backends = service.backends()

    # Filter for quantum backends (not simulators)
    quantum_backends = [b for b in backends if not b.simulator]

    if not quantum_backends:
        print("❌ No quantum backends found")
        return

    print(f"Found {len(quantum_backends)} quantum backends:\n")

    # Sort by queue length
    backend_info = []
    for backend in quantum_backends:
        try:
            status = backend.status()
            backend_info.append({
                'name': backend.name,
                'qubits': backend.num_qubits,
                'queue': status.pending_jobs,
                'operational': status.operational,
                'status_msg': status.status_msg
            })
        except Exception as e:
            print(f"⚠️  Could not get status for {backend.name}: {e}")

    # Sort by queue length (shortest first)
    backend_info.sort(key=lambda x: x['queue'])

    # Display results
    print(f"{'Backend':<20} {'Qubits':<8} {'Queue':<8} {'Status':<12} {'Message'}")
    print("-" * 80)

    for info in backend_info:
        status_icon = "✅" if info['operational'] else "❌"
        queue_str = f"{info['queue']}" if info['queue'] < 1000 else f"{info['queue']:,}"
        print(f"{info['name']:<20} {info['qubits']:<8} {queue_str:<8} {status_icon} {info['status_msg']:<12}")

    # Recommendations
    print("\n" + "="*80)
    print("💡 RECOMMENDATIONS")
    print("="*80)

    # Find best backend (shortest queue, operational, enough qubits)
    best = None
    for info in backend_info:
        if info['operational'] and info['qubits'] >= 5:
            best = info
            break

    if best:
        print(f"\n🎯 Best choice for 5q-3t experiment:")
        print(f"   Backend: {best['name']}")
        print(f"   Qubits: {best['qubits']}")
        print(f"   Queue: {best['queue']} jobs")
        print(f"   Est. wait time: {best['queue'] * 2}-{best['queue'] * 5} minutes")
        print(f"\n   Run with:")
        print(f"   python ibm_hardware_noise_experiment.py --config 5q-3t --backend {best['name']}")

    # Show queue trends
    avg_queue = sum(b['queue'] for b in backend_info) / len(backend_info)
    print(f"\n📊 Queue Statistics:")
    print(f"   Average queue: {avg_queue:.0f} jobs")
    print(f"   Shortest queue: {backend_info[0]['queue']} jobs ({backend_info[0]['name']})")
    print(f"   Longest queue: {backend_info[-1]['queue']} jobs ({backend_info[-1]['name']})")

    if avg_queue > 100:
        print(f"\n⚠️  High traffic detected!")
        print(f"   Consider running during off-peak hours (US nighttime, 3-8am EST)")

    print("\n" + "="*80 + "\n")


def check_specific_backend(backend_name, account_name=None):
    """Check status of a specific backend"""
    print(f"\n🔍 Checking {backend_name}...\n")

    try:
        if account_name:
            service = QiskitRuntimeService(name=account_name)
        else:
            service = QiskitRuntimeService()

        backend = service.backend(backend_name)
        status = backend.status()

        print(f"Backend: {backend.name}")
        print(f"Qubits: {backend.num_qubits}")
        print(f"Queue: {status.pending_jobs} jobs")
        print(f"Status: {status.status_msg}")
        print(f"Operational: {'✅ Yes' if status.operational else '❌ No'}")

        if status.pending_jobs > 0:
            est_min = status.pending_jobs * 2
            est_max = status.pending_jobs * 5
            print(f"\nEstimated wait: {est_min}-{est_max} minutes")

        return status.pending_jobs

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 If account error, update with: python edit_ibm_account.py")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Check IBM Quantum backend queue status')
    parser.add_argument('backend', nargs='?', help='Specific backend to check (e.g., ibm_brisbane)')
    parser.add_argument('--account', '-a', help='Account name to use (e.g., GiaDang_AUX)')

    args = parser.parse_args()

    if args.backend:
        # Check specific backend
        check_specific_backend(args.backend, args.account)
    else:
        # Check all backends
        check_all_backends(args.account)
