class PollQuestionChoices:
    CHOICES = (
        ("TXT", "Text"),
        ("NMBR", "Number"),
        ("DTE", "Date"),
        ("EMAIL", "Email"),
        ("TME", "Time"),
        ("RNG", "Range"),
        ("CHBX", "CheckBox"),
        ("RDO", "Radio"),
    )

    @classmethod
    def get_choices(cls):
        return cls.CHOICES

    @classmethod
    def get_default(cls):
        return cls.CHOICES[0]