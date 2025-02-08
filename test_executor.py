import io
import os
import shutil
import sys
import time
from pathlib import Path

import pytest
from prettytable import PrettyTable


class TestResultCollector:
    def __init__(self):
        self.results_by_file = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            self.total_tests += 1
            file_path = report.nodeid.split("::")[0]
            test_name = report.nodeid.split("::")[-1]
            
            if file_path not in self.results_by_file:
                self.results_by_file[file_path] = {
                    "passed": True,
                    "failed_tests": [],
                    "all_tests": []
                }
            
            self.results_by_file[file_path]["all_tests"].append(test_name)
            
            if report.failed:
                self.results_by_file[file_path]["passed"] = False
                self.results_by_file[file_path]["failed_tests"].append(test_name)
                self.failed_tests += 1
            elif report.skipped:
                self.skipped_tests += 1
            else:
                self.passed_tests += 1

def find_test_files():
    """Find all test files and directories in the project"""
    test_paths = []
    for item in Path('.').glob('tests_*'):
        if item.is_dir():
            test_paths.extend(str(f) for f in item.glob('test_*.py'))
    return test_paths

def display_detailed_results(collector):
    # Get terminal size
    terminal_width = shutil.get_terminal_size().columns
    
    table = PrettyTable()
    table.field_names = ["Test Name", "Failed Functions", "Passed", "Failed"]
    
    # Set colors for ANSI terminals
    GREEN = "\033[92m"
    RED = "\033[91m"
    RESET = "\033[0m"
    
    # Configure table styling
    table.align = "l"  # Left align text
    table.max_width = terminal_width  # Set max width to terminal width
    table.border = True
    table.hrules = True
    
    # Calculate optimal column widths
    name_width = int(terminal_width * 0.3)
    failed_func_width = int(terminal_width * 0.4)
    count_width = int(terminal_width * 0.15)
    
    table._max_width = {
        "Test Name": name_width,
        "Failed Functions": failed_func_width,
        "Passed": count_width,
        "Failed": count_width
    }
    
    for file_path, result in collector.results_by_file.items():
        file_name = os.path.basename(file_path)
        # Color the filename based on status
        colored_name = f"{GREEN}{file_name}{RESET}" if result["passed"] else f"{RED}{file_name}{RESET}"
        
        failed_tests = ", ".join(result["failed_tests"]) if result["failed_tests"] else "-"
        passed_count = len([t for t in result.get("all_tests", []) if t not in result["failed_tests"]])
        failed_count = len(result["failed_tests"])
        
        # Color the counts
        passed_display = f"{GREEN}{passed_count}{RESET}"
        failed_display = f"{RED}{failed_count}{RESET}" if failed_count > 0 else f"{failed_count}"
        
        # Truncate failed_tests if too long
        if len(failed_tests) > failed_func_width:
            failed_tests = failed_tests[:failed_func_width-3] + "..."
        
        table.add_row([
            colored_name,
            failed_tests,
            passed_display,
            failed_display
        ])
    
    print("\nTest Results:")
    print(table)

def display_test_results(total_tests, passed, failed, skipped, execution_time):
    table = PrettyTable()
    table.field_names = ["Total Tests", "Passed", "Failed", "Skipped", "Execution Time(s)"]
    table.add_row([total_tests, passed, failed, skipped, f"{execution_time:.2f}"])
    print("\nTest Execution Summary:")
    print(table)

def main():
    test_files = find_test_files()
    if not test_files:
        print("No test files found!")
        return
    
    # Capture and suppress pytest output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    sys.stderr = captured_output
    
    collector = TestResultCollector()
    pytest_args = test_files + ["-v", "--tb=short", "-p", "no:warnings", "--cache-clear"]
    
    start_time = time.time()
    exit_code = pytest.main(pytest_args, plugins=[collector])
    end_time = time.time()
    
    # Restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    
    # Display detailed results
    display_detailed_results(collector)
    
    # Remove the summary table display
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

if __name__ == "__main__":
    main()