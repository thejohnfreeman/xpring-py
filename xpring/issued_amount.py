from decimal import getcontext, Decimal

from xpring.bits import to_bytes


class IssuedAmount:
    """
    Serializes issued currency amounts from string number representations,
    matching the precision of the XRP Ledger.
    """
    """
    Zero has a special-case canonical format:
    - one "not XRP" bit set to 1
    - one sign bit set to 0 (for "negative")
    - sixty-two value bits set to 0
    """
    CANONICAL_ZERO = to_bytes(1 << 63, 8)

    MANTISSA_MIN = 10**15
    MANTISSA_MAX = 10**16 - 1
    EXPONENT_MIN = -96
    EXPONENT_MAX = 80

    def __init__(self, value: str):
        self.context = getcontext()
        self.context.prec = 15
        self.context.Emin = self.EXPONENT_MIN
        self.context.Emax = self.EXPONENT_MAX
        self.decimal = Decimal(value)

    def to_bytes(self):
        if self.decimal.is_zero():
            return self.CANONICAL_ZERO

        # Convert components to integers.
        sign, digits, exponent = self.decimal.as_tuple()
        mantissa = int(''.join(str(d) for d in digits))

        # Canonicalize to expected range.
        while mantissa < self.MANTISSA_MIN and exponent > self.EXPONENT_MIN:
            mantissa *= 10
            exponent -= 1

        while mantissa > self.MANTISSA_MAX:
            if exponent >= self.EXPONENT_MAX:
                raise ValueError('amount overflow')
            mantissa //= 10
            exponent += 1

        if exponent < self.EXPONENT_MIN or mantissa < self.MANTISSA_MIN:
            # Round to zero.
            return self.CANONICAL_ZERO

        if exponent > self.EXPONENT_MAX or mantissa > self.MANTISSA_MAX:
            raise ValueError('amount overflow')

        # Serialize to bytes.
        serial = 1 << 63  # "not XRP" bit
        if sign == 0:
            serial |= 1 << 62  # "is positive" bit
        serial |= ((exponent + 97) << 54)  # 8 bits of exponent
        serial |= mantissa  # 54 bits of mantissa

        return to_bytes(serial, 8)
