#!/usr/bin/env python3
"""
Parallel Agent Test - Tests concurrent execution of multiple LLM agents
Verifies file-based communication doesn't conflict
"""

import sys
import os
import time
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from glm_direct import call_glm_direct
    GLM_AVAILABLE = True
except ImportError:
    GLM_AVAILABLE = False

try:
    from codex_wrapper import call_codex
    CODEX_AVAILABLE = True
except ImportError:
    CODEX_AVAILABLE = False

# Test output directory
TEST_OUTPUT_DIR = Path.cwd() / ".agents" / "parallel_test"
TEST_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def run_glm_task(task_id, prompt):
    """Run a GLM task with status tracking."""
    start_time = time.time()
    status_file = TEST_OUTPUT_DIR / f"glm_{task_id}.status"

    # Write initial status
    status_data = {
        "agent": "glm",
        "task_id": task_id,
        "status": "running",
        "started_at": datetime.now().isoformat()
    }
    status_file.write_text(json.dumps(status_data, indent=2))

    result = {
        "agent": "glm",
        "task_id": task_id,
        "success": False,
        "output": "",
        "error": None,
        "duration": 0
    }

    try:
        if GLM_AVAILABLE:
            glm_result = call_glm_direct(prompt, [])
            result["success"] = glm_result.get("success", False)
            result["output"] = glm_result.get("output", "")
            result["error"] = glm_result.get("error")
        else:
            result["success"] = False
            result["error"] = "GLM wrapper not available"

    except Exception as e:
        result["error"] = str(e)

    result["duration"] = time.time() - start_time

    # Write result
    result_file = TEST_OUTPUT_DIR / f"glm_{task_id}_result.json"
    result_file.write_text(json.dumps(result, indent=2))

    # Update status
    status_data["status"] = "completed" if result["success"] else "error"
    status_data["completed_at"] = datetime.now().isoformat()
    status_data["duration"] = result["duration"]
    status_file.write_text(json.dumps(status_data, indent=2))

    return result


def run_codex_task(task_id, prompt):
    """Run a Codex task with status tracking."""
    start_time = time.time()
    status_file = TEST_OUTPUT_DIR / f"codex_{task_id}.status"

    # Write initial status
    status_data = {
        "agent": "codex",
        "task_id": task_id,
        "status": "running",
        "started_at": datetime.now().isoformat()
    }
    status_file.write_text(json.dumps(status_data, indent=2))

    result = {
        "agent": "codex",
        "task_id": task_id,
        "success": False,
        "output": "",
        "error": None,
        "duration": 0
    }

    try:
        if CODEX_AVAILABLE:
            codex_result = call_codex(prompt, [])
            result["success"] = codex_result.get("success", False)
            result["output"] = codex_result.get("output", "")
            result["error"] = codex_result.get("error")
        else:
            result["success"] = False
            result["error"] = "Codex wrapper not available"

    except Exception as e:
        result["error"] = str(e)

    result["duration"] = time.time() - start_time

    # Write result
    result_file = TEST_OUTPUT_DIR / f"codex_{task_id}_result.json"
    result_file.write_text(json.dumps(result, indent=2))

    # Update status
    status_data["status"] = "completed" if result["success"] else "error"
    status_data["completed_at"] = datetime.now().isoformat()
    status_data["duration"] = result["duration"]
    status_file.write_text(json.dumps(status_data, indent=2))

    return result


