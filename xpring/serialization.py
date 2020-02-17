"""
Derived from the sample code on the developer portal:

https://github.com/ripple/xrpl-dev-portal/blob/57dd03d9a1ff610c12c692ead93a6acb06cfe950/content/_code-samples/tx-serialization/serialize.py
"""

import json
import pkg_resources
import re
import typing as t

import typing_extensions as tex

from xpring.bits import from_bytes, to_bytes
from xpring.codec import DEFAULT_CODEC
from xpring.issued_amount import IssuedAmount
from xpring.types import AccountId, Address, Amount


def field_id(type_code, field_code):
    """
    Encode a field ID from its type and field codes.

    The encoding occupies 1 to 3 bytes depending on whether the codes are
    "common" (<16) or "uncommon" (>=16).
    """
    # Codes must be nonzero and fit in 1 byte.
    assert 0 < type_code < 256
    assert 0 < field_code < 256

    # Each code takes a nibble (4 bits) in the first byte.
    # If a code spills over the nibble (i.e. >=16), then the nibble is
    # filled with zeroes and the code is given a trailing byte.
    # Type always comes before field.

    if type_code < 16 and field_code < 16:
        return to_bytes(type_code << 4 | field_code, 1)
    if type_code >= 16 and field_code < 16:
        return to_bytes(field_code << 8 | type_code, 2)
    if type_code < 16 and field_code >= 16:
        return to_bytes(type_code << 12 | field_code, 2)
    return to_bytes(type_code << 8 | field_code, 3)


def vl_encode(blob: bytes) -> bytes:
    """
    Encode a variable length type.

    Prefixes an arbitrary byte array (a "blob") with an encoded length. The
    length of the prefix is 1 to 3 bytes depending on the length of the blob:

    <= 918744 bytes: prefix is 3 bytes
    <= 12480 bytes: prefix is 2 bytes
    <= 192 bytes: prefix is 1 byte
    """
    length = len(blob)
    if length > 918744:
        raise ValueError(
            'variable length field must not be longer than 918744 bytes'
        )
    if length > 12480:
        prefix = to_bytes(length - 12481 + (241 << 16), 3)
    elif length > 192:
        prefix = to_bytes(length - 193 + (193 << 8), 2)
    else:
        prefix = bytes([length])
    return prefix + blob


def serialize_account_id(address: str) -> bytes:
    return vl_encode(DEFAULT_CODEC.decode_address(t.cast(Address, address)))


def serialize_amount(amount: Amount) -> bytes:
    """
    Serialize an Amount.

    An XRP Amount comes as a string. It must be serialized to 64 bits:
    1 zero bit, 1 sign bit (zero for negative, one for positive), 62 bits of
    absolute value.

    A non-XRP Amount comes as a dictionary. It must be serialized thus:
    64 bits of unsigned value; 160 bit currency code; 160 bit issuer
    AccountID.
    """
    if isinstance(amount, str):
        value = int(amount)
        sign = int(value > 0)
        magnitude = abs(value)
        assert magnitude <= 10**17
        return to_bytes(sign << 62 | magnitude, 8)
    if isinstance(amount, dict):
        value_bytes = IssuedAmount(amount['value']).to_bytes()
        currency_bytes = serialize_currency(amount['currency'])
        address_bytes = DEFAULT_CODEC.decode_address(
            t.cast(Address, amount['issuer'])
        )
        return value_bytes + currency_bytes + address_bytes
    raise ValueError('Amount must be `str` or `{value, currency, issuer}`')


def serialize_array(array: t.Iterable) -> bytes:
    """Serialize an array of objects."""
    return b''.join(
        serialize_object(item, mark=False) for item in array
    ) + ARRAY_END_MARKER


def serialize_blob(blob_hex: str) -> bytes:
    return vl_encode(bytes.fromhex(blob_hex))


# ISO 4217 3-character currency code
CURRENCY_CODE_PATTERN = re.compile(r'^[][A-Za-z0-9?!@#$%^&*<>(){}|]{3}$')
HEX_160_PATTERN = re.compile(r'^[0-9a-fA-F]{40}$')


