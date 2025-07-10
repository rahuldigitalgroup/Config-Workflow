# SU2 Validation Pipeline Workflows

This repository contains GitHub Actions workflows for automating the SU2 validation process as described in the problem statement.

## Workflow Files

### 1. `su2_validation.yml` - Main Validation Pipeline
The primary workflow that handles the complete SU2 validation process:
- Parses configuration files
- Collects user inputs for validation parameters
- Copies files between repositories
- Builds and runs SU2 simulations
- Generates plots and collects results
- Deploys results to the website repository

### 2. `config_input.yml` - Configuration Input Handler
A comprehensive workflow that:
- Accepts user inputs for all configuration parameters
- Updates configuration files with user-provided values
- Copies configurations to all mesh folders
- Executes the complete validation pipeline
- Stores results as artifacts and deploys to website

### 3. Dynamic Workflow Generation
Use the Python script to generate workflows based on any configuration file:

```bash
python .github/scripts/generate_dynamic_workflow.py template_config.cfg
```

## Usage Instructions

### Step 1: Prepare Repository Structure
Ensure your repositories follow this structure:

**SU2 Main Repository:**
```
VandV/
├── Basic/
│   └── 2DML/
│       ├── config.cfg
│       ├── Plot.py
│       ├── Exp_data.dat
│       ├── Mesh1/ (empty)
│       ├── Mesh2/ (empty)
│       └── ...
├── Extended/
│   └── ...
└── Automation.py
```

**SU2 VandV Repository:**
```
VandV/
├── Basic/
│   └── 2DML/
│       ├── Mesh1/
│       │   ├── restart.dat
│       │   └── mesh.su2
│       ├── Mesh2/
│       │   ├── restart.dat
│       │   └── mesh.su2
│       └── ...
└── Extended/
    └── ...
```

### Step 2: Run the Validation Pipeline

1. **Go to Actions tab** in your GitHub repository
2. **Select "Configure Validation Parameters"** workflow
3. **Click "Run workflow"**
4. **Fill in the required parameters:**
   - **Category:** Basic or Extended
   - **Case Name:** e.g., "2D Mixing Layer"
   - **Case Code:** e.g., "2DML"
   - **Configuration Parameters:** Modify any SU2 parameters as needed

### Step 3: Monitor Execution
The workflow will:
1. ✅ Update configuration files with your inputs
2. ✅ Copy files between repositories
3. ✅ Build SU2 with dependencies
4. ✅ Run simulations on all meshes
5. ✅ Generate plots
6. ✅ Store results as artifacts
7. ✅ Deploy plots to website repository

### Step 4: Access Results
- **Simulation Results:** Download from GitHub Actions artifacts
- **Plots:** Available in the SU2-Website repository under a new branch named after your validation case

## Configuration Parameters

The workflow accepts all standard SU2 configuration parameters including:

- `SOLVER` - Solver type (RANS, EULER, etc.)
- `KIND_TURB_MODEL` - Turbulence model (SA, SST, etc.)
- `MACH_NUMBER` - Mach number
- `AOA` - Angle of attack
- `FREESTREAM_TEMPERATURE` - Freestream temperature
- `FREESTREAM_PRESSURE` - Freestream pressure
- `CFL_NUMBER` - CFL number
- `ITER` - Number of iterations
- `CONV_RESIDUAL_MINVAL` - Convergence criteria
- And many more...

## Repository Requirements

### Secrets Required:
- `GITHUB_TOKEN` - For accessing other repositories

### Repository Access:
- SU2 Main Repository (current)
- SU2-VandV Repository (mesh and restart files)
- SU2-Website Repository (for result deployment)

## Troubleshooting

### Common Issues:
1. **Config file not found:** Ensure the validation case exists in the specified category
2. **Build failures:** Check that all dependencies are properly installed
3. **Missing files:** Verify that mesh and restart files exist in the VandV repository
4. **Permission errors:** Ensure GITHUB_TOKEN has appropriate permissions

### Logs:
Check the GitHub Actions logs for detailed error messages and execution status.

## Customization

To modify the workflow for your specific needs:
1. Edit the workflow YAML files
2. Update the Python script for different parsing logic
3. Modify the build and installation steps as needed
4. Adjust the result collection and deployment process

## Support

For issues or questions about the validation pipeline, please check:
1. GitHub Actions logs
2. Repository structure requirements
3. Configuration file format
4. Dependencies and build requirements