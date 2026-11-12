"""Student result calculator (FIXED VERSION).

Functions
---------
validate_score    - check that a score is a number from 0 to 100
get_grade         - convert a score into a letter grade
calculate_average - average of a list of scores
classify_result   - PASS / PASS WITH WARNING / FAIL using average and attendance
build_report      - one-line report for a student, with error handling
"""

PASS_MARK = 40
ATTENDANCE_MARK = 75


def validate_score(score):
    """Return the score as a float, or raise TypeError / ValueError."""
    if isinstance(score, bool) or not isinstance(score, (int, float)):
        raise TypeError("Score must be a number.")
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")
    return float(score)


def get_grade(score):
    """Convert a score (0-100) to a letter grade A-F."""
    score = validate_score(score)
    if score >= 70:
        return "A"
    elif score >= 60:
        return "B"
    elif score >= 50:
        return "C"
    elif score >= 45:
        return "D"
    elif score >= 40:
        return "E"
    else:
        return "F"


def calculate_average(scores):
    """Return the average of a non-empty list of valid scores (2 d.p.)."""
    if not scores:
        raise ValueError("At least one score is required.")
    total = 0.0
    for score in scores:
        total += validate_score(score)
    return round(total / len(scores), 2)


def classify_result(scores, attendance):
    """Return 'PASS', 'PASS WITH WARNING' or 'FAIL'.

    A student passes if the average is at least PASS_MARK.  If attendance is
    below ATTENDANCE_MARK the pass carries a warning.
    """
    if isinstance(attendance, bool) or not isinstance(attendance, (int, float)):
        raise TypeError("Attendance must be a number.")
    if attendance < 0 or attendance > 100:
        raise ValueError("Attendance must be between 0 and 100.")
    average = calculate_average(scores)
    if average >= PASS_MARK:
        if attendance >= ATTENDANCE_MARK:
            return "PASS"
        return "PASS WITH WARNING"
    return "FAIL"


def build_report(name, raw_scores, attendance):
    """Build a one-line report; bad input is reported instead of crashing."""
    try:
        scores = [float(s) for s in raw_scores]       # "50" -> 50.0
        average = calculate_average(scores)
        grade = get_grade(average)
        result = classify_result(scores, attendance)
    except (ValueError, TypeError) as error:
        return f"{name}: could not process - {error}"
    return f"{name}: average {average:.2f}, grade {grade}, result {result}"


if __name__ == "__main__":  # pragma: no cover
    students = {
        "Ada": ([75, 68, 82], 80),
        "Bayo": ([], 90),
        "Chi": ([45, "50", 60], 70),
        "Dayo": ([30, 35, "abc"], 85),
    }
    for student, (marks, attend) in students.items():
        print(build_report(student, marks, attend))
