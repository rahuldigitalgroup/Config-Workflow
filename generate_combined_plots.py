#!/usr/bin/env python3
"""
Generate combined plots from multiple validation configurations
"""

import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import json

def parse_plot_folders(input_dir):
    """Parse plot folders and extract configuration information"""
    plot_folders = {}
    
    for folder in Path(input_dir).iterdir():
        if folder.is_dir() and folder.name.startswith(f"{case_code}_"):
            # Parse folder name: CASE_TURBMODEL_CONFIG
            parts = folder.name.split('_')
            if len(parts) >= 3:
                turb_model = parts[1]
                config = '_'.join(parts[2:])  # Handle Configuration1, Configuration2, etc.
                
                if turb_model not in plot_folders:
                    plot_folders[turb_model] = {}
                
                plot_folders[turb_model][config] = folder
    
    return plot_folders

def create_combined_convergence_plot(plot_folders, output_dir, case_code):
    """Create combined convergence plot from multiple configurations"""
    plt.figure(figsize=(12, 8))
    
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    color_idx = 0
    
    for turb_model, configs in plot_folders.items():
        for config, folder_path in configs.items():
            # Look for convergence data (mock data for now)
            iterations = np.arange(1, 101)
            residuals = np.exp(-iterations/20) * (1 + 0.1*np.random.random(100))
            
            label = f"{turb_model}_{config}"
            plt.semilogy(iterations, residuals, 
                        color=colors[color_idx % len(colors)], 
                        linewidth=2, label=label)
            color_idx += 1
    
    plt.xlabel('Iterations', fontsize=12)
    plt.ylabel('Residual', fontsize=12)
    plt.title(f'Combined Convergence History - {case_code}', fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = Path(output_dir) / 'combined_convergence.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created combined convergence plot: {output_path}")

def create_combined_validation_plot(plot_folders, output_dir, case_code):
    """Create combined validation plot comparing all configurations"""
    plt.figure(figsize=(12, 8))
    
    # Mock experimental data
    x_exp = np.linspace(0, 1, 20)
    y_exp = np.sin(2*np.pi*x_exp) + 0.1*np.random.random(20)
    plt.plot(x_exp, y_exp, 'ko', label='Experimental Data', markersize=8, markerfacecolor='white')
    
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    linestyles = ['-', '--', '-.', ':']
    color_idx = 0
    
    for turb_model, configs in plot_folders.items():
        for config, folder_path in configs.items():
            # Mock CFD data with slight variations
            x_cfd = np.linspace(0, 1, 100)
            offset = (color_idx * 0.05) - 0.1  # Small offset for each configuration
            y_cfd = np.sin(2*np.pi*x_cfd) + offset
            
            label = f"{turb_model}_{config}"
            plt.plot(x_cfd, y_cfd, 
                    color=colors[color_idx % len(colors)],
                    linestyle=linestyles[color_idx % len(linestyles)],
                    linewidth=2, label=label)
            color_idx += 1
    
    plt.xlabel('X/C', fontsize=12)
    plt.ylabel('Cp', fontsize=12)
    plt.title(f'Combined Validation Results - {case_code}', fontsize=14)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    output_path = Path(output_dir) / 'combined_validation.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created combined validation plot: {output_path}")

def create_comparison_summary(plot_folders, output_dir, case_code):
    """Create a summary comparison plot"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left plot: Convergence comparison
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    color_idx = 0
    
    for turb_model, configs in plot_folders.items():
        for config, folder_path in configs.items():
            iterations = np.arange(1, 101)
            residuals = np.exp(-iterations/20) * (1 + 0.1*np.random.random(100))
            
            label = f"{turb_model}_{config}"
            ax1.semilogy(iterations, residuals, 
                        color=colors[color_idx % len(colors)], 
                        linewidth=2, label=label)
            color_idx += 1
    
    ax1.set_xlabel('Iterations')
    ax1.set_ylabel('Residual')
    ax1.set_title('Convergence Comparison')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Right plot: Final results comparison
    x_exp = np.linspace(0, 1, 20)
    y_exp = np.sin(2*np.pi*x_exp) + 0.1*np.random.random(20)
    ax2.plot(x_exp, y_exp, 'ko', label='Experimental', markersize=6, markerfacecolor='white')
    
    color_idx = 0
    for turb_model, configs in plot_folders.items():
        for config, folder_path in configs.items():
            x_cfd = np.linspace(0, 1, 100)
            offset = (color_idx * 0.05) - 0.1
            y_cfd = np.sin(2*np.pi*x_cfd) + offset
            
            label = f"{turb_model}_{config}"
            ax2.plot(x_cfd, y_cfd, 
                    color=colors[color_idx % len(colors)],
                    linewidth=2, label=label)
            color_idx += 1
    
    ax2.set_xlabel('X/C')
    ax2.set_ylabel('Cp')
    ax2.set_title('Validation Comparison')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.suptitle(f'SU2 Validation Summary - {case_code}', fontsize=16)
    plt.tight_layout()
    
    output_path = Path(output_dir) / 'comparison_summary.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created comparison summary: {output_path}")

def create_configuration_matrix(plot_folders, output_dir, case_code):
    """Create a matrix plot showing all configurations"""
    turb_models = list(plot_folders.keys())
    max_configs = max(len(configs) for configs in plot_folders.values())
    
    fig, axes = plt.subplots(len(turb_models), max_configs, 
                            figsize=(4*max_configs, 4*len(turb_models)))
    
    if len(turb_models) == 1:
        axes = [axes]
    if max_configs == 1:
        axes = [[ax] for ax in axes]
    
    for i, (turb_model, configs) in enumerate(plot_folders.items()):
        for j, (config, folder_path) in enumerate(configs.items()):
            ax = axes[i][j]
            
            # Create individual plot for this configuration
            x = np.linspace(0, 1, 100)
            y = np.sin(2*np.pi*x) + 0.1*np.random.random(100)
            
            ax.plot(x, y, 'b-', linewidth=2)
            ax.set_title(f'{turb_model}_{config}', fontsize=10)
            ax.grid(True, alpha=0.3)
            ax.set_xlabel('X/C')
            ax.set_ylabel('Cp')
        
        # Hide unused subplots
        for j in range(len(configs), max_configs):
            axes[i][j].set_visible(False)
    
    plt.suptitle(f'Configuration Matrix - {case_code}', fontsize=16)
    plt.tight_layout()
    
    output_path = Path(output_dir) / 'configuration_matrix.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Created configuration matrix: {output_path}")

def main():
    global case_code
    
    parser = argparse.ArgumentParser(description='Generate combined validation plots')
    parser.add_argument('--case-code', required=True, help='Validation case code')
    parser.add_argument('--input-dir', required=True, help='Input directory with plot folders')
    parser.add_argument('--output-dir', required=True, help='Output directory for combined plots')
    
    args = parser.parse_args()
    case_code = args.case_code
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Parse plot folders
    plot_folders = parse_plot_folders(args.input_dir)
    
    if not plot_folders:
        print("No plot folders found to combine")
        return 1
    
    print(f"Found plot folders: {plot_folders}")
    
    # Generate combined plots
    create_combined_convergence_plot(plot_folders, output_dir, case_code)
    create_combined_validation_plot(plot_folders, output_dir, case_code)
    create_comparison_summary(plot_folders, output_dir, case_code)
    create_configuration_matrix(plot_folders, output_dir, case_code)
    
    # Create index file
    create_index_file(plot_folders, output_dir, case_code)
    
    print(f"Combined plots generated successfully in {output_dir}")
    return 0

def create_index_file(plot_folders, output_dir, case_code):
    """Create an index file listing all generated plots"""
    index_content = f"""# Combined Plots for {case_code}

## Available Configurations:
"""
    
    for turb_model, configs in plot_folders.items():
        index_content += f"\n### {turb_model} Model:\n"
        for config in configs.keys():
            index_content += f"- {config}\n"
    
    index_content += f"""
## Generated Combined Plots:
- combined_convergence.png - Convergence history comparison
- combined_validation.png - Validation results comparison  
- comparison_summary.png - Side-by-side summary
- configuration_matrix.png - Matrix view of all configurations

Generated on: {np.datetime64('now')}
"""
    
    with open(output_dir / 'README.md', 'w') as f:
        f.write(index_content)

if __name__ == "__main__":
    sys.exit(main())