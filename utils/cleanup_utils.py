import os
import shutil
import datetime

def delete_old_timestamp_folders(base_dir: str, days_old: int = 7, timestamp_format="%Y-%m-%d_%H-%M-%S", marker_file=".last_cleanup"):
    """
    Deletes subfolders older than `days_old` days in the given base directory.
    Uses folder name's timestamp to determine age.
    Only runs once every 7 days using a marker file.

    Args:
        base_dir (str): Parent folder containing dated folders.
        days_old (int): Threshold in days for deletion.
        timestamp_format (str): Format used in folder names.
        marker_file (str): Name of the marker file to control cleanup frequency.
    """
    now = datetime.datetime.now()
    marker_path = os.path.join(base_dir, marker_file)

    # Check if we should skip (weekly cleanup control)
    if os.path.exists(marker_path):
        try:
            with open(marker_path, "r") as f:
                last_run = datetime.datetime.strptime(f.read().strip(), "%Y-%m-%d")
            if (now - last_run).days < 7:
                return  # Skip cleanup
        except Exception:
            pass

    # Cleanup logic
    if not os.path.exists(base_dir):
        return

    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path) and folder != marker_file:
            try:
                folder_time = datetime.datetime.strptime(folder, timestamp_format)
                if (now - folder_time).days > days_old:
                    shutil.rmtree(folder_path)
                    print(f"[Cleanup] Deleted old folder: {folder_path}")
            except ValueError:
                continue  # Skip non-timestamp folders

    # Update marker
    os.makedirs(base_dir, exist_ok=True)
    with open(marker_path, "w") as f:
        f.write(now.strftime("%Y-%m-%d"))
