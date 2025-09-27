#!/usr/bin/env python3
"""
Test Suite Runner - Python equivalent of TestNG suite management
"""
import sys
import subprocess
import argparse
from test_suites import TestSuites, TestSuiteRunner


def run_test_suite(suite_name: str, additional_args: list = None):
    """Run a specific test suite"""
    if suite_name not in TestSuites.get_available_suites():
        print(f"Error: Unknown test suite '{suite_name}'")
        print(f"Available suites: {', '.join(TestSuites.get_available_suites())}")
        return 1
    
    print(f"Running {suite_name} test suite...")
    print(f"Description: {TestSuites.get_suite_info()[suite_name]}")
    print("-" * 50)
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest']
    
    if suite_name == 'smoke':
        cmd.extend(['-m', 'smoke'])
    elif suite_name == 'regression':
        cmd.extend(['-m', 'regression'])
    elif suite_name == 'login':
        cmd.extend(['-m', 'login'])
    elif suite_name == 'cart':
        cmd.extend(['-m', 'cart'])
    elif suite_name == 'checkout':
        cmd.extend(['-m', 'checkout'])
    elif suite_name == 'navigation':
        cmd.extend(['-m', 'navigation'])
    elif suite_name == 'sort':
        cmd.extend(['-m', 'sort'])
    elif suite_name == 'critical':
        cmd.extend(['-m', 'critical'])
    elif suite_name == 'full':
        cmd.extend(['tests/'])
    
    # Add additional arguments
    if additional_args:
        cmd.extend(additional_args)
    
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run the command
    try:
        result = subprocess.run(cmd, check=True)
        print(f"\n✅ {suite_name} test suite completed successfully!")
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {suite_name} test suite failed!")
        return e.returncode


def list_suites():
    """List all available test suites"""
    print("Available Test Suites:")
    print("=" * 50)
    for suite in TestSuites.get_available_suites():
        info = TestSuites.get_suite_info()[suite]
        print(f"  {suite:12} - {info}")
    print()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Run test suites (Python equivalent of TestNG groups)')
    parser.add_argument('suite', nargs='?', help='Test suite to run')
    parser.add_argument('--list', action='store_true', help='List available test suites')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--incognito', action='store_true', help='Run in incognito mode')
    parser.add_argument('--env', choices=['dev', 'staging', 'prod'], default='dev', help='Environment to run against')
    parser.add_argument('--allure', action='store_true', help='Generate Allure report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.list:
        list_suites()
        return 0
    
    if not args.suite:
        print("Error: Please specify a test suite to run")
        print("Use --list to see available suites")
        return 1
    
    # Build additional arguments
    additional_args = []
    if args.headless:
        additional_args.append('--headless')
    if args.incognito:
        additional_args.append('--incognito')
    if args.allure:
        additional_args.extend(['--alluredir', 'allure-results'])
    if args.verbose:
        additional_args.append('-v')
    
    # Set environment
    import os
    os.environ['ENVIRONMENT'] = args.env
    
    return run_test_suite(args.suite, additional_args)


if __name__ == '__main__':
    sys.exit(main())

