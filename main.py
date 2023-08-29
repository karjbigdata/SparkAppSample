from msal import ClientApplication


class AttachmentDownloader:

    def __init__(self, username: str, password: str):

        self.client_id = '<your client id>'
        self.authority = 'https://login.microsoftonline.com/<tenant-name>'

        # Initialise MS ClientApplication object with your client_id and authority URL
        self.app = ClientApplication(client_id=self.client_id,
                                     authority=self.authority)
        self.username = username # your mailbox username
        self.password = password # your mailbox password

        token = self.app.acquire_token_by_username_password(username=self.username,
                                                            password=self.password,
                                                            scopes=['.default'])
        print(token)

        # headers can be constructed with this token
        headers = {"Authorization": f"Bearer {token.get('access_token')}"}

if __name__ == "__main__":

    downloader = AttachmentDownloader("karthikeyy@outlook.com", "Apple@1234#")


