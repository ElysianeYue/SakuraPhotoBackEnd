# tokens.py
import hashlib

import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.encoding import smart_bytes
from django.utils.http import base36_to_int
from six import text_type

from SakuraPhotos import settings


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()

