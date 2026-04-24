from os import environ

SOCIAL_AUTH_BACKEND_ATTRS = {
    "oidc": ("Login with Pocket ID", ""),
}

SOCIAL_AUTH_OIDC_ENDPOINT = environ.get('SOCIAL_AUTH_OIDC_ENDPOINT')
SOCIAL_AUTH_OIDC_KEY = environ.get('SOCIAL_AUTH_OIDC_KEY')
SOCIAL_AUTH_OIDC_SECRET = environ.get('SOCIAL_AUTH_OIDC_SECRET')
SOCIAL_AUTH_OIDC_SCOPE = ["openid", "profile", "email", "groups"]
SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "netbox.sso_pipeline_roles.add_groups",
    "netbox.sso_pipeline_roles.remove_groups",
    "netbox.sso_pipeline_roles.set_roles",
)
