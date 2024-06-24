from gsuite.gauth.gauth import GAuth
from gsuite.models import GAuthConfig


def main():
    creds = None


def gsuite():
    authconfig = GAuthConfig(
        GOOGLE_CLIENT_ID="277806072672-4dnp0sbeh2eu3ght4gqhjji9tt2uip5l.apps.googleusercontent.com",
        GOOGLE_CLIENT_SECRET="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",
        GOOGLE_AUTH_SCOPE=[
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/drive.file",
        ],
    )

    gauth = GAuth.from_config(authconfig)
    print(gauth.get_auth_url())
    code = input("enter code here: ")
    creds = gauth.authenticate_with_code(code)
    print(creds)


if __name__ == "__main__":
    gsuite()
