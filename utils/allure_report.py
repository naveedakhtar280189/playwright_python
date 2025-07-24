from datetime import timedelta, datetime

import os
import subprocess
import json

def generate_allure_report(results_dir="allure-results", base_output="reports/allure-report"):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_dir = os.path.join(base_output, f"allure-report-{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        print("[INFO] Generating Allure HTML report...")
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run(["allure", "generate", results_dir, "--clean", "-o", output_dir],
            check=True, shell=True
        )
        print(f"[PASS] Allure report generated at: {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to generate Allure report: {e}")
    except Exception as ex:
        print(f"[ERROR] Exception during Allure report generation: {ex}")

def parse_allure_summary(allure_report_dir="reports/allure-report") -> dict:
    try:
        summary_file = os.path.join(allure_report_dir, "widgets", "summary.json")
        if not os.path.exists(summary_file):
            print(f"[WARN] Summary file not found: {summary_file}")
            return {}

        with open(summary_file, "r") as f:
            data = json.load(f)

        stats = data.get("statistic", {})
        time_info = data.get("time", {})

        duration_ms = time_info.get("duration", 0)
        duration = str(timedelta(milliseconds=duration_ms))

        summary = {
            "total": stats.get("total", 0),
            "passed": stats.get("passed", 0),
            "failed": stats.get("failed", 0),
            "skipped": stats.get("skipped", 0),
            "broken": stats.get("broken", 0),
            "unknown": stats.get("unknown", 0),
            "duration": duration
        }

        print(f"[INFO] Parsed summary from Allure: {summary}")
        return summary

    except Exception as e:
        print(f"[ERROR] Failed to parse Allure summary: {e}")
        return {}
    