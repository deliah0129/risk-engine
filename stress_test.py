#!/usr/bin/env python3
"""
Comprehensive stress testing suite for the risk engine simulation system.

This script validates:
- Sequential throughput and performance
- Concurrent session handling and thread safety
- State persistence reliability
- Deterministic behavior
- Error handling under stress
"""

import argparse
import json
import shutil
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

# =========================
# Paths
# =========================

ENGINE_ROOT = Path(__file__).resolve().parent
STATE_DIR = ENGINE_ROOT / "state"
LOG_DIR = ENGINE_ROOT / "logs"
RESULTS_DIR = ENGINE_ROOT / "stress_test_results"
BACKUP_DIR = ENGINE_ROOT / "state_backup"

RESULTS_DIR.mkdir(exist_ok=True)

# =========================
# Utilities
# =========================

def utc_now() -> str:
    """Return current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def backup_state() -> Path:
    """Backup state directory with timestamp."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    backup_path = BACKUP_DIR / f"backup_{timestamp}"
    
    if STATE_DIR.exists():
        shutil.copytree(STATE_DIR, backup_path)
        print(f"✓ Backed up state to: {backup_path}")
    else:
        print("✓ No existing state to backup")
        backup_path = None
    
    return backup_path

def restore_state(backup_path: Path) -> None:
    """Restore state from backup."""
    if backup_path is None:
        print("✓ No backup to restore")
        return
    
    if STATE_DIR.exists():
        shutil.rmtree(STATE_DIR)
    
    shutil.copytree(backup_path, STATE_DIR)
    print(f"✓ Restored state from: {backup_path}")

def clear_state() -> None:
    """Remove and recreate state directory."""
    if STATE_DIR.exists():
        shutil.rmtree(STATE_DIR)
    STATE_DIR.mkdir(exist_ok=True)
    print("✓ Cleared state directory")

def run_engine(timeout: int = 30) -> tuple:
    """
    Execute main.py and return (exec_time, success, output).
    
    Args:
        timeout: Maximum execution time in seconds
    
    Returns:
        tuple: (execution_time, success_bool, output_string)
    """
    start = time.time()
    try:
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=ENGINE_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        exec_time = time.time() - start
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return (exec_time, success, output)
    except subprocess.TimeoutExpired:
        exec_time = time.time() - start
        return (exec_time, False, f"TIMEOUT after {timeout}s")
    except Exception as e:
        exec_time = time.time() - start
        return (exec_time, False, f"ERROR: {str(e)}")

# =========================
# Test Suite 1: Sequential Throughput
# =========================

def test_sequential_throughput(iterations: int = 100) -> dict:
    """
    Run the engine sequentially for multiple iterations.
    
    Measures:
    - Execution time per run
    - Success/failure rates
    - Throughput (runs per second)
    - Statistical metrics
    """
    print("\n" + "=" * 70)
    print("TEST SUITE 1: SEQUENTIAL THROUGHPUT TEST")
    print("=" * 70)
    print(f"Iterations: {iterations}")
    print(f"Started at: {utc_now()}")
    print("-" * 70)
    
    clear_state()
    
    results = []
    exec_times = []
    successes = 0
    failures = 0
    
    for i in range(1, iterations + 1):
        exec_time, success, output = run_engine()
        
        results.append({
            "iteration": i,
            "exec_time": exec_time,
            "success": success,
            "output": output[:500]  # Truncate for storage
        })
        
        if success:
            successes += 1
            exec_times.append(exec_time)
            status = "✓"
        else:
            failures += 1
            status = "✗"
        
        print(f"{status} Run {i}/{iterations}: {exec_time:.3f}s")
    
    # Calculate statistics
    total_time = sum(exec_times) if exec_times else 0
    avg_time = statistics.mean(exec_times) if exec_times else 0
    median_time = statistics.median(exec_times) if exec_times else 0
    std_dev = statistics.stdev(exec_times) if len(exec_times) > 1 else 0
    min_time = min(exec_times) if exec_times else 0
    max_time = max(exec_times) if exec_times else 0
    throughput = successes / total_time if total_time > 0 else 0
    
    print("\n" + "-" * 70)
    print("RESULTS:")
    print(f"  Total runs:        {iterations}")
    print(f"  Successful:        {successes}")
    print(f"  Failed:            {failures}")
    print(f"  Success rate:      {(successes/iterations*100):.1f}%")
    print(f"  Average time:      {avg_time:.3f}s")
    print(f"  Median time:       {median_time:.3f}s")
    print(f"  Std deviation:     {std_dev:.3f}s")
    print(f"  Min time:          {min_time:.3f}s")
    print(f"  Max time:          {max_time:.3f}s")
    print(f"  Throughput:        {throughput:.2f} runs/sec")
    print("=" * 70)
    
    return {
        "test_name": "sequential_throughput",
        "iterations": iterations,
        "successes": successes,
        "failures": failures,
        "success_rate": successes / iterations * 100,
        "total_time": total_time,
        "avg_time": avg_time,
        "median_time": median_time,
        "std_dev": std_dev,
        "min_time": min_time,
        "max_time": max_time,
        "throughput": throughput,
        "results": results,
        "timestamp": utc_now()
    }

