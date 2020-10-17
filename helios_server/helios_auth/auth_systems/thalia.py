"""
Thalia Authentication

"""
import datetime
import json

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.core.mail import send_mail

# some parameters to indicate that status updating is not possible
STATUS_UPDATES = False

# display tweaks
LOGIN_MESSAGE = "Log in with my Thalia Account"

oauth = OAuth()
# oauth.register(
#     name="thalia",
#     client_id="cRJt1rw0hIoVbRLzpWI12wZKJWsyM1FeU5vk7XMS",
#     client_secret="hdkuWIGXAOwRcK78yIf9DtcA6FpFeXxMDsxRfAmoubJrTHWB7aGUeehk1MqMGGI2CyrLBhWabFhUatBOFtA7bGB8deqGTWcg7Ulrv2hqGBQ9GofxnN6MRTtJXUh4is1G",
#     authorize_url="https://staging.thalia.nu/user/oauth/authorize/",
#     access_token_url="https://staging.thalia.nu/user/oauth/token/",
#     api_base_url="https://staging.thalia.nu/api/v1/",
#     scope="members:read",
# )

oauth.register(
    name="thalia",
    client_id="rLIrRdepTqJrHdul1YwbT2klK1ePBwlUaUORVf3V",
    client_secret="vFaiWcHkmSG5hkqZkB3v3KtrVCx7xhVa8a9CvfihI2GT7phZefzLvmFzA5WAlSjDGejwJhVcMipAp9ctRGnq3GQSulBsYhkaBTrUHPWWmX7zsIykrMpklqq7ECpSPVcQ",
    authorize_url="http://127.0.0.1:8001/user/oauth/authorize/",
    access_token_url="http://127.0.0.1:8001/user/oauth/token/",
    api_base_url="http://127.0.0.1:8001/api/v1/",
    scope="members:read",
)


def get_auth_url(request, redirect_url):
    redirect_uri = request.build_absolute_uri(redirect_url)

    return oauth.thalia.authorize_redirect(request, redirect_uri).url


def get_user_info_after_auth(request):
    if "code" not in request.GET:
        return None

    token = oauth.thalia.authorize_access_token(
        request, grant_type="authorization_code"
    )
    resp = oauth.thalia.get("members/me/", token=token)

    user = json.loads(resp.text)

    if not user["membership_type"] == "member":
        raise Exception("only current members can vote")

    email = user["email"]

    name = user["display_name"]

    return {
        "type": "thalia",
        "user_id": email,
        "name": name,
        "info": {"email": email},
        "token": token,
    }


def do_logout(user):
    """
    logout of Thalia
    """
    return None


def update_status(token, message):
    """
    simple update
    """
    pass


def send_message(user_id, name, user_info, subject, body):
    """
    send email to Thalia users. user_id is the email for thalia.
    """
    send_mail(
        subject,
        body,
        settings.SERVER_EMAIL,
        ["%s <%s>" % (name, user_id)],
        fail_silently=False,
    )


def generate_constraint(category_id, user):
    return {"event": category_id}


def pretty_eligibility(constraint):
    return f'Users present for event with id {constraint["event"]}'


def eligibility_category_id(constraint):
    return constraint["event"]


def list_categories(user):
    resp = oauth.thalia.get("events/", token=user.token)
    events = [event for event in json.loads(resp.text) if event["registration_allowed"]]
    return [
        {"id": str(event["pk"]), "name": f'Present at "{event["title"]}"'}
        for event in events
    ]

def check_constraint(constraint, user):
    """
    for eligibility
    """
    events_resp = oauth.thalia.get("events/", token=user.token)
    events = json.loads(events_resp.text)
    present = [str(event["pk"]) for event in events if event["present"] == True]
    return constraint["event"] in present


#
# Election Creation
#


def can_create_election(user_id, user_info):
    return True