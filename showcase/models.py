from django.db import model

C_MAJOR = ["C", "D", "E", "F", "G", "A", "B"]

class Melody(models.Model):
    notes = models.TextField()

    def parse_notes(self):
        return self.notes.replace(",", " ").split()

    def note_name(self, note):
        return ''.join([c for c in note if c.isalpha()])

    def analyze(self):
        notes = self.parse_notes()
        errors = []

        # Rule 1: C major diatonic only
        for n in notes:
            pitch = self.note_name(n)
            if pitch not in C_MAJOR:
                errors.append(f"Non-diatonic note: {n}")

        # Rule 2: Leading tone resolution (B → C)
        for i in range(len(notes) - 1):
            cur = self.note_name(notes[i])
            nxt = self.note_name(notes[i + 1])
            if cur == "B" and nxt != "C":
                errors.append("Leading tone (B) should resolve to C")

        return errors if errors else ["✅ Voice-leading OK"]

    def __str__(self):
        return self.note
