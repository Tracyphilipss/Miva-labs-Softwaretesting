"""Student result calculator - BUGGY VERSION (for the debugging exercise)."""

PASS_MARK = 40


def validate_score(score):
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")
    return score


def get_grade(score):
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
    if not scores:
        raise ValueError("At least one score is required.")
    total = 0
    for i in range(len(scores)):
        total += scores[i]                # BUG 4 (runtime): "50" + int -> TypeError
    return total / len(scores)            # BUG 5 (runtime): empty list -> ZeroDivisionError


if __name__ == "__main__":
    students = {"Ada": [75, 68, 82], "Bayo": [], "Chi": [45, "50", 60]}
    for name, scores in students.items():
        try:
            avg = calculate_average(scores)
        except ValueError as error:
            print(name, "error:", error)
            continue
        print(name, "average:", avg, "grade:", get_grade(avg))
