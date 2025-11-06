from django.db import models

# ---------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------
C_MAJOR = ["C", "D", "E", "F", "G", "A", "B"]

# Map letter names to pitch values (mod 12)
NOTE_TO_INT = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

# Melodic consonance/dissonance
CONSONANT_INTERVALS = {0, 2, 4, 5, 7, 9}
DISSONANT_INTERVALS = {1, 6, 10, 11}  # m2, TT, m7, M7


# ---------------------------------------------------------
# MELODY MODEL
# ---------------------------------------------------------
class Melody(models.Model):
    notes = models.TextField(help_text="Example: C4 D4 E4 F4 G4")

    def __str__(self):
        return f"Melody: {self.notes[:20]}..."

    # ----------------------------------------------
    # UTILITY FUNCTIONS
    # ----------------------------------------------
    def parse_notes(self):
        """Convert user string into list of letter names."""
        raw = self.notes.replace(",", " ").split()
        return [self.note_name(n) for n in raw if n]

    def note_name(self, note):
        """Extract only the letter name (removes octaves)."""
        return ''.join(c for c in note if c.isalpha())

    def interval(self, n1, n2):
        """Interval in semitones (mod 12)."""
        return abs(NOTE_TO_INT[n1] - NOTE_TO_INT[n2]) % 12

    # ----------------------------------------------
    # MAIN ANALYSIS ALGORITHM
    # ----------------------------------------------
    def analyze(self):
        notes = self.parse_notes()
        feedback = []
        score = 10.0  # Start at 10/10

        if len(notes) < 2:
            return {
                "score": 0,
                "feedback": ["Not enough notes to analyze."]
            }

        # --------------------------
        # RULE 1: C-major diatonic
        # --------------------------
        for n in notes:
            if n not in C_MAJOR:
                feedback.append(f"Non-diatonic note: {n}")
                score -= 1.5

        # --------------------------
        # RULE 2, 3, 4: Intervals
        # --------------------------
        for i in range(len(notes) - 1):
            cur = notes[i]
            nxt = notes[i + 1]
            iv = self.interval(cur, nxt)

            # Stepwise motion (good)
            if iv in {1, 2}:
                continue

            # Skips (minor/major 3rd)
            if iv in {3, 4}:
                continue

            # Leap 4th or more
            if iv >= 5:
                feedback.append(f"Large leap: {cur} → {nxt}")
                score -= 1.0

                # RULE: Direction change after leap
                if i + 2 < len(notes):
                    after = notes[i + 2]

                    going_up = NOTE_TO_INT[nxt] > NOTE_TO_INT[cur]
                    after_up = NOTE_TO_INT[after] > NOTE_TO_INT[nxt]

                    if going_up == after_up:
                        feedback.append("Leap not followed by direction change")
                        score -= 1.0

                    # Must be stepwise after leap
                    if self.interval(nxt, after) not in {1, 2}:
                        feedback.append("Leap not followed by stepwise motion")
                        score -= 1.0

