"""
Google Authentication

"""

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.core.mail import send_mail

# some parameters to indicate that status updating is not possible
STATUS_UPDATES = False

# display tweaks
LOGIN_MESSAGE = "Log in with my Google Account"

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth = OAuth()
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


def get_auth_url(request, redirect_url):
    redirect_uri = request.build_absolute_uri(redirect_url)

    return oauth.google.authorize_redirect(request, redirect_uri).url


def get_user_info_after_auth(request):
    if "code" not in request.GET:
        return None

    token = oauth.google.authorize_access_token(request)
    user = oauth.google.parse_id_token(request, token)

    # the email address is in the credentials, that's how we make sure it's verified
    if not user["email_verified"]:
        raise Exception("email address with Google not verified")

    email = user["email"]

    name = user["name"]

    # watch out, response also contains email addresses, but not sure whether thsoe are verified or not
    # so for email address we will only look at the id_token

    return {
        "type": "google",
        "user_id": email,
        "name": name,
        "info": {"email": email},
        "token": {},
    }


def do_logout(user):
    """
    logout of Google
    """
    return None


def update_status(token, message):
    """
    simple update
    """
    pass


def send_message(user_id, name, user_info, subject, body):
    """
    send email to google users. user_id is the email for google.
    """
    send_mail(
        subject,
        body,
        settings.SERVER_EMAIL,
        ["%s <%s>" % (name, user_id)],
        fail_silently=False,
    )


def check_constraint(constraint, user_info):
    """
    for eligibility
    """
    pass


#
# Election Creation
#


def can_create_election(user_id, user_info):
    return True
