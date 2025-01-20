import glob
import os
import pytest
from io import StringIO
from contextlib import redirect_stdout

# test_folders =  glob.glob('tests**/', recursive=True)
# for folder in test_folders:
#     test_files = glob.glob(os.path.join(folder, 'test_*.py'))
#     if test_files:
#         pytest.main(test_files)

def run_tests_and_summarize():
    test_folders = glob.glob('tests**/', recursive=True)
    passed_tests = []
    failed_tests = []

    # Capture pytest output
    pytest_output = StringIO()
    with redirect_stdout(pytest_output):
        for folder in test_folders:
            test_files = glob.glob(os.path.join(folder, 'test_*.py'))
            for test_file in test_files:
                # Run pytest for each test file and capture results
                result = pytest.main([test_file])
                if result == 0:  # 0 means all tests passed
                    passed_tests.append(test_file)
                else:
                    failed_tests.append(test_file)

    # Extract failed test case names and error messages
    failed_test_details = []
    pytest_output.seek(0)
    lines = pytest_output.readlines()
    for i, line in enumerate(lines):
        if line.startswith("FAILED"):
            test_name = line.split("::")[0].strip()
            error_message = []
            # Collect relevant error lines following the failure
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == "" or lines[j].startswith("="):  # Stop on empty or pytest separator lines
                    break
                error_message.append(lines[j].strip())
            failed_test_details.append((test_name, "\n".join(error_message)))

    # Summary Report
    print("\nTest Summary")
    print("------------")
    for test in passed_tests:
        print(f"✅ {test}")
    for test, _ in failed_test_details:
        print(f"❌ {test}")

    # Aggregator
    print("\nAggregator:")
    print("------------")
    print(f"✅ Passed: {len(passed_tests)}")
    print(f"❌ Failed: {len(failed_test_details)}\n")

if __name__ == "__main__":
    run_tests_and_summarize()