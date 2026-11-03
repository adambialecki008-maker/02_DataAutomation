from downtime_analyzer import analyze_downtime, validated_events


def test_validated_events_rejects_events_if_no_id():
    events = [
        {"id": "e1", "machine": "PRESS_1", "duration_s": 120},
        {"id": "", "machine": "PRESS_3", "duration_s": 300},
    ]
    passed, errors = validated_events(events)
    assert len(passed) == 1
    assert errors[0] == "Skipped event because no id"
    assert passed[0]["machine"] == "PRESS_1"


def test_validated_events_rejects_events_if_no_machine():
    events = [
        {"id": "e1", "machine": "", "duration_s": 120},
        {"id": "e2", "machine": "PRESS_3", "duration_s": 300},
    ]
    passed, errors = validated_events(events)
    assert len(passed) == 1
    assert errors[0] == "Skipped event because no machine for id: e1"
    assert passed[0]["id"] == "e2"


def test_validate_events_skips_if_field_missing():
    events = [
        {"machine": "PRESS_8", "duration_s": 120},
        {"id": "e2", "machine": "PRESS_3", "duration_s": 300},
        {"id": "e1", "machine": "PRESS_2", "duration_s": 100},
        {"id": "e3", "duration_s": 100},
    ]
    passed, errors = validated_events(events)
    assert len(passed) == 2


def test_validate_events_saves_event_if_second_with_same_id_is_proper():
    events = [
        {"id": "e1", "machine": "PRESS_3", "duration_s": -300},
        {"id": "e1", "machine": "PRESS_2", "duration_s": 100},
        {"id": "e2", "machine": "PRESS_3", "duration_s": 300},
    ]
    passed, errors = validated_events(events)
    assert len(passed) == 2
    assert passed[0]["id"] == "e1"
    assert passed[0]["machine"] == "PRESS_2"


def test_validate_events_dont_break_if_list_is_empty():
    events = []
    passed, errors = validated_events(events)
    assert len(passed) == 0


def test_validate_events_skips_if_wrong_data_type_machine():
    events = [
        {"id": "e3", "machine": 123, "duration_s": 120},
        {"id": "e2", "machine": "PRESS_3", "duration_s": 300},
        {"id": "e1", "machine": "PRESS_2", "duration_s": 100},
    ]
    passed, errors = validated_events(events)
    assert len(passed) == 2


def test_validate_events_skips_if_duration_is_bool():
    events = [
        {"id": "e3", "machine": "PRESS_1", "duration_s": 120},
        {"id": "e2", "machine": "PRESS_3", "duration_s": 300},
        {"id": "e1", "machine": "PRESS_2", "duration_s": True},
    ]
    passed, errors = validated_events(events)
    assert len(passed) == 2


def test_validate_events_skips_if_wrong_data_type_id():
    events = [
        {"id": 123, "machine": "PRESS_8", "duration_s": 120},
        {"id": "e2", "machine": "PRESS_3", "duration_s": 300},
        {"id": "e1", "machine": "PRESS_2", "duration_s": 100},
    ]
    passed, errors = validated_events(events)
    assert len(passed) == 2


def test_validated_events_rejects_events_if_double_id():
    events = [
        {"id": "e1", "machine": "PRESS_8", "duration_s": 120},
        {"id": "e2", "machine": "PRESS_3", "duration_s": 300},
        {"id": "e1", "machine": "PRESS_2", "duration_s": 100},
    ]
    passed, errors = validated_events(events)
    assert len(passed) == 2
    assert errors[0] == "Skipped event because double id"
    assert passed[0]["id"] == "e1"
    assert passed[1]["id"] == "e2"
    assert passed[1]["machine"] == "PRESS_3"


def test_validated_events_rejects_wrong_duration_format():
    events = [
        {"id": "e1", "machine": "PRESS_1", "duration_s": 120},
        {"id": "e4", "machine": "CNC_2", "duration_s": -20},
        {"id": "e6", "machine": "PRESS_1", "duration_s": "60"},
    ]

    passed, errors = validated_events(events)
    assert len(passed) == 1
    assert len(errors) == 2
    assert errors[0] == ("Wrong duration_s value for event id : e4")
    assert passed[0]["duration_s"] == 120


def test_analyze_downtime_returns_expected_dictionary():
    events = [
        {"id": "e1", "machine": "PRESS_1", "duration_s": 120},
        {"id": "e2", "machine": "PRESS_1", "duration_s": 300},
        {"id": "e3", "machine": "CNC_2", "duration_s": 90},
        {"id": "e2", "machine": "PRESS_1", "duration_s": 999},
        {"id": "e4", "machine": "CNC_2", "duration_s": -20},
        {"id": "e5", "machine": "", "duration_s": 50},
        {"id": "e6", "machine": "PRESS_1", "duration_s": "60"},
    ]
    expected_list = {
        "machines": {
            "PRESS_1": {"count": 2, "total_stop_s": 420},
            "CNC_2": {"count": 1, "total_stop_s": 90},
        },
        "rejected": 4,
    }
    results = analyze_downtime(events)
    assert results == expected_list


def test_analyze_downtime_returns_empty():
    events = []
    expected_list = {"machines": {}, "rejected": 0}
    results = analyze_downtime(events)
    assert results == expected_list
