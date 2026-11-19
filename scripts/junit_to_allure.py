#!/usr/bin/env python3
"""Convert Jest JUnit XML into test results understood by Allure."""

import argparse
import hashlib
import json
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path


def convert(paths, output):
    output.mkdir(parents=True, exist_ok=True)
    total = 0
    for path in paths:
        root = ET.parse(path).getroot()
        for case in root.iter("testcase"):
            name = case.get("name") or "unnamed test"
            suite = case.get("classname") or path.stem
            full_name = f"{suite}.{name}"
            result = {
                "uuid": str(uuid.uuid4()),
                "historyId": hashlib.sha256(full_name.encode()).hexdigest(),
                "name": name,
                "fullName": full_name,
                "status": "passed",
                "stage": "finished",
                "labels": [{"name": "suite", "value": suite}],
            }
            for tag, status in (("failure", "failed"), ("error", "broken"), ("skipped", "skipped")):
                issue = case.find(tag)
                if issue is not None:
                    result["status"] = status
                    result["statusDetails"] = {
                        "message": issue.get("message") or "",
                        "trace": issue.text or "",
                    }
                    break
            target = output / f"{result['uuid']}-result.json"
            target.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
            total += 1
    if total == 0:
        raise ValueError("JUnit reports contain no test cases")
    return total


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    print(f"Converted {convert(args.reports, args.output)} JUnit tests to Allure results")
