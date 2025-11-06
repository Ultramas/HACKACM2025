from django.db import models

# ---------------------------------------------------------
# CONSTANTS — One octave C major (C4 → C5)
# ---------------------------------------------------------

# Allowed notes user can enter
ALLOWED_NOTES = {"C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"}

# C-major scale list
C_MAJOR = ["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]

# Semitone values (MIDI numbers)
NOTE_TO_INT = {
    "C4": 60,
    "D4": 62,
    "E4": 64,
    "F4": 65,
    "G4": 67,
    "A4": 69,
    "B4": 71,
    "C5": 72,
}

# Stepwise intervals (1 or 2 semitones)
STEPWISE = {1, 2}

# Skips (minor/major 3rd)
SKIPS = {3, 4}

# Leap = anything ≥ 5 semitones
LEAP_THRESHOLD = 5


# ---------------------------------------------------------
# MELODY MODEL
# ---------------------------------------------------------
class Melody(models.Model):
    notes = models.TextField(help_text="Example: C4 D4 E4 F4 G4")

    def __str__(self):
        return f"Melody: {self.notes[:20]}..."

    # ----------------------------------------------
    # Utility: Extract note names with octave
    # ----------------------------------------------
    def parse_notes(self):
        """
        Convert user string into note names, keeping octaves.
        Example: "C4 D4 E4" → ["C4", "D4", "E4"]
        """
        raw = self.notes.replace(",", " ").split()
        return [self.normalize(n) for n in raw if n]

    def normalize(self, note):
        """
        Keep letters + number (ex: 'C4', 'G5').
        Filters out weird characters.
        """
        cleaned = ''.join(c for c in note if c.isalnum())
        return cleaned

    # ----------------------------------------------
    # Compute interval in semitones (absolute)
    # ----------------------------------------------
    def interval(self, n1, n2):
        return abs(NOTE_TO_INT[n2] - NOTE_TO_INT[n1])

    # ----------------------------------------------
    # MAIN ANALYSIS
    # ----------------------------------------------
    def analyze(self):
        notes = self.parse_notes()
        feedback = []
        score = 10.0

        # ------------------------------------------
        # Validate minimum length
        # ------------------------------------------
        if len(notes) < 2:
            return {
                "score": 0,
                "feedback": ["Not enough notes to analyze."]
            }

        # ------------------------------------------
        # Validate ALL notes are allowed
        # ------------------------------------------
        for n in notes:
            if n not in ALLOWED_NOTES:
                feedback.append(f"Invalid note (allowed C4–C5 only): {n}")
                score -= 2.0

        # ------------------------------------------
        # Rule 1: Must be C-major diatonic
        # ------------------------------------------
        for n in notes:
            if n not in C_MAJOR:
                feedback.append(f"Non-diatonic note: {n}")
                score -= 1.0

        # ------------------------------------------
        # Rules 2–4: Intervals + Leaps
        # ------------------------------------------
        for i in range(len(notes) - 1):
            cur = notes[i]
            nxt = notes[i + 1]
            iv = self.interval(cur, nxt)

            # Stepwise (good)
            if iv in STEPWISE:
                continue

            # Skip of 3rd (acceptable)
            if iv in SKIPS:
                continue

            # Leap (4th or larger)
            if iv >= LEAP_THRESHOLD:
                feedback.append(f"Large leap: {cur} → {nxt}")
                score -= 1.0

                # Check direction change
                if i + 2 < len(notes):
                    after = notes[i + 2]

                    going_up = NOTE_TO_INT[nxt] > NOTE_TO_INT[cur]
                    after_up = NOTE_TO_INT[after] > NOTE_TO_INT[nxt]

                    if going_up == after_up:
                        feedback.append("Leap not followed by direction change")
                        score -= 1.0

                    # Check stepwise after leap
                    follow_iv = self.interval(nxt, after)
                    if follow_iv not in STEPWISE:
                        feedback.append("Leap not followed by stepwise motion")
                        score -= 1.0

        # ------------------------------------------
        # FINAL SCORE SAFETY
        # ------------------------------------------
        if score < 0:
            score = 0

        return {
            "score": round(score, 2),
            "feedback": feedback if feedback else ["Great job! Melody is smooth and diatonic."]
        }
