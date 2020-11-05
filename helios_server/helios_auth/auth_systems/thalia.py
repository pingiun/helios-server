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
oauth.register(
    name="thalia", scope="members:read activemembers:read",
)

_THALIA_GROUPS = None
_THALIA_GROUPS_UPDATE = None


def get_groups(token):
    global _THALIA_GROUPS, _THALIA_GROUPS_UPDATE
    if (
        _THALIA_GROUPS is None
        or _THALIA_GROUPS_UPDATE + datetime.timedelta(hours=1) < datetime.datetime.now()
    ):
        resp = oauth.thalia.get("activemembers/groups/", token=token)
        if resp.status_code == 403:
            oauth.thalia.refresh_token()

        _THALIA_GROUPS = json.loads(resp.text)
        _THALIA_GROUPS_UPDATE = datetime.datetime.now()

    return _THALIA_GROUPS


def get_auth_url(request, redirect_url):
    redirect_uri = request.build_absolute_uri(redirect_url)

    return oauth.thalia.authorize_redirect(request, redirect_uri, approval_prompt="auto").url


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

    groups = get_groups(token)
    groups = [
        str(group["pk"])
        for group in groups
        if user["pk"] in [member["pk"] for member in group["members"]]
    ]

    return {
        "type": "thalia",
        "user_id": email,
        "name": name,
        "info": {"email": email, "groups": groups},
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
    if category_id.startswith("event:"):
        return {"event": category_id.removeprefix("event:")}
    if category_id.startswith("group:"):
        return {"group": category_id.removeprefix("group:")}
    raise ValueError(f"Invalid category_id for thalia: {category_id}")


def pretty_eligibility(constraint):
    return f'Users present for event with id {constraint["event"]}'


def eligibility_category_id(constraint):
    return constraint["event"]


def list_categories(user):
    resp = oauth.thalia.get("events/", token=user.token)
    events = [event for event in json.loads(resp.text) if event["registration_allowed"]]
    return [
        {"id": f'event:{event["pk"]}', "name": f'Present at "{event["title"]}"'}
        for event in events
    ] + [
        {"id": f'group:{group["pk"]}', "name": group["name"]}
        for group in get_groups(user.token)
    ]


def check_constraint(constraint, user):
    """
    for eligibility
    """
    if "event" in constraint:
        events_resp = oauth.thalia.get("events/", token=user.token)
        events = json.loads(events_resp.text)
        present = [str(event["pk"]) for event in events if event["present"] == True]
        return constraint["event"] in present
    if "group" in constraint:
        return constraint["group"] in user.info["groups"]


#
# Election Creation
#


def can_create_election(user_id, user_info):
    return True
