import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

_key_vault_name = os.environ["KEY_VAULT_NAME"]
_kv_uri = f"https://{_key_vault_name}.vault.azure.net"
_credential = DefaultAzureCredential()
_client = SecretClient(vault_url=_kv_uri, credential=_credential)

def get_secret(secret_name):
    return _client.get_secret(secret_name).value

def azure_auth(secret_name, secret_pass):
    retrieved_secret_name = get_secret(secret_name)
    retrieved_secret_pass = get_secret(secret_pass)
    return retrieved_secret_name, retrieved_secret_pass

