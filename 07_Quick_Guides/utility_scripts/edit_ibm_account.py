#!/usr/bin/env python3
"""
IBM Quantum Account Editor
Easily view, add, update, or delete IBM Quantum accounts
"""

from qiskit_ibm_runtime import QiskitRuntimeService
import json
from pathlib import Path

def view_accounts():
    """View all saved IBM Quantum accounts."""
    print("\n" + "="*80)
    print("📋 YOUR IBM QUANTUM ACCOUNTS")
    print("="*80 + "\n")

    try:
        accounts = QiskitRuntimeService.saved_accounts()

        if not accounts:
            print("❌ No accounts found!")
            print("   Run option 2 to add an account.\n")
            return

        for i, (name, details) in enumerate(accounts.items(), 1):
            print(f"{i}. Account: {name}")
            print(f"   Channel: {details.get('channel', 'N/A')}")
            print(f"   URL: {details.get('url', 'N/A')}")

            # Show partial token for security
            token = details.get('token', 'N/A')
            if token and token != 'N/A':
                masked_token = token[:10] + "..." + token[-10:] if len(token) > 20 else token[:5] + "..."
                print(f"   Token: {masked_token}")

            if 'instance' in details:
                print(f"   Instance: {details['instance'][:40]}...")

            print()

        print(f"Total accounts: {len(accounts)}")

    except Exception as e:
        print(f"❌ Error loading accounts: {e}")


def add_account():
    """Add a new IBM Quantum account."""
    print("\n" + "="*80)
    print("➕ ADD NEW IBM QUANTUM ACCOUNT")
    print("="*80 + "\n")

    print("Choose channel type:")
    print("1. IBM Cloud (Recommended - New Standard)")
    print("2. IBM Quantum Platform (Premium)")
    print("3. Local (Simulator only)")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == '1':
        channel = 'ibm_cloud'
        url = 'https://cloud.ibm.com'
    elif choice == '2':
        channel = 'ibm_quantum_platform'
        url = 'https://cloud.ibm.com'
    elif choice == '3':
        channel = 'local'
        url = None
    else:
        print("❌ Invalid choice!")
        return

    print(f"\n✅ Selected channel: {channel}")
    print(f"   URL: {url}")

    # Get account name
    name = input("\nAccount name (e.g., 'my-ibm-account'): ").strip()
    if not name:
        print("❌ Account name cannot be empty!")
        return

    # Get token
    print(f"\n🔑 Get your token from:")
    if channel == 'ibm_cloud':
        print("   https://cloud.ibm.com/quantum → Instances → API Token")
    elif channel == 'ibm_quantum_platform':
        print("   https://cloud.ibm.com/quantum → API Token")
    else:
        print("   (No token needed for local simulator)")

    token = input("\nEnter API token: ").strip()
    if not token:
        print("❌ Token cannot be empty!")
        return

    # Get instance (REQUIRED for cloud channels)
    instance = None
    if channel in ['ibm_cloud', 'ibm_quantum_platform']:
        print("\n📍 INSTANCE CRN (REQUIRED for IBM Cloud):")
        print("   Format: crn:v1:bluemix:public:quantum-computing:...")
        print("   Get it from: https://cloud.ibm.com/quantum → Your Instance")
        instance = input("\nEnter instance CRN: ").strip()
        if not instance:
            print("⚠️  Warning: Instance CRN is recommended for IBM Cloud accounts")
            confirm = input("Continue without instance? (y/n): ").strip().lower()
            if confirm != 'y':
                print("❌ Account creation cancelled.")
                return

    # Confirm
    print("\n" + "-"*80)
    print("📝 SUMMARY:")
    print(f"   Name: {name}")
    print(f"   Channel: {channel}")
    print(f"   URL: {url}")
    print(f"   Token: {token[:10]}...{token[-10:]}")
    if instance:
        print(f"   Instance: {instance[:40]}...")
    print("-"*80)

    confirm = input("\nSave this account? (y/n): ").strip().lower()

    if confirm == 'y':
        try:
            # Save account
            save_kwargs = {
                'channel': channel,
                'token': token,
                'name': name,
                'overwrite': True
            }

            # Only add URL for non-standard channels
            if url:
                save_kwargs['url'] = url

            if instance:
                save_kwargs['instance'] = instance

            QiskitRuntimeService.save_account(**save_kwargs)

            print(f"\n✅ Account '{name}' saved successfully!")

            # Test connection
            test = input("\nTest connection now? (y/n): ").strip().lower()
            if test == 'y':
                test_account(name)

        except Exception as e:
            print(f"\n❌ Error saving account: {e}")
    else:
        print("\n❌ Account not saved.")