# =========================
# Test Suite 2: Concurrent Sessions
# =========================

def run_concurrent_session(session_id: int, iterations: int) -> dict:
    """Run a single concurrent session."""
    results = []
    successes = 0
    failures = 0
    
    for i in range(iterations):
        start = time.time()
        try:
            result = subprocess.run(
                [sys.executable, "main.py"],
                cwd=ENGINE_ROOT,
                capture_output=True,
                text=True,
                timeout=30
            )
            exec_time = time.time() - start
            success = result.returncode == 0
            
            if success:
                successes += 1
            else:
                failures += 1
            
            results.append({
                "iteration": i + 1,
                "exec_time": exec_time,
                "success": success
            })
        except Exception as e:
            exec_time = time.time() - start
            failures += 1
            results.append({
                "iteration": i + 1,
                "exec_time": exec_time,
                "success": False,
                "error": str(e)
            })
    
    return {
        "session_id": session_id,
        "iterations": iterations,
        "successes": successes,
        "failures": failures,
        "results": results
    }

def test_concurrent_sessions(sessions: int = 10, iterations_per_session: int = 10) -> dict:
    """
    Run multiple concurrent sessions to test concurrent execution handling.
    
    Measures:
    - Concurrent execution handling
    - Thread safety of test harness
    - Concurrent throughput
    
    Note: Sessions share the same state directory as the engine uses
    a fixed state location. This tests the engine's ability to handle
    concurrent invocations.
    """
    print("\n" + "=" * 70)
    print("TEST SUITE 2: CONCURRENT SESSIONS TEST")
    print("=" * 70)
    print(f"Sessions: {sessions}")
    print(f"Iterations per session: {iterations_per_session}")
    print(f"Total runs: {sessions * iterations_per_session}")
    print(f"Started at: {utc_now()}")
    print("-" * 70)
    
    clear_state()
    
    start_time = time.time()
    session_results = []
    
    with ThreadPoolExecutor(max_workers=sessions) as executor:
        futures = {
            executor.submit(run_concurrent_session, i, iterations_per_session): i
            for i in range(sessions)
        }
        
        for future in as_completed(futures):
            session_id = futures[future]
            try:
                result = future.result()
                session_results.append(result)
                print(f"✓ Session {session_id}: {result['successes']}/{result['iterations']} successful")
            except Exception as e:
                print(f"✗ Session {session_id} failed: {str(e)}")
                session_results.append({
                    "session_id": session_id,
                    "error": str(e),
                    "successes": 0,
                    "failures": iterations_per_session
                })
    
    total_time = time.time() - start_time
    
    # Aggregate results
    total_runs = sessions * iterations_per_session
    total_successes = sum(s.get("successes", 0) for s in session_results)
    total_failures = sum(s.get("failures", 0) for s in session_results)
    throughput = total_runs / total_time if total_time > 0 else 0
    
    print("\n" + "-" * 70)
    print("RESULTS:")
    print(f"  Total sessions:    {sessions}")
    print(f"  Total runs:        {total_runs}")
    print(f"  Successful:        {total_successes}")
    print(f"  Failed:            {total_failures}")
    print(f"  Success rate:      {(total_successes/total_runs*100):.1f}%")
    print(f"  Total time:        {total_time:.3f}s")
    print(f"  Concurrent throughput: {throughput:.2f} runs/sec")
    print("=" * 70)
    
    return {
        "test_name": "concurrent_sessions",
        "sessions": sessions,
        "iterations_per_session": iterations_per_session,
        "total_runs": total_runs,
        "total_successes": total_successes,
        "total_failures": total_failures,
        "success_rate": total_successes / total_runs * 100,
        "total_time": total_time,
        "throughput": throughput,
        "session_results": session_results,
        "timestamp": utc_now()
    }

