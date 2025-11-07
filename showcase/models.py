from django.db import models

# ---------------------------------------------------------
# ✅ ALLOWED NOTES — One octave only, C4 → C5
# ---------------------------------------------------------
ALLOWED_NOTES = {
    "C4","C#4","D4","D#4","E4",
    "F4","F#4","G4","G#4","A4","A#4","B4",
    "C5"   # Top of the octave
}

# ✅ Only white-key notes of C-major (diatonic)
C_MAJOR = {
    "C4","D4","E4","F4","G4","A4","B4","C5"
}

# ✅ MIDI Semitone Values (one-octave C4 → C5)
NOTE_TO_INT = {
    "C4": 60,  "C#4": 61,
    "D4": 62,  "D#4": 63,
    "E4": 64,
    "F4": 65,  "F#4": 66,
    "G4": 67,  "G#4": 68,
    "A4": 69,  "A#4": 70,
    "B4": 71,
    "C5": 72
}

# Stepwise (good)
STEPWISE = {1, 2}

# Skips (m3/M3)
SKIPS = {3, 4}

# Leap = anything >= P4 (5 semitones)
LEAP_THRESHOLD = 5


# ---------------------------------------------------------
# ✅ MELODY MODEL
# ---------------------------------------------------------
class Melody(models.Model):
    notes = models.TextField(help_text="Example: C4 D#4 F4 G4 C5")

    def __str__(self):
        return f"Melody: {self.notes[:20]}..."

    # ----------------------------------------------
    # Parse notes
    # ----------------------------------------------
    def parse_notes(self):
        raw = self.notes.replace(",", " ").upper().split()
        return [self.normalize(n) for n in raw if n]

    def normalize(self, note):
        cleaned = ''.join(c for c in note if c.isalnum() or c == '#')
        return cleaned.upper()

    # ----------------------------------------------
    # Interval in semitones
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

        # Must have at least 2 notes
        if len(notes) < 2:
            return {
                "score": 0,
                "feedback": ["Not enough notes to analyze."]
            }

        # Validate notes exist in allowed set
        for n in notes:
            if n not in ALLOWED_NOTES:
                feedback.append(f"Invalid note (C4–C5 only): {n}")
                score -= 2.0

        # Diatonic check (C major)
        for n in notes:
            if n not in C_MAJOR:
                feedback.append(f"Non-diatonic accidental: {n}")
                score -= 1.0

        # Interval rules
        for i in range(len(notes) - 1):
            cur = notes[i]
            nxt = notes[i + 1]
            iv = self.interval(cur, nxt)

            # Stepwise okay
            if iv in STEPWISE:
                continue

            # Skips (m3/M3) okay
            if iv in SKIPS:
                continue

            # Leap
            if iv >= LEAP_THRESHOLD:
                feedback.append(f"Large leap: {cur} → {nxt}")
                score -= 1.0

                # Direction change rule
                if i + 2 < len(notes):
                    after = notes[i + 2]

                    up = NOTE_TO_INT[nxt] > NOTE_TO_INT[cur]
                    after_up = NOTE_TO_INT[after] > NOTE_TO_INT[nxt]

                    if up == after_up:
                        feedback.append("Leap not followed by direction change")
                        score -= 1.0

                    # Stepwise after leap
                    if self.interval(nxt, after) not in STEPWISE:
                        feedback.append("Leap not followed by stepwise motion")
                        score -= 1.0

        return {
            "score": max(0, round(score, 2)),
            "feedback": feedback if feedback else ["Great melody! Smooth and diatonic."]
        }