def update_account():
    """Update an existing account."""
    print("\n" + "="*80)
    print("✏️  UPDATE EXISTING ACCOUNT")
    print("="*80 + "\n")

    accounts = QiskitRuntimeService.saved_accounts()

    if not accounts:
        print("❌ No accounts found!")
        return

    print("Select account to update:")
    for i, name in enumerate(accounts.keys(), 1):
        print(f"{i}. {name}")

    choice = input("\nEnter number: ").strip()

    try:
        idx = int(choice) - 1
        account_name = list(accounts.keys())[idx]
        current = accounts[account_name]

        print(f"\n📝 Updating: {account_name}")
        print(f"   Current channel: {current['channel']}")

        # Update token
        print(f"\n🔑 Current token: {current['token'][:10]}...{current['token'][-10:]}")
        new_token = input("   Enter new token (or press Enter to keep current): ").strip()

        if new_token:
            current['token'] = new_token

            # Save updated account
            save_kwargs = {
                'channel': current['channel'],
                'token': current['token'],
                'url': current.get('url', 'https://auth.quantum.ibm.com/api'),
                'name': account_name,
                'overwrite': True
            }

            if 'instance' in current:
                save_kwargs['instance'] = current['instance']

            QiskitRuntimeService.save_account(**save_kwargs)
            print(f"\n✅ Account '{account_name}' updated successfully!")
        else:
            print("\n❌ No changes made.")

    except (ValueError, IndexError):
        print("❌ Invalid choice!")
    except Exception as e:
        print(f"❌ Error updating account: {e}")


def delete_account():
    """Delete an account."""
    print("\n" + "="*80)
    print("🗑️  DELETE ACCOUNT")
    print("="*80 + "\n")

    accounts = QiskitRuntimeService.saved_accounts()

    if not accounts:
        print("❌ No accounts found!")
        return

    print("Select account to delete:")
    for i, name in enumerate(accounts.keys(), 1):
        print(f"{i}. {name}")

    choice = input("\nEnter number: ").strip()

    try:
        idx = int(choice) - 1
        account_name = list(accounts.keys())[idx]

        confirm = input(f"\n⚠️  Delete '{account_name}'? (y/n): ").strip().lower()

        if confirm == 'y':
            QiskitRuntimeService.delete_account(name=account_name)
            print(f"\n✅ Account '{account_name}' deleted!")
        else:
            print("\n❌ Deletion cancelled.")

    except (ValueError, IndexError):
        print("❌ Invalid choice!")
    except Exception as e:
        print(f"❌ Error deleting account: {e}")


def test_account(account_name=None):
    """Test account connection."""
    print("\n" + "="*80)
    print("🔌 TEST ACCOUNT CONNECTION")
    print("="*80 + "\n")

    if not account_name:
        accounts = QiskitRuntimeService.saved_accounts()

        if not accounts:
            print("❌ No accounts found!")
            return

        print("Select account to test:")
        for i, name in enumerate(accounts.keys(), 1):
            print(f"{i}. {name}")

        choice = input("\nEnter number: ").strip()

        try:
            idx = int(choice) - 1
            account_name = list(accounts.keys())[idx]
        except (ValueError, IndexError):
            print("❌ Invalid choice!")
            return

    print(f"\n🔌 Testing connection to '{account_name}'...")

    try:
        service = QiskitRuntimeService(name=account_name)
        print(f"   ✅ Connected successfully!")

        # Get backends
        backends = service.backends()
        print(f"   📡 Available backends: {len(backends)}")

        if backends:
            print("\n   First 5 backends:")
            for backend in backends[:5]:
                status = backend.status()
                print(f"      • {backend.name} ({backend.num_qubits} qubits) - {status.status_msg}")

        print(f"\n✅ Account '{account_name}' is working correctly!")

    except Exception as e:
        print(f"\n❌ Connection failed: {e}")


def edit_json_file():
    """Open JSON file in default text editor."""
    config_file = Path.home() / '.qiskit' / 'qiskit-ibm.json'

    print("\n" + "="*80)
    print("📝 EDIT JSON FILE DIRECTLY")
    print("="*80 + "\n")

    print(f"File location: {config_file}")

    if not config_file.exists():
        print("❌ Configuration file not found!")
        return

    print("\nOpening in default text editor...")

    import subprocess
    import platform

    try:
        if platform.system() == 'Darwin':  # macOS
            subprocess.run(['open', str(config_file)])
        elif platform.system() == 'Linux':
            subprocess.run(['xdg-open', str(config_file)])
        elif platform.system() == 'Windows':
            subprocess.run(['notepad', str(config_file)])

        print("✅ File opened!")
        print("\n⚠️  CAUTION:")
        print("   - Make sure JSON syntax is valid")
        print("   - Backup before making changes")
        print("   - Invalid JSON will break account loading")

    except Exception as e:
        print(f"❌ Error opening file: {e}")
        print(f"\nManually open: {config_file}")


def main():
    """Main menu."""
    while True:
        print("\n" + "="*80)
        print("🔧 IBM QUANTUM ACCOUNT EDITOR")
        print("="*80)
        print("\n1. View all accounts")
        print("2. Add new account")
        print("3. Update account token")
        print("4. Delete account")
        print("5. Test account connection")
        print("6. Edit JSON file directly")
        print("7. Exit")

        choice = input("\nEnter choice (1-7): ").strip()

        if choice == '1':
            view_accounts()
        elif choice == '2':
            add_account()
        elif choice == '3':
            update_account()
        elif choice == '4':
            delete_account()
        elif choice == '5':
            test_account()
        elif choice == '6':
            edit_json_file()
        elif choice == '7':
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid choice! Please enter 1-7.")


if __name__ == "__main__":
    main()