# =========================
# Test Suite 3: State Persistence
# =========================

def test_state_persistence(cycles: int = 50) -> dict:
    """
    Test state save/load performance over many cycles.
    
    Measures:
    - Save time (write JSON)
    - Load time (read and parse JSON)
    - File sizes
    - Data integrity
    - I/O throughput
    """
    print("\n" + "=" * 70)
    print("TEST SUITE 3: STATE PERSISTENCE TEST")
    print("=" * 70)
    print(f"Cycles: {cycles}")
    print(f"Started at: {utc_now()}")
    print("-" * 70)
    
    clear_state()
    
    test_file = STATE_DIR / "stress_test_state.json"
    results = []
    save_times = []
    load_times = []
    file_sizes = []
    integrity_checks = 0
    
    for i in range(1, cycles + 1):
        # Create test state
        test_data = {
            "phase": i,
            "iteration": i,
            "timestamp": utc_now(),
            "payload": {
                "data": "x" * 1000,  # 1KB of data
                "values": list(range(100))
            }
        }
        
        # Measure save time
        start = time.time()
        test_file.write_text(json.dumps(test_data, indent=2), encoding="utf-8")
        save_time = time.time() - start
        save_times.append(save_time)
        
        # Measure file size
        file_size = test_file.stat().st_size
        file_sizes.append(file_size)
        
        # Measure load time
        start = time.time()
        loaded_data = json.loads(test_file.read_text(encoding="utf-8"))
        load_time = time.time() - start
        load_times.append(load_time)
        
        # Verify integrity
        integrity_ok = loaded_data == test_data
        if integrity_ok:
            integrity_checks += 1
            status = "✓"
        else:
            status = "✗"
        
        results.append({
            "cycle": i,
            "save_time": save_time,
            "load_time": load_time,
            "file_size": file_size,
            "integrity_ok": integrity_ok
        })
        
        if i % 10 == 0 or i == cycles:
            print(f"{status} Cycle {i}/{cycles}: save={save_time*1000:.2f}ms, load={load_time*1000:.2f}ms, size={file_size}B")
    
    # Calculate statistics
    avg_save = statistics.mean(save_times)
    avg_load = statistics.mean(load_times)
    avg_size = statistics.mean(file_sizes)
    total_bytes = sum(file_sizes)
    total_time = sum(save_times) + sum(load_times)
    io_throughput = total_bytes / total_time if total_time > 0 else 0
    
    print("\n" + "-" * 70)
    print("RESULTS:")
    print(f"  Total cycles:      {cycles}")
    print(f"  Integrity checks:  {integrity_checks}/{cycles} passed")
    print(f"  Avg save time:     {avg_save*1000:.2f}ms")
    print(f"  Avg load time:     {avg_load*1000:.2f}ms")
    print(f"  Avg file size:     {avg_size:.0f} bytes")
    print(f"  Total I/O time:    {total_time:.3f}s")
    print(f"  I/O throughput:    {io_throughput/1024:.2f} KB/s")
    print("=" * 70)
    
    # Cleanup
    if test_file.exists():
        test_file.unlink()
    
    return {
        "test_name": "state_persistence",
        "cycles": cycles,
        "integrity_passed": integrity_checks,
        "integrity_failed": cycles - integrity_checks,
        "avg_save_time": avg_save,
        "avg_load_time": avg_load,
        "avg_file_size": avg_size,
        "total_io_time": total_time,
        "io_throughput_bytes_per_sec": io_throughput,
        "results": results,
        "timestamp": utc_now()
    }

# =========================
# Test Suite 4: Determinism Verification
# =========================