def serialize_currency(currency: str) -> bytes:
    if CURRENCY_CODE_PATTERN.match(currency):
        if currency == 'XRP':
            # Rare, but when the currency code "XRP" is serialized,
            # it's a special-case: all zeroes.
            return bytes(20)

        code_ascii = currency.encode('ASCII')
        # standard currency codes: https://xrpl.org/currency-formats.html#standard-currency-codes
        # 8 bits type code (0x00)
        # 88 bits reserved (zeroes)
        # 24 bits ASCII
        # 16 bits version (0x0000)
        # 24 bits reserved (zeroes)
        return bytes(12) + code_ascii + bytes(5)

    if HEX_160_PATTERN.match(currency):
        return bytes.fromhex(currency)

    raise ValueError(f'unknown currency code: {currency}')


def serialize_field(field, value):
    id_bytes = field['id']
    serialize = field['serialize']
    if serialize is None:
        field_name = field['name']
        field_type = field['type']
        raise NotImplementedError(
            f'cannot serialize field {field_name} ({field_type})'
        )
    try:
        value_bytes = serialize(value)
    except ValueError as cause:
        field_type = field['type']
        field_name = field['name']
        raise ValueError(f'field {field_name} ({field_type}): {str(cause)}')
    return id_bytes + value_bytes


def serialize_hash(bits: int, value: str) -> bytes:
    blob = bytes.fromhex(value)
    if len(blob) * 8 != bits:
        raise ValueError(f'expected {bits} bits: {value}')
    return blob


def serialize_hash128(value: str) -> bytes:
    return serialize_hash(128, value)


def serialize_hash160(value: str) -> bytes:
    return serialize_hash(160, value)


def serialize_hash256(value: str) -> bytes:
    return serialize_hash(256, value)


def field_key(field):
    try:
        return field['key']
    except KeyError as error:
        raise AssertionError(f'field {field_name} missing key')


def serialize_object(
    object_: dict, signing: bool = False, mark: bool = True
) -> bytes:
    fields = [FIELDS_BY_NAME[name] for name in object_.keys()]
    fields = [
        field for field in fields
        if field['isSerialized'] and (not signing or field['isSigningField'])
    ]
    fields = sorted(fields, key=field_key)

    blob = bytearray()
    for field in fields:
        blob.extend(serialize_field(field, object_[field['name']]))
    if mark:
        blob.extend(OBJECT_END_MARKER)
    return blob


def serialize_path(path: t.Collection) -> bytes:
    print(f'path: {path}')
    if not len(path):
        raise ValueError('a Path must not be empty')
    return b''.join(serialize_step(step) for step in path)


def serialize_pathset(pathset: t.Collection) -> bytes:
    print(f'pathset: {pathset}')
    if not len(pathset):
        raise ValueError('a PathSet must not be empty')
    return PATH_END_MARKER.join(
        serialize_path(path) for path in pathset
    ) + PATHSET_END_MARKER


def serialize_step(step: t.Mapping) -> bytes:
    blob = bytearray([0])
    if 'account' in step:
        blob[0] |= 0x01
        blob.extend(DEFAULT_CODEC.decode_address(step['account']))
    if 'currency' in step:
        blob[0] |= 0x10
        blob.extend(serialize_currency(step['currency']))
    if 'issuer' in step:
        blob[0] |= 0x20
        blob.extend(DEFAULT_CODEC.decode_address(step['issuer']))
    return blob


def serialize_transaction_type(name: str) -> bytes:
    return to_bytes(TRANSACTION_TYPES_BY_NAME[name], 2)


