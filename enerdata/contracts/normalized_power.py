NORMALIZED_POWERS = {
    191: ('1x127', '1.5'),
    200: ('1x133', '1.5'),
    330: ('1x220', '1.5'),
    345: ('1x230', '1.5'),
    381: ('1x127', '3'),
    399: ('1x133', '3'),
    445: ('1x127', '3.5'),
    466: ('1x133', '3.5'),
    572: ('3x220/127', '1.5'),
    598: ('3x230/133', '1.5'),
    635: ('1x127', '5'),
    660: ('1x220', '3'),
    665: ('1x133', '5'),
    690: ('1x230', '3'),
    770: ('1x220', '3.5'),
    805: ('1x230', '3.5'),
    953: ('1x127', '7.5'),
    987: ('3x380/220', '1.5'),
    998: ('1x133', '7.5'),
    1039: ('3x400/230', '1.5'),
    1100: ('1x220', '5'),
    1143: ('3x220/127', '3'),
    1150: ('1x230', '5'),
    1195: ('3x230/133', '3'),
    1270: ('1x127', '10'),
    1330: ('1x133', '10'),
    1334: ('3x220/127', '3.5'),
    1394: ('3x230/133', '3.5'),
    1650: ('1x220', '7.5'),
    1725: ('1x230', '7.5'),
    1905: ('1x127', '15'),
    1975: ('3x380/220', '3'),
    1992: ('3x230/133', '5'),
    1995: ('1x133', '15'),
    2078: ('3x400/230', '3'),
    2200: ('1x220', '10'),
    2300: ('1x230', '10'),
    2304: ('3x380/220', '3.5'),
    2425: ('3x400/230', '3.5'),
    2540: ('1x127', '20'),
    2660: ('1x133', '20'),
    2858: ('3x220/127', '7.5'),
    2988: ('3x230/133', '7.5'),
    3175: ('1x127', '25'),
    3291: ('3x380/220', '5'),
    3300: ('1x220', '15'),
    3325: ('1x133', '25'),
    3450: ('1x230', '15'),
    3464: ('3x400/230', '5'),
    3810: ('1x127', '30'),
    3811: ('3x220/127', '10'),
    3984: ('3x230/133', '10'),
    3990: ('1x133', '30'),
    4400: ('1x220', '20'),
    4445: ('1x127', '35'),
    4600: ('1x230', '20'),
    4655: ('1x133', '35'),
    4936: ('3x380/220', '7.5'),
    5080: ('1x127', '40'),
    5196: ('3x400/230', '7.5'),
    5320: ('1x133', '40'),
    5500: ('1x220', '25'),
    5715: ('1x127', '45'),
    5716: ('3x220/127', '15'),
    5750: ('1x230', '25'),
    5976: ('3x230/133', '15'),
    5985: ('1x133', '45'),
    6350: ('1x127', '50'),
    6582: ('3x380/220', '10'),
    6600: ('1x220', '30'),
    6650: ('1x133', '50'),
    6900: ('1x230', '30'),
    6928: ('3x400/230', '10'),
    7621: ('3x220/127', '20'),
    7700: ('1x220', '35'),
    7967: ('3x230/133', '20'),
    8001: ('1x127', '63'),
    8050: ('1x230', '35'),
    8379: ('1x133', '63'),
    8800: ('1x220', '40'),
    9200: ('1x230', '40'),
    9526: ('3x220/127', '25'),
    9873: ('3x380/220', '15'),
    9900: ('1x220', '45'),
    9959: ('3x230/133', '25'),
    10350: ('1x230', '45'),
    10392: ('3x400/230', '15'),
    11000: ('1x220', '50'),
    11432: ('3x220/127', '30'),
    11500: ('1x230', '50'),
    11951: ('3x230/133', '30'),
    13164: ('3x380/220', '20'),
    13337: ('3x220/127', '35'),
    13856: ('3x400/230', '20'),
    13860: ('1x220', '63'),
    13943: ('3x230/133', '35'),
    14490: ('1x230', '63'),
    15242: ('3x220/127', '40'),
    15935: ('3x230/133', '40'),
    16454: ('3x380/220', '25'),
    17147: ('3x220/127', '45'),
    17321: ('3x400/230', '25'),
    17927: ('3x230/133', '45'),
    19053: ('3x220/127', '50'),
    19745: ('3x380/220', '30'),
    19919: ('3x230/133', '50'),
    20785: ('3x400/230', '30'),
    23036: ('3x380/220', '35'),
    24006: ('3x220/127', '63'),
    24249: ('3x400/230', '35'),
    25097: ('3x230/133', '63'),
    26327: ('3x380/220', '40'),
    27713: ('3x400/230', '40'),
    29618: ('3x380/220', '45'),
    31177: ('3x400/230', '45'),
    32909: ('3x380/220', '50'),
    34641: ('3x400/230', '50'),
    41465: ('3x380/220', '63'),
    43648: ('3x400/230', '63')
}


class NormalizedPower(object):

    def get_volt_int(self, pot):
        volt_int = NORMALIZED_POWERS.get(pot, None)
        if volt_int is None:
            raise ValueError('The given power is not normalized')
        return volt_int

    def is_normalized(self, pot):
        return pot in NORMALIZED_POWERS

    def get_norm_powers(self, pot_min, pot_max):
        for norm_pow in sorted(NORMALIZED_POWERS):
            if pot_min < norm_pow <= pot_max:
                yield norm_pow
            elif norm_pow > pot_max:
                break