def test_determinism(runs: int = 10) -> dict:
    """
    Verify that the engine produces identical outputs for identical inputs.
    
    Measures:
    - Output consistency
    - Deterministic behavior
    """
    print("\n" + "=" * 70)
    print("TEST SUITE 4: DETERMINISM VERIFICATION TEST")
    print("=" * 70)
    print(f"Runs: {runs}")
    print(f"Started at: {utc_now()}")
    print("-" * 70)
    
    clear_state()
    
    outputs = []
    exec_times = []
    
    for i in range(1, runs + 1):
        exec_time, success, output = run_engine()
        exec_times.append(exec_time)
        
        if success:
            outputs.append(output)
            print(f"✓ Run {i}/{runs}: {exec_time:.3f}s")
        else:
            print(f"✗ Run {i}/{runs}: FAILED")
            outputs.append(None)
    
    # Check determinism
    valid_outputs = [o for o in outputs if o is not None]
    
    if len(valid_outputs) < 2:
        is_deterministic = None
        print("\n✗ Not enough successful runs to verify determinism")
    else:
        first_output = valid_outputs[0]
        is_deterministic = all(o == first_output for o in valid_outputs)
        
        if is_deterministic:
            print(f"\n✓ ENGINE IS DETERMINISTIC: All {len(valid_outputs)} outputs are identical")
        else:
            print(f"\n✗ ENGINE IS NOT DETERMINISTIC: Outputs differ across runs")
    
    print("\n" + "-" * 70)
    print("RESULTS:")
    print(f"  Total runs:        {runs}")
    print(f"  Successful runs:   {len(valid_outputs)}")
    print(f"  Deterministic:     {is_deterministic}")
    print(f"  Avg exec time:     {statistics.mean(exec_times):.3f}s" if exec_times else "  N/A")
    print("=" * 70)
    
    return {
        "test_name": "determinism_verification",
        "runs": runs,
        "successful_runs": len(valid_outputs),
        "is_deterministic": is_deterministic,
        "avg_exec_time": statistics.mean(exec_times) if exec_times else 0,
        "timestamp": utc_now()
    }

# =========================
# Main Execution
# =========================

def save_results(results: dict, test_name: str) -> Path:
    """Save test results to JSON file."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    filename = f"stress_test_{test_name}_{timestamp}.json"
    filepath = RESULTS_DIR / filename
    
    filepath.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n✓ Results saved to: {filepath}")
    return filepath

def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive stress testing suite for the risk engine"
    )
    parser.add_argument(
        "--test",
        choices=["all", "sequential", "concurrent", "persistence", "determinism"],
        default="all",
        help="Which test suite to run (default: all)"
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=100,
        help="Number of iterations for sequential test (default: 100)"
    )
    parser.add_argument(
        "--sessions",
        type=int,
        default=10,
        help="Number of concurrent sessions (default: 10)"
    )
    parser.add_argument(
        "--cycles",
        type=int,
        default=50,
        help="Number of cycles for persistence test (default: 50)"
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=10,
        help="Number of runs for determinism test (default: 10)"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 70)
    print("RISK ENGINE - COMPREHENSIVE STRESS TEST SUITE")
    print("=" * 70)
    print(f"Started at: {utc_now()}")
    print(f"Test selection: {args.test}")
    print("=" * 70)
    
    # Backup existing state
    backup_path = backup_state()
    
    try:
        all_results = {}
        
        # Run selected tests
        if args.test in ["all", "sequential"]:
            result = test_sequential_throughput(args.iterations)
            all_results["sequential_throughput"] = result
        
        if args.test in ["all", "concurrent"]:
            result = test_concurrent_sessions(args.sessions)
            all_results["concurrent_sessions"] = result
        
        if args.test in ["all", "persistence"]:
            result = test_state_persistence(args.cycles)
            all_results["state_persistence"] = result
        
        if args.test in ["all", "determinism"]:
            result = test_determinism(args.runs)
            all_results["determinism_verification"] = result
        
        # Save combined results
        if all_results:
            final_results = {
                "test_suite": "comprehensive_stress_test",
                "timestamp": utc_now(),
                "configuration": {
                    "test": args.test,
                    "iterations": args.iterations,
                    "sessions": args.sessions,
                    "cycles": args.cycles,
                    "runs": args.runs
                },
                "results": all_results
            }
            save_results(final_results, args.test)
        
        print("\n" + "=" * 70)
        print("✓ ALL TESTS COMPLETED")
        print("=" * 70)
        
    finally:
        # Always restore state
        print("\n" + "-" * 70)
        print("CLEANUP:")
        print("-" * 70)
        restore_state(backup_path)
        
        # Cleanup backup
        if backup_path and backup_path.exists():
            shutil.rmtree(backup_path)
            print(f"✓ Removed backup: {backup_path}")
        
        print("=" * 70)

if __name__ == "__main__":
    main()
