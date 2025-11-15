#!/usr/bin/env python3
"""
Test IBM Quantum Connection
Verify your IBM account can connect before running full experiment
"""

from qiskit_ibm_runtime import QiskitRuntimeService
import sys

def test_connection():
    """Test IBM Quantum connection."""
    print("\n" + "="*80)
    print("🔌 TESTING IBM QUANTUM CONNECTION")
    print("="*80 + "\n")

    # Step 1: Load account
    print("1️⃣  Loading IBM Quantum account...")
    try:
        service = QiskitRuntimeService()
        print("   ✅ Account loaded successfully!\n")
    except Exception as e:
        print(f"   ❌ Failed to load account: {e}\n")
        print("💡 Troubleshooting:")
        print("   - Check your internet connection")
        print("   - Verify account is saved: python edit_ibm_account.py")
        print("   - Check token hasn't expired")
        return False

    # Step 2: Get account info
    print("2️⃣  Getting account information...")
    try:
        active = service.active_account()
        if active:
            print(f"   Account channel: {active.get('channel', 'N/A')}")
            print(f"   URL: {active.get('url', 'N/A')}")
            print("   ✅ Account info retrieved!\n")
        else:
            print("   ⚠️  No active account details available\n")
    except Exception as e:
        print(f"   ⚠️  Could not get account info: {e}\n")

    # Step 3: List backends
    print("3️⃣  Fetching available backends...")
    try:
        backends = service.backends()
        print(f"   ✅ Found {len(backends)} quantum backends!\n")

        if backends:
            print("   📡 Available Quantum Computers:")
            print("   " + "-"*70)

            for backend in backends[:10]:  # Show first 10
                try:
                    status = backend.status()
                    print(f"   • {backend.name}")
                    print(f"     Qubits: {backend.num_qubits}")
                    print(f"     Status: {status.status_msg}")
                    print(f"     Queue: {status.pending_jobs} jobs")
                    print()
                except Exception as e:
                    print(f"   • {backend.name} (status unavailable)")
                    print()

            if len(backends) > 10:
                print(f"   ... and {len(backends) - 10} more backends\n")

        return True

    except Exception as e:
        print(f"   ❌ Failed to fetch backends: {e}\n")
        print("💡 This usually means:")
        print("   - Network connection issue")
        print("   - IBM Quantum services are down")
        print("   - Authentication token is invalid")
        return False


def test_backend_access(backend_name='ibm_brisbane'):
    """Test access to a specific backend."""
    print("\n" + "="*80)
    print(f"🖥️  TESTING ACCESS TO {backend_name.upper()}")
    print("="*80 + "\n")

    try:
        service = QiskitRuntimeService()
        backend = service.backend(backend_name)

        print(f"✅ Successfully connected to {backend.name}!\n")

        # Get backend properties
        print("Backend Details:")
        print("-" * 60)
        print(f"Name: {backend.name}")
        print(f"Qubits: {backend.num_qubits}")
        print(f"Version: {backend.version}")

        # Get status
        status = backend.status()
        print(f"\nStatus: {status.status_msg}")
        print(f"Operational: {status.operational}")
        print(f"Pending jobs: {status.pending_jobs}")

        # Get configuration
        config = backend.configuration()
        print(f"\nMax shots: {config.max_shots}")
        print(f"Max experiments: {config.max_experiments}")

        print("\n✅ Backend is ready for use!")
        return True

    except Exception as e:
        print(f"❌ Failed to access {backend_name}: {e}\n")
        print("💡 Try a different backend:")
        print("   python test_ibm_connection.py --backend ibm_kyoto")
        return False


def main():
    """Main test function."""
    import argparse

    parser = argparse.ArgumentParser(description='Test IBM Quantum Connection')
    parser.add_argument('--backend', type=str, default='ibm_brisbane',
                       help='Backend to test (default: ibm_brisbane)')
    args = parser.parse_args()

    # Test connection
    connection_ok = test_connection()

    if not connection_ok:
        print("\n" + "="*80)
        print("❌ CONNECTION TEST FAILED")
        print("="*80)
        print("\n⚠️  Cannot proceed with hardware experiments")
        print("   Please fix connection issues first")
        sys.exit(1)

    # Test backend access
    backend_ok = test_backend_access(args.backend)

    if backend_ok:
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED!")
        print("="*80)
        print("\n🚀 You're ready to run IBM hardware experiments:")
        print(f"   python ibm_hardware_noise_experiment.py --backend {args.backend}")
    else:
        print("\n" + "="*80)
        print("⚠️  BACKEND TEST FAILED")
        print("="*80)
        print("\n💡 But other backends may work. Try running:")
        print("   python ibm_hardware_noise_experiment.py")


if __name__ == "__main__":
    main()
