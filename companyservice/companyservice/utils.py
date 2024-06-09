from django.contrib.auth import authenticate

import json
import jwt
import requests

def jwt_get_username_from_payload_handler(payload):
    username = payload.get('sub').replace('|', '.')
    authenticate(remote_user=username)
    return username

def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('dev-o1pgfoz1hqx3xfij.us.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')
    
    issuer = 'https://{}/'.format('dev-o1pgfoz1hqx3xfij.us.auth0.com')
    expected_audience = 'http://localhost:8000/companyapi'
    final_audience = ''

    # Decode without verifying to inspect the audience
    decoded_token = jwt.decode(token, public_key, algorithms=['RS256'], options={"verify_aud": False})
    
    # Check if the expected audience is in the audience claim
    print(decoded_token['aud'][0])
    if decoded_token['aud'][0] == expected_audience:
        final_audience = decoded_token['aud']

    issuer = 'https://{}/'.format('dev-o1pgfoz1hqx3xfij.us.auth0.com')
    return jwt.decode(token, public_key, audience=final_audience, issuer=issuer, algorithms=['RS256'])