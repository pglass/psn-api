import os

SSO_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/ssocookie'
CODE_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/authorize'
OAUTH_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/token'
USERS_URL = 'https://us-prof.np.community.playstation.net/userProfile/v1/users'

LOGIN_CLIENT_ID = '71a7beb8-f21a-47d9-a604-2e71bee24fe0'
OAUTH_CLIENT_ID = 'b7cbf451-6bb6-4a5a-8913-71e61f462787'
OAUTH_CLIENT_SECRET = 'zsISsjmCx85zgCJg'

DUID = "0000000d000400808F4B3AA3301B4945B2E3636E38C0DDFC"

SCOPE = ",".join([
    "capone:report_submission",
    "psn:sceapp",
    "user:account.get",
    "user:account.settings.privacy.get",
    "user:account.settings.privacy.update",
    "user:account.realName.get",
    "user:account.realName.update",
    "kamaji:get_account_hash",
    "kamaji:ugc:distributor",
    "oauth:manage_device_usercodes",
])

DEFAULT_FRIEND_FIELDS = (
    "onlineId",
    "avatarUrls",
    "following",
    "friendRelation",
    "isOfficiallyVerified",
    "personalDetail(@default,profilePictureUrls)",
    "personalDetailSharing",
    "plus",
    "presences(@titleInfo,hasBroadcastData,lastOnlineDate)",
    "primaryOnlineStatus",
    "trophySummary(@default)",
)

