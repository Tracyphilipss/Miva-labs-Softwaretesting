"""Student result calculator - BUGGY VERSION (for the debugging exercise)."""

PASS_MARK = 40


def validate_score(score):
    if score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100.")
    return score


def get_grade(score)                      # BUG 1 (syntax): missing colon 
    if score > 70:                        # BUG 2 (logic): should be >=
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
    total = 0
    for i in range(1, len(scores)):       # BUG 3 (logic): skips the first score
        total += scores[i]                # BUG 4 (runtime): "50" + int -> TypeError
    return total / len(scores)            # BUG 5 (runtime): empty list -> ZeroDivisionError


if __name__ == "__main__":
    students = {"Ada": [75, 68, 82], "Bayo": [], "Chi": [45, "50", 60]}
    for name, scores in students.items():
        avg = calculate_average(scores)
        print(name, "average:", avg, "grade:", get_grade(avg))
