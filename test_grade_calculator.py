"""PyTest suite for grade_calculator.py

Sections
  1. Black-box: Equivalence Partitioning (EP)
  2. Black-box: Boundary Value Analysis (BVA)
  3. White-box: Statement and Branch coverage
  4. White-box: Path coverage (classify_result, calculate_average loop)
  5. Edge cases and error handling (build_report)
"""
import pytest
from grade_calculator import (validate_score, get_grade, calculate_average,
                              classify_result, build_report)


# ---------------------------------------------------------------- 1. EP
# One representative value per partition is enough.
@pytest.mark.parametrize("score, expected", [
    (85, "A"),      # partition 70-100
    (65, "B"),      # partition 60-69
    (55, "C"),      # partition 50-59
    (47, "D"),      # partition 45-49
    (42, "E"),      # partition 40-44
    (20, "F"),      # partition 0-39
])
def test_ep_valid_grade_partitions(score, expected):
    assert get_grade(score) == expected


@pytest.mark.parametrize("bad_score", [-5, 150])
def test_ep_invalid_numeric_partitions(bad_score):     # below 0 / above 100
    with pytest.raises(ValueError):
        get_grade(bad_score)


@pytest.mark.parametrize("bad_type", ["abc", None, [70], True])
def test_ep_invalid_type_partition(bad_type):
    with pytest.raises(TypeError):
        get_grade(bad_type)


# --------------------------------------------------------------- 2. BVA
# Test on, just below and just above every boundary.
@pytest.mark.parametrize("score, expected", [
    (0, "F"), (1, "F"),
    (39, "F"), (39.99, "F"), (40, "E"), (41, "E"),
    (44, "E"), (45, "D"), (46, "D"),
    (49, "D"), (50, "C"), (51, "C"),
    (59, "C"), (60, "B"), (61, "B"),
    (69, "B"), (69.99, "B"), (70, "A"), (71, "A"),
    (99, "A"), (100, "A"),
])
def test_bva_grade_boundaries(score, expected):
    assert get_grade(score) == expected


@pytest.mark.parametrize("score", [-1, -0.01, 100.01, 101])
def test_bva_just_outside_valid_range(score):
    with pytest.raises(ValueError):
        validate_score(score)


@pytest.mark.parametrize("attendance, expected", [
    (74, "PASS WITH WARNING"), (75, "PASS"), (76, "PASS"),
])
def test_bva_attendance_boundary(attendance, expected):
    assert classify_result([60, 60], attendance) == expected


@pytest.mark.parametrize("scores, expected", [
    ([39, 39], "FAIL"), ([40, 40], "PASS"), ([41, 41], "PASS"),
])
def test_bva_pass_mark_boundary(scores, expected):
    assert classify_result(scores, 100) == expected


# ------------------------------------------- 3. Statement / Branch coverage
def test_validate_score_returns_float_for_valid_int():
    assert validate_score(50) == 50.0
    assert isinstance(validate_score(50), float)


def test_calculate_average_normal_list():
    assert calculate_average([70, 80, 90]) == 80.0


def test_calculate_average_rounds_to_two_places():
    assert calculate_average([45, 50, 60]) == 51.67


def test_calculate_average_empty_list_raises():
    with pytest.raises(ValueError):
        calculate_average([])


def test_calculate_average_rejects_invalid_score_inside_list():
    with pytest.raises(ValueError):
        calculate_average([70, 120])


def test_classify_result_rejects_non_numeric_attendance():
    with pytest.raises(TypeError):
        classify_result([60], "high")


@pytest.mark.parametrize("attendance", [-1, 101])
def test_classify_result_rejects_out_of_range_attendance(attendance):
    with pytest.raises(ValueError):
        classify_result([60], attendance)


# ------------------------------------------------------- 4. Path coverage
# classify_result has three normal paths through its two decisions:
#   Path 1: average >= 40  AND attendance >= 75  -> PASS
#   Path 2: average >= 40  AND attendance < 75   -> PASS WITH WARNING
#   Path 3: average <  40                        -> FAIL
def test_path1_pass():
    assert classify_result([70, 80], 90) == "PASS"


def test_path2_pass_with_warning():
    assert classify_result([70, 80], 50) == "PASS WITH WARNING"


def test_path3_fail():
    assert classify_result([20, 30], 90) == "FAIL"


# calculate_average loop: zero, one and many iterations.
def test_loop_zero_iterations_is_rejected():
    with pytest.raises(ValueError):
        calculate_average([])


def test_loop_one_iteration():
    assert calculate_average([55]) == 55.0


def test_loop_many_iterations():
    assert calculate_average([10, 20, 30, 40]) == 25.0


# ------------------------------------------- 5. Edge cases / error handling
def test_build_report_normal_student():
    assert build_report("Ada", [75, 68, 82], 80) == \
        "Ada: average 75.00, grade A, result PASS"


def test_build_report_accepts_numbers_typed_as_text():
    assert build_report("Chi", [45, "50", 60], 70) == \
        "Chi: average 51.67, grade C, result PASS WITH WARNING"


def test_build_report_empty_scores_reports_error():
    assert "could not process" in build_report("Bayo", [], 90)


def test_build_report_non_numeric_text_reports_error():
    assert "could not process" in build_report("Dayo", [30, "abc"], 85)


def test_build_report_none_score_reports_error():
    assert "could not process" in build_report("Eze", [None], 85)


def test_build_report_failing_student():
    assert build_report("Fola", [20, 30], 95).endswith("result FAIL")
