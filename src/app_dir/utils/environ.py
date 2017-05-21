import os, re, boto3, base64

from environ import Env as EnvironEnv

base64_pattern = re.compile(r'(?:[A-Za-z0-9+/]{4}){2,}(?:[A-Za-z0-9+/]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9+/][AQgw]==)')

AWS_REGION = os.environ.get('AWS_REGION', None)

class Env(EnvironEnv):
    """ Extends environ.Env with added AWS KMS encryption support. """

    def decrypt_kms_data(self, encrypted_data):
        if AWS_REGION:
            kms = boto3.client('kms', region_name=AWS_REGION)

            decrypted = kms.decrypt(CiphertextBlob=encrypted_data)

            if decrypted.get('KeyId'):
                # Decryption succeed
                return decrypted.get('Plaintext')

    def __call__(self, var, cast=None, default=EnvironEnv.NOTSET, parse_default=False):
        value = self.get_value(var, cast=cast, default=default, parse_default=parse_default)

        if value:
            # Check if environment value base64 encoded
            if base64_pattern.match(value):
                # If yes, decode it using AWS KMS
                data = base64.b64decode(value)
                decrypted_value = self.decrypt_kms_data(data)

                # If decryption succeed, use it
                if decrypted_value:
                    value = decrypted_value

        return value