#!/usr/bin/env python3
"""
Test runner script with environment support
"""
import os
import sys
import subprocess
import argparse
from config.simple_config import SimpleConfig


def run_tests(environment='dev', test_path='tests', markers=None, parallel=False, headless=False, incognito=False):
    """
    Run tests with specified environment configuration
    
    Args:
        environment: Environment to run tests against (dev, staging, prod)
        test_path: Path to test files or directories
        markers: Pytest markers to filter tests
        parallel: Enable parallel execution
        headless: Run browser in headless mode
        incognito: Run browser in incognito mode
    """
    
    # Set environment variable
    os.environ['ENVIRONMENT'] = environment
    
    # Get configuration for the environment
    config = SimpleConfig(environment)
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest', test_path]
    
    # Add environment-specific options
    if headless or config.headless:
        cmd.append('--headless')
    
    if incognito or config.incognito:
        cmd.append('--incognito')
    
    # Add markers if specified
    if markers:
        cmd.extend(['-m', markers])
    
    # Add parallel execution if enabled
    if parallel:
        workers = config.parallel_workers
        cmd.extend(['-n', str(workers)])
    
    # Add Allure reporting
    cmd.extend(['--alluredir', 'allure-results'])
    
    # Add verbose output
    cmd.append('-v')
    
    # Add environment info
    cmd.extend(['--env', environment])
    
    print(f"Running tests for environment: {environment}")
    print(f"Command: {' '.join(cmd)}")
    print(f"Base URL: {config.base_url}")
    print(f"Browser: {config.browser}")
    print(f"Headless: {config.headless}")
    print(f"Parallel workers: {config.parallel_workers}")
    print("-" * 50)
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\nTests completed successfully for {environment} environment")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\nTests failed for {environment} environment")
        return e.returncode


def main():
    """Main function to handle command line arguments"""
    parser = argparse.ArgumentParser(description='Run SauceDemo automation tests')
    parser.add_argument('--env', choices=['dev', 'staging', 'prod'], default='dev',
                       help='Environment to run tests against')
    parser.add_argument('--path', default='tests',
                       help='Path to test files or directories')
    parser.add_argument('--markers', help='Pytest markers to filter tests')
    parser.add_argument('--parallel', action='store_true',
                       help='Enable parallel execution')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode')
    parser.add_argument('--incognito', action='store_true',
                       help='Run browser in incognito mode')
    
    args = parser.parse_args()
    
    return run_tests(
        environment=args.env,
        test_path=args.path,
        markers=args.markers,
        parallel=args.parallel,
        headless=args.headless,
        incognito=args.incognito
    )


if __name__ == '__main__':
    sys.exit(main())


