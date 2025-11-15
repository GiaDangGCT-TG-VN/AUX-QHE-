"""
OpenQASM 3 Circuit Analyzer for AUX-QHE
Interactive analysis of OpenQASM 3 features and auxiliary states
"""

import re
import json
from pathlib import Path

def analyze_openqasm3_file(file_path):
    """
    Analyze OpenQASM 3 file and extract AUX-QHE specific information.

    Args:
        file_path (str): Path to OpenQASM 3 file

    Returns:
        dict: Analysis results
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        print(f"🔍 Analyzing OpenQASM 3 File: {Path(file_path).name}")
        print("=" * 60)

        analysis = {
            'file_info': analyze_file_structure(content),
            'qasm3_features': analyze_qasm3_features(content),
            'aux_qhe_data': analyze_aux_qhe_data(content),
            'circuit_operations': analyze_circuit_operations(content),
            'classical_data': analyze_classical_data(content)
        }

        display_analysis(analysis)
        return analysis

    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return None

def analyze_file_structure(content):
    """Analyze basic file structure."""
    lines = content.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    comment_lines = [line for line in lines if line.strip().startswith('//')]

    return {
        'total_lines': len(lines),
        'non_empty_lines': len(non_empty_lines),
        'comment_lines': len(comment_lines),
        'file_size': len(content),
        'has_openqasm3_header': 'OPENQASM 3.0' in content
    }

def analyze_qasm3_features(content):
    """Analyze OpenQASM 3 specific features."""
    features = {
        'classical_types': [],
        'functions': [],
        'structs': [],
        'conditionals': 0,
        'loops': 0,
        'includes': []
    }

    # Find classical types
    type_patterns = [
        r'bit\[\d+\]',
        r'int\[\d+\]',
        r'const int',
        r'const bit'
    ]

    for pattern in type_patterns:
        matches = re.findall(pattern, content)
        features['classical_types'].extend(matches)

    # Find function definitions
    func_matches = re.findall(r'def\s+(\w+)\s*\([^)]*\)', content)
    features['functions'] = func_matches

    # Find struct definitions
    struct_matches = re.findall(r'struct\s+(\w+)\s*{', content)
    features['structs'] = struct_matches

    # Count conditionals and loops
    features['conditionals'] = len(re.findall(r'\bif\s*\(', content))
    features['loops'] = len(re.findall(r'\bfor\s+', content))

    # Find includes
    include_matches = re.findall(r'include\s+"([^"]+)"', content)
    features['includes'] = include_matches

    return features

def analyze_aux_qhe_data(content):
    """Analyze AUX-QHE specific data."""
    aux_data = {
        'auxiliary_states': 0,
        'layers': [],
        'cross_terms': {},
        'qotp_keys': {},
        't_gates': 0,
        'aux_corrections': 0
    }

    # Extract auxiliary state count
    aux_match = re.search(r'total_aux_states\s*=\s*(\d+)', content)
    if aux_match:
        aux_data['auxiliary_states'] = int(aux_match.group(1))

    # Extract layer information
    layer_matches = re.findall(r'layer_(\d+)_size\s*=\s*(\d+)', content)
    for layer, size in layer_matches:
        aux_data['layers'].append({'layer': int(layer), 'size': int(size)})

    # Extract cross-terms
    cross_matches = re.findall(r'layer_(\d+)_cross_terms\s*=\s*(\d+)', content)
    for layer, count in cross_matches:
        aux_data['cross_terms'][int(layer)] = int(count)

    # Extract QOTP keys
    a_key_match = re.search(r'a_init\s*=\s*"([01]+)"', content)
    b_key_match = re.search(r'b_init\s*=\s*"([01]+)"', content)

    if a_key_match and b_key_match:
        aux_data['qotp_keys'] = {
            'a_init': a_key_match.group(1),
            'b_init': b_key_match.group(1)
        }

    # Count T-gates and auxiliary corrections
    aux_data['t_gates'] = len(re.findall(r'\bt\s+q\[', content))
    aux_data['aux_corrections'] = len(re.findall(r'aux_t|apply_aux_correction', content))

    return aux_data

def analyze_circuit_operations(content):
    """Analyze quantum circuit operations."""
    operations = {
        'quantum_gates': {},
        'measurements': 0,
        'total_operations': 0
    }

    # Common quantum gates
    gate_patterns = {
        'hadamard': r'\bh\s+q\[',
        't_gate': r'\bt\s+q\[',
        'cnot': r'\bcx\s+q\[',
        'pauli_x': r'\bx\s+q\[',
        'pauli_z': r'\bz\s+q\[',
        'phase': r'\bp\s+q\['
    }

    for gate_name, pattern in gate_patterns.items():
        count = len(re.findall(pattern, content))
        if count > 0:
            operations['quantum_gates'][gate_name] = count
            operations['total_operations'] += count

    # Count measurements
    operations['measurements'] = len(re.findall(r'measure\s+q\[', content))

    return operations

def analyze_classical_data(content):
    """Analyze classical data structures."""
    classical = {
        'variables': [],
        'arrays': [],
        'constants': [],
        'registers': []
    }

    # Find classical variables
    var_patterns = [
        r'bit\[(\d+)\]\s+(\w+)',
        r'int\[(\d+)\]\s+(\w+)',
        r'const\s+int\s+(\w+)\s*=\s*(\d+)'
    ]

    for pattern in var_patterns:
        matches = re.findall(pattern, content)
        if 'bit[' in pattern:
            classical['variables'].extend([{'type': f'bit[{m[0]}]', 'name': m[1]} for m in matches])
        elif 'int[' in pattern:
            classical['variables'].extend([{'type': f'int[{m[0]}]', 'name': m[1]} for m in matches])
        elif 'const' in pattern:
            classical['constants'].extend([{'name': m[0], 'value': m[1]} for m in matches])

    return classical

def display_analysis(analysis):
    """Display analysis results in a formatted way."""
    print("📊 ANALYSIS RESULTS")
    print("=" * 50)

    # File structure
    file_info = analysis['file_info']
    print(f"📄 File Structure:")
    print(f"   Lines: {file_info['total_lines']} (non-empty: {file_info['non_empty_lines']})")
    print(f"   Comments: {file_info['comment_lines']}")
    print(f"   Size: {file_info['file_size']} characters")
    print(f"   OpenQASM 3: {'✅' if file_info['has_openqasm3_header'] else '❌'}")

    # OpenQASM 3 features
    qasm3 = analysis['qasm3_features']
    print(f"\n🔧 OpenQASM 3 Features:")
    print(f"   Functions: {len(qasm3['functions'])} {qasm3['functions']}")
    print(f"   Structs: {len(qasm3['structs'])} {qasm3['structs']}")
    print(f"   Conditionals: {qasm3['conditionals']}")
    print(f"   Loops: {qasm3['loops']}")
    print(f"   Classical types: {len(set(qasm3['classical_types']))}")

    # AUX-QHE data
    aux = analysis['aux_qhe_data']
    print(f"\n🔑 AUX-QHE Data:")
    print(f"   Auxiliary states: {aux['auxiliary_states']}")
    print(f"   Layers: {len(aux['layers'])}")
    for layer_info in aux['layers']:
        layer_num = layer_info['layer']
        layer_size = layer_info['size']
        cross_terms = aux['cross_terms'].get(layer_num, 0)
        print(f"     Layer {layer_num}: {layer_size} terms, {cross_terms} cross-terms")

    if aux['qotp_keys']:
        print(f"   QOTP Keys: a={aux['qotp_keys']['a_init']}, b={aux['qotp_keys']['b_init']}")

    # Circuit operations
    ops = analysis['circuit_operations']
    print(f"\n⚙️  Circuit Operations:")
    print(f"   Total operations: {ops['total_operations']}")
    for gate, count in ops['quantum_gates'].items():
        print(f"     {gate}: {count}")
    print(f"   Measurements: {ops['measurements']}")

def interactive_qasm3_explorer():
    """Interactive explorer for OpenQASM 3 files."""
    print("🔍 Interactive OpenQASM 3 Explorer")
    print("=" * 50)

    # Available files
    qasm_files = [
        "/Users/giadang/my_qiskitenv/AUX-QHE/aux_qhe_keys.qasm",
        "/Users/giadang/my_qiskitenv/AUX-QHE/aux_qhe_circuit.qasm",
        "/Users/giadang/my_qiskitenv/AUX-QHE/test_openqasm3_output.qasm"
    ]

    print("Available OpenQASM 3 files:")
    for i, file_path in enumerate(qasm_files, 1):
        filename = Path(file_path).name
        exists = "✅" if Path(file_path).exists() else "❌"
        print(f"  {i}. {filename} {exists}")

    print("\nAnalyzing all available files...")

    analyses = {}
    for file_path in qasm_files:
        if Path(file_path).exists():
            print(f"\n{'='*60}")
            analysis = analyze_openqasm3_file(file_path)
            analyses[file_path] = analysis

    # Summary comparison
    print(f"\n{'='*20} COMPARISON SUMMARY {'='*20}")
    for file_path, analysis in analyses.items():
        if analysis:
            filename = Path(file_path).name
            aux_states = analysis['aux_qhe_data']['auxiliary_states']
            total_ops = analysis['circuit_operations']['total_operations']
            file_size = analysis['file_info']['file_size']

            print(f"📊 {filename}:")
            print(f"   Size: {file_size} chars, Aux states: {aux_states}, Operations: {total_ops}")

    return analyses

if __name__ == "__main__":
    interactive_qasm3_explorer()