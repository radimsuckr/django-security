.. _models:

Models
======

Auth Token
----------


.. class:: auth_token.models.Token

  Model for storing authorization tokens.

  .. attribute:: key

    ``CharField``, contains authorization token value.

  .. attribute:: user

    ``ForeignKey``, foreign key to the logged user.

  .. attribute:: created_at

    ``DateTimeField``, contains date and time of token creation.

  .. attribute:: last_access

    ``DateTimeField``, contains date and time of lost token access.

  .. attribute:: is_active

    ``BooleanField`` contains if token is active.

  .. attribute:: user_agent

    ``CharField``, stored HTTP header User-Agent, that was get during token creation.

  .. attribute:: expiration

    ``BooleanField``, contains information if user set preserved token.

  .. attribute:: ip

    IP address of the logged user.

  .. attribute:: auth_slug

    ``SlugField``, slug that you can use for your own purposes.

  .. attribute:: backend

    Field contains name of the django authorization backend


.. class:: auth_token.models.TokenRelatedObject

  Model storing related objects with authorization token

  .. attribute:: token

    Relation to the authorization token.

  .. attribute:: content_type

    Content type of the related object.

  .. attribute:: object_id

    Identifier of the related object.

  .. attribute:: content_object

    Related object (``GenericForeignKey``)


.. class:: auth_token.models.UserTokenTakeover

  Model contains information about token takeover.

  .. attribute:: token

    Relation to the authorization token.

  .. attribute:: user

    Takeoved user.

  .. attribute:: is_active

   ``BooleanField`` contains if token is active.


.. class:: auth_token.models.AnonymousToken

  ``AnonymousToken`` has save purpose as Django ``AnonymousUser``. If you are using auth_token middleware request contains token (``request.token``). If token is not found the ``AnonymousToken`` is set to the request.


.. class:: auth_token.models.VerificationToken

  Verification token can be used for password reset or other athorization methods via e-mail, SMS or other media.

  .. attribute:: created_at

    ``DateTimeField``, contains date and time of token creation.

  .. attribute:: content_type

    Content type of the verified object.

  .. attribute:: object_id

    Identifier of the verified object.

  .. attribute:: content_object

    Verified object (``GenericForeignKey``)

  .. attribute:: key

    Verification token value.

  .. attribute:: expiration_in_minutes

    Token expiration in minutes.

  .. attribute:: slug

    Slug that can be used for token purposes definition.

  .. attribute:: is_active

   ``BooleanField`` contains if token is active.
