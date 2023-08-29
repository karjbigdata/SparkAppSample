import msal
import json
import requests


# function to generate access token
def get_access_token():
    tenentID = "Azure_tenent_id"
    authority = 'https://login.microsoftonline.com/' + tenentID
    clientID = "Azure App/Client ID"
    clientSecret = "Azure App secret"
    scope = ['https://graph.microsoft.com/.default']
    app = msal.ConfidentialClientApplication(clientID, authority= authority, client_credential=clientSecret)
    access_token = app.acquire_token_for_client(scopes=scope)
    return access_token


def get_email_attachements(message_id):
    url = f"https://graph.microsoft.com/v1.0/users/{mail_user}/messages/{message_id}/attachments?"
    response = requests.get(url, headers=headers)
    return response.json()


access_token = get_access_token()
token = access_token['access_token']

date_received = '2023-02-04'  # date greater to search for latest mails
mail_subject = "INPUT DAILY INGESTION FILE MDP" # subject search string
mail_sender = 'other-project@outlook.com'  # mail sender id
mail_user = 'mdp-mdp@mdp.onmicrosoft.com'  # mail receiver id

# api call url
url = f"https://graph.microsoft.com/v1.0/users/{mail_user}/messages?$" \
      f"filter=startswith(from/emailAddress/address,'{mail_sender}') and " \
      f"subject eq '{mail_subject}' and receivedDateTime ge {date_received}"

headers = {
    "Authorization": f"Bearer {token}",
    "ContentType": "application/json"
}

# Send the api request
response = requests.get(url, headers=headers)
data = json.loads(response.text)

# loop through each response
for dataId in data["value"]:
    print(dataId['id'])
    msg_id = dataId['id']

    # get attachments now
    attachments = get_email_attachements(message_id=msg_id)
    for attachment in attachments['value']:
        attachment_name = attachment['name']
        attachment_id = attachment['id']
        #print(attachment_name)

        # download url request api call
        download_attachment_endpoint = f"https://graph.microsoft.com/v1.0/users/{mail_user}/messages/{msg_id}/attachments/{attachment_id}"

        headers_download = {
            "Authorization": f"Bearer {token}",
            "ContentType": "application/octet-stream"
        }

        response = requests.get(download_attachment_endpoint, headers=headers_download)
        response.raise_for_status()

        # store the attachments in current working directory
        with open(attachment_name, 'wb') as f:
            f.write(response.content)











