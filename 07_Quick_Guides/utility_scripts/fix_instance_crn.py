#!/usr/bin/env python3
"""
Fix Instance CRN Issues
Helps diagnose and fix IBM Quantum instance problems
"""

from qiskit_ibm_runtime import QiskitRuntimeService
import sys

print("=" * 80)
print("🔍 IBM QUANTUM INSTANCE CRN DIAGNOSTIC")
print("=" * 80)

# Step 1: Check current accounts
print("\n📋 Step 1: Checking saved accounts...")
accounts = QiskitRuntimeService.saved_accounts()

if not accounts:
    print("❌ No accounts found!")
    print("   Run: python edit_ibm_account.py")
    sys.exit(1)

print(f"\nFound {len(accounts)} account(s):")
for name, details in accounts.items():
    print(f"\n   Account: {name}")
    print(f"   Channel: {details.get('channel')}")
    if 'instance' in details:
        crn = details['instance']
        print(f"   Instance CRN: {crn}")
        
        # Check for common issues
        if crn.endswith('::'):
            print(f"   ⚠️  WARNING: CRN ends with '::' (should end with single ':')")
        if not crn.startswith('crn:v1:bluemix:public:quantum-computing:'):
            print(f"   ⚠️  WARNING: CRN format looks incorrect")

# Step 2: Try to load service and get instances
print("\n" + "=" * 80)
print("📡 Step 2: Trying to connect...")
print("=" * 80)

for name in accounts.keys():
    print(f"\n🔌 Testing account: {name}")
    try:
        service = QiskitRuntimeService(name=name)
        print(f"   ✅ Connected successfully!")
        
        # Get instances
        print(f"\n   📍 Available instances:")
        try:
            instances = service.instances()
            if instances:
                for i, instance in enumerate(instances, 1):
                    print(f"      {i}. {instance}")
            else:
                print(f"      ❌ No instances found")
                print(f"      💡 You may need to create an instance at:")
                print(f"         https://cloud.ibm.com/quantum")
        except Exception as e:
            print(f"      ⚠️  Could not list instances: {e}")
        
        # Get backends
        print(f"\n   🖥️  Available backends:")
        try:
            backends = service.backends()
            if backends:
                print(f"      Found {len(backends)} backend(s):")
                for backend in backends[:5]:
                    print(f"         • {backend.name} ({backend.num_qubits} qubits)")
                if len(backends) > 5:
                    print(f"         ... and {len(backends) - 5} more")
            else:
                print(f"      ❌ No backends accessible!")
                print(f"      💡 Possible reasons:")
                print(f"         1. Wrong instance CRN")
                print(f"         2. No access to backends in this instance")
                print(f"         3. Instance not properly provisioned")
        except Exception as e:
            print(f"      ❌ Error accessing backends: {e}")
            
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")

# Step 3: Recommendations
print("\n" + "=" * 80)
print("💡 RECOMMENDATIONS")
print("=" * 80)

print("""
If you see 'Invalid instance' or 'No backends accessible':

1. **Verify your Instance CRN:**
   - Login to: https://cloud.ibm.com/quantum
   - Click on your instance name
   - Copy the FULL Instance CRN (should NOT end with '::')
   - Format: crn:v1:bluemix:public:quantum-computing:us-east:a/...:...:

2. **Check Instance Access:**
   - Make sure your instance has backend access
   - Free tier: Limited backends
   - Paid tier: More backends available

3. **Update Your Account:**
   python edit_ibm_account.py
   # Delete old account
   # Add new account with CORRECT Instance CRN (no '::' at end)

4. **Alternative: Try without Instance CRN:**
   Some accounts work better without specifying instance.
   When adding account, press Enter to skip instance CRN.

5. **Verify Access:**
   After updating, test with:
   python check_backend_queue.py --account GiaDang_AUX
""")

print("=" * 80)
