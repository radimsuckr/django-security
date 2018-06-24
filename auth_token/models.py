import os, binascii
import string

from datetime import timedelta

from django.conf import settings as django_settings
from django.db import models
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import force_text

from auth_token.config import settings


class Token(models.Model):
    """
    The default authorization token model.
    """

    key = models.CharField(max_length=40, primary_key=True, null=False, blank=False)
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL, related_name='auth_token', null=False, blank=False,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    last_access = models.DateTimeField(auto_now=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    # It is possiple use https://github.com/selwin/django-user_agents/tree/master/django_user_agents or
    # https://github.com/selwin/python-user-agents for parse
    # Limited size to 256
    user_agent = models.CharField(max_length=256, null=True, blank=True)
    expiration = models.BooleanField(default=True)
    ip = models.GenericIPAddressField(null=False, blank=False)
    auth_slug = models.SlugField(null=True, blank=True)
    backend = models.CharField(max_length=255, null=False, blank=False)
    allowed_cookie = models.BooleanField(default=True)
    allowed_header = models.BooleanField(default=True)

    is_from_header = False
    is_from_cookie = False

    @property
    def active_takeover(self):
        return self.user_takeovers.filter(is_active=True).last()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Token, self).save(*args, **kwargs)

    def generate_key(self):
        """
        Random ID generating
        """
        return force_text(binascii.hexlify(os.urandom(20)))

    def _get_token_age(self):
        return self.expiration and settings.DEFAULT_TOKEN_AGE or settings.MAX_TOKEN_AGE

    @property
    def is_expired(self):
        return self.last_access + timedelta(seconds=self._get_token_age()) < timezone.now()

    @property
    def time_to_expiration(self):
        return (self.last_access + timedelta(seconds=self._get_token_age())) - timezone.now()

    @property
    def str_time_to_expiration(self):
        return str(self.time_to_expiration) if self.time_to_expiration.total_seconds() > 0 else '00:00:00'

    def __str__(self):
        return self.key


class TokenRelatedObject(models.Model):
    """
    Generic relation to objects related with authorization token
    """

    token = models.ForeignKey(Token, related_name='related_objects', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.TextField()
    content_object = GenericForeignKey('content_type', 'object_id')


class UserTokenTakeover(models.Model):
    """
    The model allows to change user without token change
    """

    token = models.ForeignKey(Token, related_name='user_takeovers', on_delete=models.CASCADE)
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL, related_name='user_token_takeovers', null=False,
                             blank=False, on_delete=models.CASCADE)
    is_active = models.BooleanField()


class AnonymousToken:

    key = None
    user = AnonymousUser
    creted_at = None
    is_active = False
    user_agent = None
    is_expired = True
    is_from_header = False
    is_from_cookie = False
    active_takeover = None
    backend = None
    allowed_cookie = False
    allowed_header = False

    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError


class VerificationTokenManager(models.Manager):

    def deactivate(self, obj, slug=None, key=None):
        self.filter_active_tokens(obj, slug, key).update(is_active=False)

    def deactivate_and_create(self, obj, slug=None, deactivate_old_tokens=True, expiration_in_minutes=24 * 60):
        if deactivate_old_tokens:
            self.deactivate(obj, slug)
        return self.create(
            content_type=ContentType.objects.get_for_model(obj.__class__),
            object_id=obj.pk,
            slug=slug,
            expiration_in_minutes=expiration_in_minutes
        )

    def exists_valid(self, obj, verification_key, slug=None):
        for token in self.filter_active_tokens(obj, slug):
            if token.check_key(verification_key):
                return True
        return False

    def filter_active_tokens(self, obj, slug=None, key=None):
        qs = self.filter(
            is_active=True,
            slug=slug,
            content_type=ContentType.objects.get_for_model(obj.__class__),
            object_id=obj.pk
        )
        return qs.filter(key=key) if key else qs


class VerificationToken(models.Model):
    """
    Specific verification tokens that can be send via e-mail to check user authorization (example password reset)
    """

    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.TextField()
    content_object = GenericForeignKey('content_type', 'object_id')
    key = models.CharField(null=False, blank=False, max_length=100)
    expiration_in_minutes = models.PositiveIntegerField(null=True, blank=True, default=None)
    slug = models.SlugField(null=True, blank=True)
    is_active = models.BooleanField(null=False, blank=False, default=True)

    objects = VerificationTokenManager()

    def generate_key(self, length=20, allowed_chars=string.ascii_uppercase + string.digits):
        return get_random_string(length, allowed_chars)

    @property
    def is_valid(self):
        return (
            self.is_active and self.key and self.expiration_in_minutes and
            timezone.now() <= self.created_at + timedelta(minutes=self.expiration_in_minutes)
        )

    def check_key(self, verification_key):
        """
        Returns True iff verification key is correct and not expired
        """
        return self.is_valid and self.key == verification_key

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.key

    class Meta:
        ordering = ('-created_at',)