def run_parallel_test():
    """Test running GLM and Codex in parallel."""
    print("=" * 60)
    print("Parallel Agent Execution Test")
    print("=" * 60)
    print()

    # Check availability
    print("Agent Availability:")
    print(f"  GLM: {'Available' if GLM_AVAILABLE else 'Not Available'}")
    print(f"  Codex: {'Available' if CODEX_AVAILABLE else 'Not Available'}")
    print()

    if not GLM_AVAILABLE and not CODEX_AVAILABLE:
        print("ERROR: No agents available for testing")
        return False

    # Define test tasks
    tasks = []

    if GLM_AVAILABLE:
        tasks.append(("glm", 1, "Write a haiku about parallel computing."))
        tasks.append(("glm", 2, "What is 2 + 2? Answer in one word."))

    if CODEX_AVAILABLE:
        tasks.append(("codex", 1, "Write a haiku about distributed systems."))
        tasks.append(("codex", 2, "What is 3 + 3? Answer in one word."))

    print(f"Running {len(tasks)} tasks in parallel...")
    print()

    # Clear previous test results
    for f in TEST_OUTPUT_DIR.glob("*_result.json"):
        f.unlink()
    for f in TEST_OUTPUT_DIR.glob("*.status"):
        f.unlink()

    # Run tasks in parallel
    start_time = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=4) as executor:
        future_to_task = {}

        for agent, task_id, prompt in tasks:
            if agent == "glm":
                future = executor.submit(run_glm_task, task_id, prompt)
            else:
                future = executor.submit(run_codex_task, task_id, prompt)
            future_to_task[future] = (agent, task_id, prompt)

        for future in as_completed(future_to_task):
            agent, task_id, prompt = future_to_task[future]
            try:
                result = future.result()
                results.append(result)
                print(f"  [{agent.upper()} Task {task_id}] Completed in {result['duration']:.2f}s - {'SUCCESS' if result['success'] else 'FAILED'}")
            except Exception as e:
                print(f"  [{agent.upper()} Task {task_id}] Exception: {e}")

    total_duration = time.time() - start_time

    print()
    print("=" * 60)
    print("Test Results")
    print("=" * 60)
    print()

    # Summary
    successful = sum(1 for r in results if r["success"])
    print(f"Total tasks: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")
    print(f"Total duration: {total_duration:.2f}s")
    print()

    # Check for file conflicts
    print("File Communication Check:")
    result_files = list(TEST_OUTPUT_DIR.glob("*_result.json"))
    status_files = list(TEST_OUTPUT_DIR.glob("*.status"))

    print(f"  Result files created: {len(result_files)}")
    print(f"  Status files created: {len(status_files)}")

    # Verify no conflicts (each file should be unique)
    result_names = [f.name for f in result_files]
    status_names = [f.name for f in status_files]

    if len(result_names) == len(set(result_names)):
        print("  No file conflicts detected: PASS")
    else:
        print("  WARNING: Duplicate file names detected!")

    print()

    # Detailed results
    print("Detailed Results:")
    for r in results:
        status_icon = "OK" if r["success"] else "X"
        print(f"  [{status_icon}] {r['agent'].upper()} Task {r['task_id']}: {r['duration']:.2f}s")
        if r.get("error"):
            print(f"      Error: {r['error']}")
        if r.get("output"):
            preview = r["output"][:100].replace("\n", " ")
            print(f"      Output: {preview}...")

    print()
    print("=" * 60)

    # Check if sequential would have taken longer
    individual_times = [r["duration"] for r in results]
    sequential_time = sum(individual_times)
    parallel_time = total_duration

    print("Performance Analysis:")
    print(f"  Sequential time estimate: {sequential_time:.2f}s")
    print(f"  Parallel time actual: {parallel_time:.2f}s")
    if parallel_time < sequential_time:
        speedup = sequential_time / parallel_time
        print(f"  Speedup: {speedup:.2f}x")
    print()

    return successful == len(results)


def test_file_conflicts():
    """Test that file-based communication doesn't have conflicts."""
    print("=" * 60)
    print("File Conflict Test")
    print("=" * 60)
    print()

    import threading

    conflicts = []
    files_created = []

    def write_file(thread_id, iteration):
        """Simulate concurrent file writes."""
        filename = TEST_OUTPUT_DIR / f"thread_{thread_id}_iter_{iteration}.json"
        data = {
            "thread_id": thread_id,
            "iteration": iteration,
            "timestamp": datetime.now().isoformat(),
            "data": "x" * 100  # 100 bytes
        }

        try:
            # Check if file already exists (conflict)
            if filename.exists():
                conflicts.append(filename.name)
                return False

            # Write file
            filename.write_text(json.dumps(data, indent=2))
            files_created.append(filename.name)

            # Small delay to increase chance of race condition
            time.sleep(0.001)

            return True
        except Exception as e:
            conflicts.append(f"{filename.name}: {e}")
            return False

    # Run many threads writing to different files
    print("Running 50 threads with 10 iterations each...")
    print()

    threads = []
    for thread_id in range(50):
        for iteration in range(10):
            t = threading.Thread(target=write_file, args=(thread_id, iteration))
            threads.append(t)
            t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    print(f"Files created: {len(files_created)}")
    print(f"Conflicts detected: {len(conflicts)}")

    if conflicts:
        print("Conflicts:")
        for c in conflicts[:10]:  # Show first 10
            print(f"  - {c}")
    else:
        print("No conflicts detected: PASS")

    print()

    # Clean up test files
    for f in TEST_OUTPUT_DIR.glob("thread_*_iter_*.json"):
        f.unlink()

    return len(conflicts) == 0


def main():
    """Main entry point."""
    # Clean up from previous tests
    for f in TEST_OUTPUT_DIR.glob("*_result.json"):
        f.unlink()
    for f in TEST_OUTPUT_DIR.glob("glm_*.status"):
        f.unlink()
    for f in TEST_OUTPUT_DIR.glob("codex_*.status"):
        f.unlink()

    # Run parallel test
    parallel_success = run_parallel_test()

    # Run file conflict test
    conflict_success = test_file_conflicts()

    # Overall result
    print("=" * 60)
    print("Overall Test Result:")
    if parallel_success and conflict_success:
        print("  ALL TESTS PASSED")
        print("=" * 60)
        return 0
    else:
        print("  SOME TESTS FAILED")
        if not parallel_success:
            print("  - Parallel execution test failed")
        if not conflict_success:
            print("  - File conflict test failed")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
