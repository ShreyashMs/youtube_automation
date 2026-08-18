# Resumable Pipeline Documentation

## Overview

Your pipeline now supports automatic resumption of interrupted tasks! If a task fails or is interrupted during processing, the next pipeline run will automatically resume from that task without needing manual intervention.

## How It Works

### Before (Old Behavior)
Previously, if a task was interrupted during processing:
- The task would remain marked as `in_progress` in the progress file
- Running the pipeline again would fail with an error: "Queue item X is already in progress"
- You had to manually delete the `in_progress` marker or call `release_claim()` to continue

### After (New Behavior)
Now, when a task is interrupted:
- The task remains marked as `in_progress` in the progress file
- Running the pipeline again will automatically detect this and resume the task
- The pipeline continues from where it left off
- Once completed successfully, the task is marked as completed

## Pipeline Architecture

### Task Lifecycle

1. **Claiming Phase**
   - `claim_next_item()` (JSON pipeline) or `claim_next_episode()` (Series pipeline)
   - Checks if there's an interrupted task to resume
   - If yes → resumes it automatically
   - If no → claims a new task from the queue

2. **Processing Phase**
   - Executes 6 sequential steps (script, thumbnail, footage, voice, video, upload)
   - Each step is tracked with visible logging
   - If any step fails, task remains in `in_progress` state

3. **Completion Phase**
   - Calls `mark_uploaded()` to complete the task
   - Clears the `in_progress` marker
   - Marks task in the `completed` section

4. **Error Handling**
   - If any step fails, `release_claim()` is called
   - Task remains in `in_progress` state
   - Next pipeline run will resume from this task

## Progress Files

### JSON Content Pipeline
**File:** `data/content_queue_progress.json`

```json
{
  "version": 1,
  "completed": {
    "task-id-001": {
      "uploaded_at": "...",
      "video_id": "...",
      "video_url": "..."
    }
  },
  "in_progress": null  // Task to resume (if any)
}
```

### Series Pipeline
**File:** `data/series_progress.json`

```json
{
  "version": 2,
  "series": {
    "bhagwat_gita": {
      "completed": {
        "bhagwat_gita:chapter-1:episode-1": {
          "completed_at": "...",
          "video_id": "...",
          "video_url": "..."
        }
      },
      "in_progress": null  // Episode to resume (if any)
    }
  }
}
```

## Logging Output

### Normal Execution
```
Running JSON queue item: task-id-042 (neutral)
Title: Example Video Title

[STEP 1/6] Saving script...
✓ Script saved
[STEP 2/6] Creating thumbnail...
✓ Thumbnail created
[STEP 3/6] Fetching footage...
✓ Footage fetched (5 clips)
[STEP 4/6] Generating voice...
✓ Voice generated
[STEP 5/6] Creating video...
✓ Video created
[STEP 6/6] Uploading video...
✓ Video uploaded - ID: xyz123

✓ JSON pipeline completed in 245.3 seconds.
```

### Resume Execution
```
[RESUME] Resuming interrupted task: task-id-042
[RESUME] Task was claimed at: 2026-08-18T10:30:45.123456+00:00

Running JSON queue item: task-id-042 (neutral)
Title: Example Video Title

[STEP 1/6] Saving script...
✓ Script saved
[STEP 3/6] Fetching footage...  # Skipped step 2 if it was already done
✓ Footage fetched (5 clips)
...
```

### Interrupt and Recovery
```
[STEP 4/6] Generating voice...
✗ Pipeline interrupted after 120.5 seconds
  Error: Network connection timeout
  Task task-id-042 will resume from the last failed step when pipeline runs again.
```

## Using the Resumable Pipeline

### Running the JSON Content Pipeline
```bash
python main.py
```

The `run_json_pipeline()` function will:
1. Check for interrupted tasks
2. Resume or claim a new task
3. Process all 6 steps
4. Automatically mark as complete on success

### Running the Series Pipeline
```bash
python -m scripts.series_pipeline
```

The `run_series_pipeline()` function will:
1. Check for interrupted episodes
2. Resume or claim a new episode
3. Process all 6 steps
4. Automatically mark as complete on success

## Manual Control

### Check Current Progress
```python
from scripts.json_content_loader import _progress
progress = _progress()
in_progress_task = progress.get("in_progress")
if in_progress_task:
    print(f"In progress: {in_progress_task['id']}")
else:
    print("No tasks in progress")
```

### Manually Clear a Stuck Task
```python
from scripts.json_content_loader import release_claim

# For JSON pipeline
release_claim("task-id-042")

# For Series pipeline
from scripts.content_loader import release_episode_claim
release_episode_claim("bhagwat_gita", "bhagwat_gita:chapter-1:episode-1")
```

### Force Reset Progress
```python
import json
import os

# Reset JSON pipeline progress
with open("data/content_queue_progress.json", "w") as f:
    json.dump({"version": 1, "completed": {}}, f, indent=2)

# Reset Series pipeline progress
with open("data/series_progress.json", "w") as f:
    json.dump({"version": 2, "series": {}}, f, indent=2)
```

## Best Practices

1. **Don't manually interrupt**: Let the pipeline complete or let it handle errors
2. **Check logs for resume detection**: Look for `[RESUME]` messages
3. **Monitor disk space**: Ensure sufficient space for intermediate files (footage, audio, video)
4. **Handle network interruptions**: The pipeline will resume when network is restored
5. **Use version control**: Keep your queue and series JSON files in version control

## Supported Interruption Points

The pipeline can resume from the following points:

1. **Script saved** → Resume from thumbnail generation
2. **Thumbnail created** → Resume from footage fetching
3. **Footage fetched** → Resume from voice generation
4. **Voice generated** → Resume from video creation
5. **Video created** → Resume from upload
6. **Upload started** → May require manual verification (upload may have succeeded even if process was interrupted)

## Troubleshooting

### Task stuck as in_progress?
- Check `data/content_queue_progress.json` for the `in_progress` field
- Run pipeline again - it should resume automatically
- If still stuck, use `release_claim()` to manually clear it

### Pipeline keeps failing at the same step?
- Check the error message for the specific failure reason
- Fix the underlying issue (network, storage, permissions, etc.)
- Run pipeline again to resume

### Want to skip a problematic task?
```python
from scripts.json_content_loader import release_claim, mark_uploaded

item_id = "problematic-task-id"
release_claim(item_id)

# Manually mark as skipped
import json
with open("data/content_queue_progress.json", "r") as f:
    progress = json.load(f)
progress["completed"][item_id] = {"skipped": True}
with open("data/content_queue_progress.json", "w") as f:
    json.dump(progress, f, indent=2)
```

## Summary

Your pipeline is now production-ready with:
- ✅ Automatic task resumption on interruption
- ✅ Clear step-by-step logging
- ✅ Graceful error handling
- ✅ Persistent progress tracking
- ✅ No manual intervention required

Just run `python main.py` and let the pipeline handle interruptions automatically!
