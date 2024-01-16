import ipaddress
import tldextract


def validate_ip(ip):
    try:
        # 将字符串转换为 IPv4Address 或者 IPv6Address 对象
        ipaddress.IPv4Network(ip) if '.' in ip else ipaddress.IPv6Network(ip)

        return True

    except ValueError as e:
        print("Invalid IP Address")
        return False


def is_valid_domain(url):
    extracted = tldextract.extract(url)
    is_valid = all([extracted.domain, extracted.suffix])

    if is_valid:
        print('Valid domain')
    else:
        print('Invalid domain')
