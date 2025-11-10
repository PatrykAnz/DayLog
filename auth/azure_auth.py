import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

def azure_auth(secretName,secretPass):
    keyVaultName = os.environ["KEY_VAULT_NAME"]
    KVUri = f"https://{keyVaultName}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)
    retrieved_secret_name = client.get_secret(secretName).value
    retrieved_secret_pass = client.get_secret(secretPass).value
    return(retrieved_secret_name,retrieved_secret_pass)

