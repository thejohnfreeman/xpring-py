SIGNATURE_EXAMPLES = (
    ('signing_key_hex', 'message_hex', 'signature_hex'),
    (
        # https://ed25519.cr.yp.to/python/sign.input
        # To understand these vectors, one must read the code:
        # https://ed25519.cr.yp.to/python/sign.py
        # This is the format:
        # signing key + verifying key : verifying key : message : signature + message
        # Don't ask me why the verifying key and message are needlessly
        # repeated in concatentations.
        (
            '9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60',
            '',
            'e5564300c360ac729086e2cc806e828a84877f1eb8e5d974d873e065224901555fb8821590a33bacc61e39701cf9b46bd25bf5f0595bbe24655141438e7a100b',
        ),
        (
            '3b26516fb3dc88eb181b9ed73f0bcd52bcd6b4c788e4bcaf46057fd078bee073',
            '4284abc51bb67235',
            'd6addec5afb0528ac17bb178d3e7f2887f9adbb1ad16e110545ef3bc57f9de2314a5c8388f723b8907be0f3ac90c6259bbe885ecc17645df3db7d488f805fa08',
        ),
    )
)
