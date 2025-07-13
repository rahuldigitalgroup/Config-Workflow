#!/usr/bin/env python3
"""
Local test script for SU2 Validation Pipeline
Simulates the GitHub Actions workflow locally
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse

def run_command(cmd, cwd=None):
    """Run a shell command"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, 
                              capture_output=True, text=True, check=True)
        print(f"OK: {cmd}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"FAIL: {cmd}")
        print(f"Error: {e.stderr}")
        return None

def setup_mock_vandv_repo():
    """Create mock VandV repository structure"""
    print("Setting up mock VandV repository...")
    
    vandv_path = Path("mock-vandv-repo")
    if vandv_path.exists():
        shutil.rmtree(vandv_path)
    
    # Create structure: ValidationCases/Basic/2DML/SA/Configuration1/Mesh1,Mesh2,Mesh3
    config_path = vandv_path / "ValidationCases" / "Basic" / "2DML" / "SA" / "Configuration1"
    
    for i in range(1, 4):
        mesh_path = config_path / f"Mesh{i}"
        mesh_path.mkdir(parents=True, exist_ok=True)
        
        # Create mock restart and mesh files
        (mesh_path / "restart.dat").write_text("Mock restart data")
        (mesh_path / "mesh.su2").write_text("Mock mesh data")
    
    print(f"Created mock VandV repo at {vandv_path}")
    return vandv_path

def test_automation_script(category, case_code, turb_model, configuration, author):
    """Test the Automation.py script locally"""
    print(f"\nTesting Automation.py locally...")
    print(f"Parameters: {category}/{case_code}/{turb_model}/{configuration}/{author}")
    
    # Setup paths
    main_path = Path("ValidationCases") / category / case_code / turb_model
    vandv_path = setup_mock_vandv_repo() / "ValidationCases" / category / case_code / turb_model
    output_path = Path("test_results") / f"{category}_{case_code}_{turb_model}_{configuration}_{author}"
    
    # Clean up previous results
    if output_path.exists():
        shutil.rmtree(output_path)
    
    # Run Automation.py
    cmd = [
        sys.executable, "ValidationCases/Automation.py",
        "--category", category,
        "--case-code", case_code,
        "--turbulence-model", turb_model,
        "--configuration", configuration,
        "--vandv-path", str(vandv_path),
        "--main-path", str(main_path),
        "--output-path", str(output_path)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Automation.py completed successfully")
        print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("Automation.py failed")
        print("Error:", e.stderr)
        print("Output:", e.stdout)
        return False

def test_plot_generation():
    """Test Plot.py script"""
    print(f"\nTesting Plot.py...")
    
    plot_script = Path("ValidationCases/Basic/2DML/SA/Configuration1/Plot.py")
    if not plot_script.exists():
        print(f"Plot.py not found at {plot_script}")
        return False
    
    # Change to the configuration directory
    config_dir = plot_script.parent
    original_cwd = os.getcwd()
    
    try:
        os.chdir(config_dir)
        result = subprocess.run([sys.executable, "Plot.py"], 
                              capture_output=True, text=True, check=True)
        print("Plot.py completed successfully")
        print("Output:", result.stdout)
        
        # Check if plots were created
        plots_dir = Path("plots")
        if plots_dir.exists():
            plot_files = list(plots_dir.glob("*.png"))
            print(f"Generated {len(plot_files)} plot files:")
            for plot_file in plot_files:
                print(f"  - {plot_file.name}")
        
        return True
    except subprocess.CalledProcessError as e:
        print("Plot.py failed")
        print("Error:", e.stderr)
        return False
    finally:
        os.chdir(original_cwd)

def test_combined_plots():
    """Test combined plots generation"""
    print(f"\nTesting combined plots generation...")
    
    # Create mock plot folders structure
    test_dir = Path("test_combined_plots")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    test_dir.mkdir()
    
    # Create mock plot folders
    (test_dir / "2DML_SA_Configuration1").mkdir()
    (test_dir / "2DML_SA_Configuration2").mkdir()
    (test_dir / "2DML_SST_Configuration1").mkdir()
    
    # Run combined plots script
    cmd = [
        sys.executable, "generate_combined_plots.py",
        "--case-code", "2DML",
        "--input-dir", str(test_dir),
        "--output-dir", str(test_dir / "combined_plots")
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("Combined plots generation completed")
        print("Output:", result.stdout)
        
        # Check generated files
        combined_dir = test_dir / "combined_plots"
        if combined_dir.exists():
            plot_files = list(combined_dir.glob("*.png"))
            print(f"Generated {len(plot_files)} combined plot files:")
            for plot_file in plot_files:
                print(f"  - {plot_file.name}")
        
        return True
    except subprocess.CalledProcessError as e:
        print("Combined plots generation failed")
        print("Error:", e.stderr)
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    dependencies = {
        'python3': 'python --version',
        'matplotlib': 'python -c "import matplotlib; print(matplotlib.__version__)"',
        'numpy': 'python -c "import numpy; print(numpy.__version__)"',
        'pandas': 'python -c "import pandas; print(pandas.__version__)"'
    }
    
    all_good = True
    for dep, cmd in dependencies.items():
        result = run_command(cmd)
        if result is None:
            print(f"MISSING: {dep}")
            all_good = False
        else:
            print(f"OK: {dep}: {result.strip()}")
    
    return all_good

def main():
    parser = argparse.ArgumentParser(description='Test SU2 Validation Pipeline locally')
    parser.add_argument('--category', default='Basic', help='Validation case category')
    parser.add_argument('--case-code', default='2DML', help='Validation case code')
    parser.add_argument('--turbulence-model', default='SA', help='Turbulence model')
    parser.add_argument('--configuration', default='Configuration1', help='Configuration')
    parser.add_argument('--author', default='TestUser', help='Author name')
    parser.add_argument('--skip-deps', action='store_true', help='Skip dependency check')
    
    args = parser.parse_args()
    
    print("SU2 Validation Pipeline - Local Test")
    print("=" * 50)
    
    # Check dependencies
    if not args.skip_deps:
        if not check_dependencies():
            print("\nSome dependencies are missing. Install them with:")
            print("pip install matplotlib numpy pandas")
            return 1
    
    # Test individual components
    success = True
    
    # Test 1: Plot generation
    if not test_plot_generation():
        success = False
    
    # Test 2: Automation script
    if not test_automation_script(args.category, args.case_code, 
                                args.turbulence_model, args.configuration, args.author):
        success = False
    
    # Test 3: Combined plots
    if not test_combined_plots():
        success = False
    
    # Summary
    print("\n" + "=" * 50)
    if success:
        print("All tests passed! Pipeline is ready for GitHub Actions.")
        print("\nNext steps:")
        print("1. Push changes to GitHub")
        print("2. Go to Actions -> 'SU2 Validation Pipeline'")
        print("3. Click 'Run workflow' and fill in parameters")
    else:
        print("Some tests failed. Check the errors above.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())