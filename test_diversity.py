"""בדיקות ל-diversity.py — יום ג', שבוע 1.

הרצה (מתוך התיקייה שבה נמצא diversity.py, בסביבת ds):
    python test_diversity.py

כל בדיקה שעוברת מדפיסה ✓. בדיקה שנכשלת עוצרת עם AssertionError ומראה איפה.
אל תשנה את הקובץ הזה כדי שיעבור — תשנה את diversity.py.
"""
import math

from diversity import richness, relative_abundance, shannon, simpson

EVEN = [10, 10, 10, 10]   # קהילה אחידה לגמרי: 4 מינים בשכיחות שווה
SKEWED = [5, 0, 15]       # מין אחד נעדר, אחד דומיננטי


def close(a, b):
    return math.isclose(a, b, rel_tol=1e-6)


def expect_raises(exc_type, func, *args, **kwargs):
    """מוודא ש-func(*args, **kwargs) זורקת בדיוק exc_type."""
    try:
        func(*args, **kwargs)
    except exc_type:
        return
    except Exception as e:  # נזרקה שגיאה, אבל מהסוג הלא נכון
        raise AssertionError(
            f"{func.__name__}{args} זרקה {type(e).__name__}, ציפינו ל-{exc_type.__name__}"
        )
    raise AssertionError(f"{func.__name__}{args} לא זרקה שגיאה, ציפינו ל-{exc_type.__name__}")


def check(name, condition):
    assert condition, name
    print(f"✓ {name}")


# --- richness ---
check("richness: אחידה", richness(EVEN) == 4)
check("richness: מין נעדר לא נספר", richness(SKEWED) == 2)
check("richness: min_count כארגומנט מילת-מפתח", richness(SKEWED, min_count=10) == 1)

# --- relative_abundance ---
ra = relative_abundance(SKEWED)
check("relative_abundance: ערכים נכונים", all(close(x, y) for x, y in zip(ra, [0.25, 0.0, 0.75])))
check("relative_abundance: מסתכם ל-1", close(sum(ra), 1.0))
check("relative_abundance: לא משנה את הקלט", SKEWED == [5, 0, 15])

# --- shannon ---
check("shannon: אחידה = ln(4)", close(shannon(EVEN), math.log(4)))
check("shannon: מוטה", close(shannon(SKEWED), 0.5623351))
check("shannon: base=2 על אחידה = 2 ביטים", close(shannon(EVEN, base=2), 2.0))

# --- simpson ---
check("simpson: ברירת מחדל היא gini (1-D)", close(simpson(SKEWED), 0.375))
check("simpson: kind='dominance' (D)", close(simpson(SKEWED, kind="dominance"), 0.625))
check("simpson: kind='inverse' (1/D)", close(simpson(EVEN, kind="inverse"), 4.0))

# kind חייב להיות keyword-only: קריאה פוזיציונית צריכה להיכשל
expect_raises(TypeError, simpson, SKEWED, "inverse")
print("✓ simpson: kind הוא keyword-only")

# --- שגיאות: כל הפונקציות חולקות את אותה ולידציה ---
for f in (richness, relative_abundance, shannon, simpson):
    expect_raises(ValueError, f, [])            # רשימה ריקה
    expect_raises(ValueError, f, [3, -1, 2])    # ספירה שלילית
    expect_raises(ValueError, f, [0, 0, 0])     # אין אף פרט בדגימה
    expect_raises(TypeError, f, [1, "a", 2])    # ערך לא מספרי
    print(f"✓ {f.__name__}: ולידציה")

expect_raises(ValueError, simpson, EVEN, kind="foo")
print("✓ simpson: kind לא מוכר זורק ValueError")

print("\nכל הבדיקות עברו 🎉")
