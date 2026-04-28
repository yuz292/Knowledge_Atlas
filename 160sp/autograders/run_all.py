#!/usr/bin/env python3
"""
run_all.py — CLI entry point for the 160sp autograder suite.

Usage:
  python3 run_all.py --track t1 --task 1 --student doe_jane --dir /path/to/submission
  python3 run_all.py --track t2 --task 2 --student all --dir /path/to/submissions/
  python3 run_all.py --self-test
"""
import argparse, json, os, sys, importlib

GRADERS = {
    ("t1", 1): "t1_task1_grader",
    ("t1", 2): "t1_task2_grader",
    ("t1", 3): "t1_task3_grader",
    ("t2", 1): "t2_task1_grader",
    ("t2", 2): "t2_task2_grader",
    ("t2", 3): "t2_task3_grader",
    ("t3", 1): "t3_task1_grader",
    ("t3", 2): "t3_task2_grader",
    ("t3", 3): "t3_task3_grader",
    ("t4", 1): "t4_task1_grader",
    ("t4", 2): "t4_task2_grader",
    ("t4", 3): "t4_task3_grader",
}

def get_grader(track: str, task: int):
    key = (track, task)
    if key not in GRADERS:
        print(f"Unknown track/task: {track}/{task}")
        sys.exit(1)
    mod_name = GRADERS[key]
    base = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base)
    mod = importlib.import_module(mod_name)
    return mod

def run_self_test():
    """Run every grader on an empty directory to verify no crashes."""
    import tempfile
    tmp = tempfile.mkdtemp(prefix="autograder_selftest_")
    print(f"Self-test directory: {tmp}")
    passed = 0
    failed = 0
    for (track, task), mod_name in sorted(GRADERS.items()):
        try:
            mod = get_grader(track, task)
            report = mod.grade(tmp, "self_test")
            print(f"  ✅ {track}/task{task} ({mod_name}): {report.total_earned:.0f}/{report.max_points:.0f}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {track}/task{task} ({mod_name}): {e}")
            failed += 1
    print(f"\nSelf-test: {passed} passed, {failed} failed")
    return failed == 0

def main():
    parser = argparse.ArgumentParser(description="160sp Autograder Suite")
    parser.add_argument("--track", choices=["t1","t2","t3","t4"], help="Track to grade")
    parser.add_argument("--task", type=int, choices=[1,2,3], help="Task number")
    parser.add_argument("--student", default="unknown", help="Student ID or 'all'")
    parser.add_argument("--dir", default=".", help="Submission directory")
    parser.add_argument("--output", choices=["json","markdown","both"], default="both")
    parser.add_argument("--self-test", action="store_true", help="Run self-test")
    parser.add_argument("--save", help="Save report to this path")
    args = parser.parse_args()

    if args.self_test:
        success = run_self_test()
        sys.exit(0 if success else 1)

    if not args.track or not args.task:
        parser.print_help()
        sys.exit(1)

    mod = get_grader(args.track, args.task)
    report = mod.grade(args.dir, args.student)

    if args.output in ("json", "both"):
        print(report.to_json())
    if args.output in ("markdown", "both"):
        print("\n" + report.to_markdown())

    if args.save:
        os.makedirs(os.path.dirname(args.save) or ".", exist_ok=True)
        with open(args.save, "w") as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"\nReport saved to {args.save}")

if __name__ == "__main__":
    main()
