#!/usr/bin/env python3
"""How hard is a lesson? Easy, Medium or Hard, from what you have to build.

The rating comes from three counts that every lesson.json records under "parts" and "oscillators":

  chips        how many chips (ICs) are on the board at once (40106, 4040, 4021, 4051).
               Each extra chip means a new pinout to learn and wires running between chips,
               which is where most building mistakes happen.
  jumpers      the jumper wires the lesson needs: the most short pre-cut wires on the board at once
               plus the most long wires (the "jumpers" line of the lesson's parts list).
               Every jumper is one more placement to get right and one more thing to check
               when the circuit doesn't work.
  oscillators  the most oscillators running at once. Each one is another loop of parts
               (a knob or sensor and a timing capacitor) to build and tune by ear.

Formula (all weights are below so the team can tune them):

  points = CHIP_POINTS × (chips − 1)
         + JUMPER_POINTS × jumpers
         + OSC_POINTS × (oscillators − 1)

  Easy    points <  MEDIUM_FROM
  Medium  MEDIUM_FROM ≤ points < HARD_FROM
  Hard    points ≥ HARD_FROM

The first chip and the first oscillator are free: every lesson has at least one of each, so
they don't make one lesson harder than another.

A lesson can override the result by adding to its lesson.json:
  "difficulty": {"level": "medium", "why": "short reason"}
The computed rating is still recorded next to the override so the two can be compared.

Run this file to see every lesson's rating and the arithmetic behind it:
    python3 tools/difficulty.py
"""
import json, pathlib

CHIP_POINTS = 4      # per chip beyond the first
JUMPER_POINTS = 0.5  # per jumper wire in the parts list
OSC_POINTS = 2       # per oscillator beyond the first
MEDIUM_FROM = 11     # Easy below this
HARD_FROM = 18       # Hard from this

# How the thresholds were set (Oct 2026, with the first five lessons):
# - "From Blink to Drum Machine" is the foundation everyone starts with, so it defines Easy:
#   2 chips, 13 jumpers, 1 oscillator = 10.5 points. MEDIUM_FROM sits just above it, so any lesson
#   that asks for more building than the foundation is at least Medium.
# - HARD_FROM marks lessons with a large jump in wiring on top of extra chips and oscillators:
#   "Stepping Through Sounds with the 4051" (23 jumpers, 3 oscillators) = 19.5 points.
# Lessons near a line (within about 1 point) could reasonably go either way; adjust the weights
# or thresholds here, or override one lesson in its lesson.json, as more lessons are added.

CHIPS = ("40106", "4040", "4021", "4051")


def counts(lesson):
    """The three counts for a lesson, from its "parts" and "oscillators" fields."""
    parts = lesson.get("parts", {})
    return {
        "chips": sum(int(parts.get(c, 0)) for c in CHIPS),
        "jumpers": int(parts.get("jumpers", 0)),
        "oscillators": int(lesson.get("oscillators", 1)),
    }


def rate(lesson):
    """Return {"level", "points", "counts", "computed", "why"} for a lesson dict (lesson.json)."""
    c = counts(lesson)
    points = (CHIP_POINTS * max(0, c["chips"] - 1)
              + JUMPER_POINTS * c["jumpers"]
              + OSC_POINTS * max(0, c["oscillators"] - 1))
    computed = "easy" if points < MEDIUM_FROM else ("medium" if points < HARD_FROM else "hard")
    why = (f"{c['chips']} chip{'s' if c['chips'] != 1 else ''}, {c['jumpers']} jumpers, "
           f"{c['oscillators']} oscillator{'s' if c['oscillators'] != 1 else ''} → {points:g} points")
    result = {"level": computed, "points": points, "counts": c, "computed": computed, "why": why}
    override = lesson.get("difficulty")
    if isinstance(override, dict) and override.get("level") in ("easy", "medium", "hard"):
        result["level"] = override["level"]
        result["why"] = f"set by hand: {override.get('why', '')} (formula: {computed}, {why})"
    return result


if __name__ == "__main__":
    root = pathlib.Path(__file__).resolve().parent.parent / "lessons"
    print(f"Easy < {MEDIUM_FROM} points ≤ Medium < {HARD_FROM} points ≤ Hard\n")
    for f in sorted(root.glob("*/lesson.json")):
        L = json.loads(f.read_text())
        r = rate(L)
        print(f"{f.parent.name:24s} {r['level']:7s} {r['why']}")