def serialize_uint(bits: int, value: int) -> bytes:
    assert 0 <= value < (1 << bits)
    return to_bytes(value, bits // 8)


def serialize_uint8(value: int) -> bytes:
    return serialize_uint(8, value)


def serialize_uint16(value: int) -> bytes:
    return serialize_uint(16, value)


def serialize_uint32(value: int) -> bytes:
    return serialize_uint(32, value)


def serialize_uint64(value: int) -> bytes:
    return serialize_uint(64, value)


class Scanner:

    def __init__(self, stream: bytes) -> None:
        self.stream = stream
        self.cursor = 0

    @property
    def inexhausted(self):
        return self.cursor < len(self.stream)

    def __bool__(self):
        return self.inexhausted

    def peek1(self) -> int:
        return self.stream[self.cursor]

    def skip(self, length: int) -> None:
        self.cursor += length

    def take1(self) -> int:
        self.cursor += 1
        return self.stream[self.cursor - 1]

    def take(self, length: int) -> bytes:
        self.cursor += length
        return self.stream[(self.cursor - length):self.cursor]


def vl_decode(scanner: Scanner) -> bytes:
    """Return the next variable-length blob while advancing the cursor.

    https://xrpl.org/serialization.html#length-prefixing
    """
    byte1 = scanner.take1()
    if byte1 < 193:
        length = byte1
    elif byte1 < 241:
        byte2 = scanner.take1()
        length = 193 + (byte1 - 193) * 256 + byte2
    elif byte1 < 255:
        byte2 = scanner.take1()
        byte3 = scanner.take1()
        length = 12481 + (byte1 - 241) * 645536 + byte2 * 256 + byte3
    else:
        raise ValueError(f'not a length prefix: {byte1}')
    return scanner.take(length)


def deserialize_account_id(scanner: Scanner) -> Address:
    account_id = t.cast(AccountId, vl_decode(scanner))
    return DEFAULT_CODEC.encode_address(account_id)


def deserialize_amount(scanner: Scanner) -> Amount:
    byte1 = scanner.peek1()
    # Most-significant bit is the format bit. 1 means "is not XRP".
    if not byte1 & (1 << 7):
        # Second most-significant bit is the sign bit. 1 means "is positive".
        sign = 1 if byte1 & (1 << 6) else -1
        # Format bit is already cleared, but clear both top bits regardless.
        magnitude = from_bytes(scanner.take(8)) & ~(0b11 << 62)
        return str(sign * magnitude)
    # TODO: Deserialize a floating point number.
    value = scanner.take(8).hex()
    currency = deserialize_currency(scanner)
    issuer = DEFAULT_CODEC.encode_address(t.cast(AccountId, scanner.take(20)))
    return {'value': value, 'currency': currency, 'issuer': issuer}


def deserialize_array(scanner: Scanner) -> t.List:
    array = []
    while scanner.peek1() != ARRAY_END_MARKER:
        key, value = deserialize_field(scanner)
        array.append({key: value})
    scanner.skip(1)
    return array


def deserialize_blob(scanner: Scanner) -> str:
    return vl_decode(scanner).hex().upper()


def deserialize_currency(scanner: Scanner) -> str:
    blob = scanner.take(160 // 8)
    # If the first 8 bits are 0x00, it is a standard currency code.
    # https://xrpl.org/currency-formats.html#standard-currency-codes
    if not blob[0]:
        return blob[12:15].decode('ASCII')
    # Otherwise, it is a nonstandard currency code.
    return blob.hex().upper()


def deserialize_field(scanner: Scanner) -> t.Tuple[str, t.Any]:
    type_code, field_code = deserialize_field_key(scanner)
    field = FIELDS_BY_ID[(type_code, field_code)]
    deserialize = field['deserialize']
    if deserialize is None:
        field_name = field['name']
        field_type = field['type']
        raise NotImplementedError(
            f'cannot deserialize field {field_name} ({field_type})'
        )
    value = deserialize(scanner)
    return (field['name'], value)


TypeCode = t.NewType('TypeCode', int)
FieldCode = t.NewType('FieldCode', int)


def deserialize_field_key(scanner: Scanner) -> t.Tuple[TypeCode, FieldCode]:
    byte1 = scanner.take1()
    type_code = byte1 >> 4
    if not type_code:
        type_code = scanner.take1()
    field_code = byte1 & 0x0F
    if not field_code:
        field_code = scanner.take1()
    return (t.cast(TypeCode, type_code), t.cast(FieldCode, field_code))


def deserialize_hash(bits: int, scanner: Scanner) -> str:
    return scanner.take(bits // 8).hex().upper()


def deserialize_hash128(scanner: Scanner) -> str:
    return deserialize_hash(128, scanner)


def deserialize_hash160(scanner: Scanner) -> str:
    return deserialize_hash(160, scanner)


def deserialize_hash256(scanner: Scanner) -> str:
    return deserialize_hash(256, scanner)


def deserialize_object(scanner: Scanner) -> t.Mapping:
    object_ = {}
    while scanner.peek1() != OBJECT_END_MARKER:
        key, value = deserialize_field(scanner)
        object_[key] = value
    scanner.skip(1)
    return object_


Step = tex.TypedDict(
    'Step', {
        'account': Address,
        'currency': str,
        'issuer': Address
    },
    total=False
)
Path = t.Collection[Step]
PathSet = t.Collection[Path]


def deserialize_path(scanner: Scanner) -> Path:
    path = []
    while scanner.peek1() not in (PATH_END_MARKER, PATHSET_END_MARKER):
        path.append(deserialize_step(scanner))
    if scanner.peek1() == PATH_END_MARKER:
        scanner.skip(1)
    return path


def deserialize_pathset(scanner: Scanner) -> PathSet:
    pathset = []
    while scanner.peek1() != PATHSET_END_MARKER:
        pathset.append(deserialize_path(scanner))
    scanner.skip(1)
    return pathset


def deserialize_step(scanner: Scanner) -> Step:
    header = scanner.take1()
    step = t.cast(Step, {})
    if header & 0x01:
        step['account'] = DEFAULT_CODEC.encode_address(
            t.cast(AccountId, scanner.take(20))
        )
    if header & 0x10:
        step['currency'] = deserialize_currency(scanner)
    if header & 0x20:
        step['issuer'] = DEFAULT_CODEC.encode_address(
            t.cast(AccountId, scanner.take(20))
        )
    return step


def deserialize_transaction_type(scanner: Scanner) -> str:
    return TRANSACTION_TYPES_BY_CODE[from_bytes(scanner.take(2))]


def deserialize_uint(bits: int, scanner: Scanner) -> int:
    return from_bytes(scanner.take(bits // 8))


def deserialize_uint8(scanner: Scanner) -> int:
    return deserialize_uint(8, scanner)


def deserialize_uint16(scanner: Scanner) -> int:
    return deserialize_uint(16, scanner)


def deserialize_uint32(scanner: Scanner) -> int:
    return deserialize_uint(32, scanner)


def deserialize_uint64(scanner: Scanner) -> int:
    return deserialize_uint(64, scanner)


CODECS = {
    'AccountID': (serialize_account_id, deserialize_account_id),
    'Amount': (serialize_amount, deserialize_amount),
    'Blob': (serialize_blob, deserialize_blob),
    'Hash128': (serialize_hash128, deserialize_hash128),
    'Hash160': (serialize_hash160, deserialize_hash160),
    'Hash256': (serialize_hash256, deserialize_hash256),
    'PathSet': (serialize_pathset, deserialize_pathset),
    'STArray': (serialize_array, deserialize_array),
    'STObject': (serialize_object, deserialize_object),
    'UInt8': (serialize_uint8, deserialize_uint8),
    'UInt16': (serialize_uint16, deserialize_uint16),
    'UInt32': (serialize_uint32, deserialize_uint32),
    'UInt64': (serialize_uint64, deserialize_uint64),
    'Vector256': (None, None),
}

# TODO: Consider lazy initialization.
_DEFINITIONS = json.load(
    pkg_resources.resource_stream('xpring', 'definitions.json')
)
TRANSACTION_TYPES_BY_NAME = _DEFINITIONS['TRANSACTION_TYPES']
TRANSACTION_TYPES_BY_CODE = {
    v: k for (k, v) in TRANSACTION_TYPES_BY_NAME.items()
}
TYPES_BY_NAME = _DEFINITIONS['TYPES']
TYPES_BY_CODE = {v: k for (k, v) in TYPES_BY_NAME.items()}
FIELDS_BY_NAME = {k: v for (k, v) in _DEFINITIONS['FIELDS']}
for field_name, field in FIELDS_BY_NAME.items():
    type_name = field['type']
    type_code = TYPES_BY_NAME[type_name]
    field_code = field['nth']
    field['name'] = field_name
    if field['isSerialized']:
        assert 0 < type_code < 256 and 0 < field_code < 256
        field['key'] = (type_code, field_code)
        field['id'] = field_id(type_code, field_code)
        field['serialize'], field['deserialize'] = CODECS[type_name]
FIELDS_BY_NAME['TransactionType']['serialize'] = serialize_transaction_type
FIELDS_BY_NAME['TransactionType']['deserialize'] = deserialize_transaction_type
FIELDS_BY_ID = {v['key']: v for v in FIELDS_BY_NAME.values() if 'key' in v}
PATH_END_MARKER = b'\xFF'
PATHSET_END_MARKER = b'\x00'
ARRAY_END_MARKER = FIELDS_BY_NAME['ArrayEndMarker']['id']
OBJECT_END_MARKER = FIELDS_BY_NAME['ObjectEndMarker']['id']
