from datetime import timedelta, datetime
import os
import subprocess
import json

def generate_allure_report(results_dir="allure-results", base_output="reports/allure-report/"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join(base_output, f"allure-report-{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        print("[INFO] Generating Allure HTML report...")
        subprocess.run([
            "allure", "generate", results_dir, "--clean", "-o", output_dir
        ], check=True, shell=True)

        print(f"[PASS] Allure report generated at: {output_dir}")
        return output_dir  # ✅ Return the actual path for further use

    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to generate Allure report: {e}")
        return None
    except Exception as ex:
        print(f"[ERROR] Exception during Allure report generation: {ex}")
        return None

def parse_allure_summary(base_dir="reports/allure-report/") -> dict:
    try:
        # Step 1: List all allure-report folders
        folders = [
            os.path.join(base_dir, f)
            for f in os.listdir(base_dir)
            if f.startswith("allure-report") and os.path.isdir(os.path.join(base_dir, f))
        ]

        if not folders:
            print(f"[WARN] No Allure report folders found in: {base_dir}")
            return {}

        # Step 2: Sort folders by last modified time
        folders.sort(key=lambda f: os.path.getmtime(f), reverse=True)
        latest_folder = folders[0]

        # Step 3: Read summary.json from latest folder
        summary_path = os.path.join(latest_folder, "widgets", "summary.json")
        if not os.path.exists(summary_path):
            print(f"[WARN] summary.json not found in: {latest_folder}")
            return {}

        with open(summary_path, "r") as f:
            data = json.load(f)

        stats = data.get("statistic", {})
        time_info = data.get("time", {})
        duration = str(timedelta(milliseconds=time_info.get("duration", 0)))

        summary = {
            "report_path": latest_folder,
            "total": stats.get("total", 0),
            "passed": stats.get("passed", 0),
            "failed": stats.get("failed", 0),
            "skipped": stats.get("skipped", 0),
            "broken": stats.get("broken", 0),
            "unknown": stats.get("unknown", 0),
            "duration": duration
        }

        print(f"[INFO] Parsed Allure summary from: {latest_folder}")
        return summary

    except Exception as e:
        print(f"[ERROR] Failed to parse Allure summary: {e}")
        return {}
    