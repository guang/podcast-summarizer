import json


def pretty_print_summary(summary):
    sorted_summary = sorted(summary, key=lambda x: x.__dict__["timestamp"])
    for i in sorted_summary:
        print(json.dumps(i.__dict__, indent=4))
