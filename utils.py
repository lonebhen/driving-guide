from logging import log
import re


def is_valid_phone_number(msisdn: str):
    pattern = r"^(00233|0233|\+233|233|0)(23|24|25|53|54|55|27|57|59|28|20|50|26|56|30|31|32|33|34|35|37|38|39)\d{7}$"
    return bool(re.match(pattern, msisdn))

def phone_number_format(msisdn: str):

    if not is_valid_phone_number(msisdn):
        msisdn = None
    else:
        if msisdn.startswith("00233"):
            msisdn = msisdn[2:]
        elif msisdn.startswith("0233"):
            msisdn = msisdn[1:]
        elif msisdn.startswith("0"):
            msisdn = "233" + msisdn[1:]
        elif msisdn.startswith("+"):
            msisdn = msisdn[1:]
        elif not msisdn.startswith("233"):
            msisdn = "233" + msisdn

    print(f"Formatted number: {msisdn}")
    return msisdn
