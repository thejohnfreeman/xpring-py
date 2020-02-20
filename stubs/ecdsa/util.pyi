import typing as t

Decoder = t.Callable[[str, int], bytes]
Encoder = t.Callable[[int, int, int], bytes]

sigdecode_der: Decoder
sigencode_string: Encoder
sigencode_der_canonize: Encoder
