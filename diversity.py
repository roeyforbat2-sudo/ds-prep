"""מדדי מגוון אלפא לדגימה אחת של ספירות מינים."""
import math


def _validate(counts):
    """בודקת שהקלט הוא רשימת ספירות חוקית; זורקת שגיאה אם לא."""
    if len(counts) == 0:
        raise ValueError("counts must not be empty")
    for c in counts:
        if not isinstance(c, (int, float)):
            raise TypeError("counts must be a number")
        if c < 0:
            raise ValueError("counts must be non-negative")
    if sum(counts) == 0:
        raise ValueError("all counts are 0")

def richness(counts, min_count=1):
    """מחזירה את מספר המינים שספירתם לפחות min_count."""
    _validate(counts)
    return len([c for c in counts if c >= min_count])

def relative_abundance(counts):
    """מחזירה רשימה חדשה של פרופורציות שמסתכמות ל-1."""
    _validate(counts)
    total = sum(counts)
    return [c / total for c in counts]

def shannon(counts, base=math.e):
    """מחזירה את מדד Shannon (H) של הדגימה."""
    proportions = relative_abundance(counts)
    return -sum(p * math.log(p, base) for p in proportions if p > 0)

def simpson(counts, *, kind="gini"):
    """מחזירה את מדד Simpson בגרסה שנבחרה ב-kind."""
    proportions = relative_abundance(counts)
    d = sum(p ** 2 for p in proportions)

    if kind == "dominance":
        return d
    elif kind == "gini":
        return 1 - d
    elif kind == "inverse":
        return 1 / d
    else:
        raise ValueError(f"unknown kind: {kind!r}")