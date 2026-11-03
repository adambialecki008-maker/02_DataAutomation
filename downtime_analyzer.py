def analyze_downtime(events: list):

    events_passed, errors = validated_events(events)
    machines = create_machines_list(events_passed)
    rejected = len(errors)
    summary = {"machines": machines, "rejected": rejected}
    return summary


def validated_events(events: list) -> tuple[list, list]:
    events_passed = []
    errors = []
    checked_id = set()
    for event in events:
        try:
            if validate_single_event(event, checked_id):
                events_passed.append(event)
        except (ValueError, TypeError, KeyError) as e:
            errors.append(str(e))
            continue
    return events_passed, errors


def validate_single_event(event, checked_id: set) -> bool:
    if not isinstance(event["id"], str):
        raise TypeError(f"Skipped event because id has wrong type")
    if not event["id"].strip():
        raise ValueError(f"Skipped event because no id")
    if not isinstance(event["machine"], str):
        raise TypeError(
            f"Skipped event because machine has wrong type for id: {event["id"]}"
        )
    if not event["machine"].strip():
        raise ValueError(f"Skipped event because no machine for id: {event["id"]}")
    if type(event["duration_s"]) is not int:
        raise TypeError(f"Wrong duration_s format for event id : {event["id"]}")
    if event["duration_s"] <= 0:
        raise ValueError(f"Wrong duration_s value for event id : {event["id"]}")
    if event["id"] not in checked_id:
        checked_id.add(event["id"])
    else:
        raise ValueError(f"Skipped event because double id")
    return True


def create_machines_list(events: list) -> dict:
    machines = {}
    for event in events:
        duration = event["duration_s"]
        name = event["machine"]
        if name not in machines:
            machines[name] = {"count": 1, "total_stop_s": duration}
        else:
            machines[name]["count"] += 1
            machines[name]["total_stop_s"] += duration

    return machines
