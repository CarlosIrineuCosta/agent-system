# Garbage Collection

## Overview

The agent-coordinator generates output files and logs during operation. Over time, these accumulate and consume disk space. The garbage collector cleans up old files automatically.

## Script

File: `scripts/garbage_collector.py`

## Retention Policies

| File Type | Location | Retention | Cleanup Method |
|-----------|----------|-----------|----------------|
| Agent outputs | `.agents/output/` | 7 days | Delete entire directory |
| Coordinated results | `.agents/coordinated/` | 7 days | Delete entire directory |
| Execution logs | `.agents/logs/` | 30 days | Delete log files |
| Session archives | `.claude/agent-coordinator/runtime/logs/` | 30 days | Delete JSON files |

## Usage

### Check Disk Usage

```bash
python3 scripts/garbage_collector.py --stats
```

Output:
```
=== Agent System Disk Usage ===
Total: 45.23 MB

Breakdown:
  .agents/queue/: 0.00 MB
  .agents/output/: 12.45 MB
  .agents/coordinated/: 8.12 MB
  .agents/logs/: 24.66 MB
```

### Preview Cleanup (Dry Run)

```bash
python3 scripts/garbage_collector.py --dry-run
```

### Run Cleanup

```bash
python3 scripts/garbage_collector.py --clean
```

### Custom Retention Periods

```bash
python3 scripts/garbage_collector.py --clean --output-days 3 --log-days 14
```

## Automatic Cleanup

The garbage collector runs automatically during `/stop` command:

1. Stop command initiates shutdown
2. GC cleans old outputs (>7 days)
3. GC cleans old logs (>30 days)
4. GC removes empty directories
5. Summary is displayed to user

## Cleanup Operations

### 1. Old Outputs

```python
clean_old_outputs(days=7)
```

Removes entire directories under `.agents/output/` and `.agents/coordinated/` older than the retention period.

### 2. Old Logs

```python
clean_old_logs(days=30)
```
Removes `.log` files from `.agents/logs/` and `.json` files from runtime logs.

### 3. Empty Directories

```python
clean_empty_dirs()
```

Removes empty directories under `.agents/` to keep the structure clean.

## Disk Space Monitoring

The system tracks disk usage and can alert when thresholds are exceeded:

| Usage Level | Action |
|-------------|--------|
| < 100 MB | Normal operation |
| 100-500 MB | Warning on `/stop` |
| > 500 MB | Urgent warning, suggest cleanup |

## Manual Cleanup Commands

### Clean Everything

```bash
# Remove all agent outputs (use with caution)
rm -rf .agents/output/* .agents/coordinated/*
```

### Clean Specific Output

```bash
# Remove specific output directory
rm -rf .agents/output/test_run_001/
```

### Clean Old Logs Only

```bash
# Find and remove logs older than 30 days
find .agents/logs/ -name "*.log" -mtime +30 -delete
```

## Safety Features

1. **Dry-run mode:** Always preview before actual cleanup
2. **Age-based:** Only removes files older than retention period
3. **Empty check:** Won't remove non-empty directories unless explicitly old
4. **Logging:** All cleanup actions are logged

## Integration with State Manager

The state manager calls the garbage collector during shutdown:

```python
def stop(self, timeout: int = 30) -> bool:
    # ... stop agents ...

    # Run cleanup
    gc = GarbageCollector()
    gc.clean_all(dry_run=False)

    # ... save state ...
```

## Best Practices

1. **Run stats before cleanup** - Know what you're deleting
2. **Use dry-run first** - Preview the impact
3. **Archive important outputs** - Move to permanent storage before cleanup
4. **Monitor disk usage** - Run `--stats` regularly
5. **Adjust retention** - Change defaults based on your needs
