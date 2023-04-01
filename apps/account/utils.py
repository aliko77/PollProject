from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (
                str(user.pk) + user.password + str(timestamp)
        )


account_activate_token = TokenGenerator()
