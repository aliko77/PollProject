class PollQuestionChoices:
    CHOICES = (
        ("TXT", "Text"),
        ("CHBX", "CheckBox"),
        ("DTE", "Date"),
        ("EMAIL", "Email"),
        ("NMBR", "Number"),
        ("RDO", "Radio"),
        ("RNG", "Range"),
        ("TME", "Time"),
    )

    @classmethod
    def get_choices(cls):
        return cls.CHOICES

    @classmethod
    def get_default(cls):
        return cls.CHOICES[0]