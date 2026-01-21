"""
Stress test for consequence extraction system.

Tests the performance and correctness of consequence extraction
under heavy load with many actors and events.
"""

import sys
from pathlib import Path
import time
import random
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from derived.consequence_extractor import extract_consequences


def generate_stress_events(
    num_actors: int = 50,
    num_turns: int = 100,
    events_per_turn: int = 20
) -> List[Dict[str, Any]]:
    """
    Generate a large synthetic event stream for stress testing.
    
    Args:
        num_actors: Number of different actors to simulate
        num_turns: Number of turns to simulate
        events_per_turn: Average number of events per turn
        
    Returns:
        List of event dictionaries
    """
    events = []
    actors = [f"Actor_{i:03d}" for i in range(num_actors)]
    
    for turn in range(1, num_turns + 1):
        # Generate events for this turn
        for _ in range(events_per_turn):
            actor = random.choice(actors)
            
            # Simulate event outcomes with some randomness
            success_rate = 0.6 + random.uniform(-0.2, 0.2)
            ok = random.random() < success_rate
            
            delta = random.uniform(-5.0, 10.0) if ok else random.uniform(-10.0, 2.0)
            cost = random.uniform(0.5, 2.0)
            magnitude = abs(delta)
            
            events.append({
                "turn": turn,
                "actor": actor,
                "ok": ok,
                "delta": delta,
                "cost": cost,
                "magnitude": magnitude,
            })
    
    return events


def run_stress_test(
    num_actors: int = 50,
    num_turns: int = 100,
    events_per_turn: int = 20,
    window: int = 10
) -> Dict[str, Any]:
    """
    Run stress test on consequence extraction.
    
    Returns:
        Dictionary with test results including timing and statistics
    """
    print(f"\n{'='*70}")
    print(f"STRESS TEST: Consequence Extraction")
    print(f"{'='*70}")
    print(f"Configuration:")
    print(f"  - Actors: {num_actors}")
    print(f"  - Turns: {num_turns}")
    print(f"  - Events per turn: {events_per_turn}")
    print(f"  - Total events: {num_turns * events_per_turn}")
    print(f"  - Window size: {window}")
    print(f"{'='*70}\n")
    
    # Generate test data
    print("Generating synthetic event stream...")
    start_gen = time.time()
    events = generate_stress_events(num_actors, num_turns, events_per_turn)
    gen_time = time.time() - start_gen
    print(f"  Generated {len(events)} events in {gen_time:.3f}s\n")
    
    # Run consequence extraction
    print("Running consequence extraction...")
    start_extract = time.time()
    results = extract_consequences(
        events,
        current_turn=num_turns,
        window=window
    )
    extract_time = time.time() - start_extract
    print(f"  Completed in {extract_time:.3f}s\n")
    
    # Analyze results
    print("Analyzing results...")
    tags_distribution: Dict[str, int] = {}
    for state in results.values():
        for tag in state.tags:
            tags_distribution[tag] = tags_distribution.get(tag, 0) + 1
    
    # Compute statistics
    stats = {
        "num_actors": num_actors,
        "num_turns": num_turns,
        "events_per_turn": events_per_turn,
        "total_events": len(events),
        "window": window,
        "generation_time_s": gen_time,
        "extraction_time_s": extract_time,
        "total_time_s": gen_time + extract_time,
        "actors_analyzed": len(results),
        "events_per_second": len(events) / extract_time if extract_time > 0 else 0,
        "tags_distribution": tags_distribution,
    }
    
    return stats


def print_stress_test_results(stats: Dict[str, Any]) -> None:
    """
    Print formatted stress test results.
    
    Args:
        stats: Dictionary with test statistics
    """
    print(f"\n{'='*70}")
    print(f"STRESS TEST RESULTS")
    print(f"{'='*70}\n")
    
    print("Performance Metrics:")
    print(f"  - Event generation time: {stats['generation_time_s']:.3f}s")
    print(f"  - Consequence extraction time: {stats['extraction_time_s']:.3f}s")
    print(f"  - Total execution time: {stats['total_time_s']:.3f}s")
    print(f"  - Processing rate: {stats['events_per_second']:.1f} events/second\n")
    
    print("Data Statistics:")
    print(f"  - Total events processed: {stats['total_events']}")
    print(f"  - Actors analyzed: {stats['actors_analyzed']}")
    print(f"  - Analysis window: {stats['window']} turns\n")
    
    if stats['tags_distribution']:
        print("Tag Distribution:")
        for tag, count in sorted(stats['tags_distribution'].items(), key=lambda x: -x[1]):
            percentage = (count / stats['actors_analyzed']) * 100
            print(f"  - {tag}: {count} actors ({percentage:.1f}%)")
    else:
        print("Tag Distribution: No tags assigned")
    
    print(f"\n{'='*70}")
    print("STRESS TEST COMPLETED")
    print(f"{'='*70}\n")


def main():
    """
    Run stress test with multiple configurations and print results.
    """
    # Test configuration
    test_configs = [
        {"num_actors": 50, "num_turns": 100, "events_per_turn": 20, "window": 10},
        {"num_actors": 100, "num_turns": 200, "events_per_turn": 30, "window": 15},
    ]
    
    all_results = []
    
    for config in test_configs:
        stats = run_stress_test(**config)
        print_stress_test_results(stats)
        all_results.append(stats)
    
    # Print summary comparison
    if len(all_results) > 1:
        print(f"\n{'='*70}")
        print("COMPARATIVE SUMMARY")
        print(f"{'='*70}\n")
        for i, stats in enumerate(all_results, 1):
            print(f"Test {i}:")
            print(f"  - Scale: {stats['total_events']} events, {stats['actors_analyzed']} actors")
            print(f"  - Performance: {stats['extraction_time_s']:.3f}s ({stats['events_per_second']:.1f} events/s)")
        print()


if __name__ == "__main__":
    main()
