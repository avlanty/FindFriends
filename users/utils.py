from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):
    
    def _make_has_value(self, member, timestamp):
        return (six.text_type(member.pk)+six.text_type(timestamp)+six.text_type(member.is_email_verified))
    
    
generate_token = TokenGenerator()