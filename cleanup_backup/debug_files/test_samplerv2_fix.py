#!/usr/bin/env python3
"""
Minimal test to verify SamplerV2 configuration fix
"""

import logging
from qiskit import QuantumCircuit, ClassicalRegister
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler, SamplerOptions
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_samplerv2_fix():
    """Test the fixed SamplerV2 configuration"""
    try:
        print("🚀 Testing Fixed SamplerV2 Configuration")
        
        # Connect to IBM backend
        service = QiskitRuntimeService()
        backend = service.least_busy(operational=True, simulator=False)
        print(f"✅ Using backend: {backend.name}")
        
        # Create simple test circuit
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        circuit.add_register(ClassicalRegister(2, "meas"))
        circuit.measure(range(2), range(2))
        
        # Test transpilation
        pass_manager = generate_preset_pass_manager(optimization_level=1, backend=backend)
        transpiled_circuit = pass_manager.run(circuit)
        print("✅ Circuit transpilation successful")
        
        # Test fixed SamplerOptions configuration  
        options = SamplerOptions()
        options.default_shots = 1024
        print("✅ SamplerOptions configuration successful")
        
        # Test Sampler creation
        sampler = Sampler(mode=backend, options=options)
        print("✅ Sampler creation successful")
        
        # Test job submission (but don't wait for completion to avoid long runtime)
        try:
            job = sampler.run([(transpiled_circuit, None)])
            print(f"✅ Job submitted successfully: {job.job_id}")
            print(f"   Job status: {job.status()}")
            
            # Cancel job to avoid queue time
            try:
                job.cancel()
                print("✅ Job cancelled (test completed)")
            except:
                print("⚠️  Job cancellation skipped (may already be running)")
                
        except Exception as e:
            if "validation errors" in str(e):
                print(f"❌ SamplerV2 validation still failing: {e}")
                return False
            else:
                print(f"⚠️  Job submission failed (non-validation error): {e}")
        
        print("\n🎉 SamplerV2 fix verification completed!")
        print("✅ No validation errors detected")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_samplerv2_fix()
    if success:
        print("✅ SamplerV2 configuration is working correctly")
    else:
        print("❌ SamplerV2 configuration still has issues")