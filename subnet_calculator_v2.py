import pandas as pd


def str_split(string: str) -> list:
    return [string[j: j + 8] for j in range(0, 32, 8)]


def ip_class(ip_bin_f: list) -> str:
    class_map = {
        '0': 'A',
        '10': "B",
        '110': 'C',
        '1110': 'D',
        "11110": "E"
    }

    for prefix, addr_class in class_map.items():
        if "".join(ip_bin_f).startswith(prefix):
            return addr_class
    return ''


def addr_scope(ip_bin_f: list) -> str:
    private_addr = ["00001010", "1010110000010000", "1010110000011111", "1100000010101000"]
    for prefix in private_addr:
        if "".join(ip_bin_f).startswith(prefix):
            return "private"
    return "public"


def first_usable(addr: list) -> str:
    return "".join(addr)[:-1] + "1"


def last_usable(addr: list) -> str:
    return "".join(addr)[:-1] + "0"


def net(addr: list, mazk) -> str:
    return f'{("".join(addr)[:mazk]):0<32}'


def broad(addr: list, mazk) -> str:
    return f'{("".join(addr)[:mazk]):1<32}'


def decimal(addr: list):
    return list(map(lambda x: int(x, 2), addr))


def valid_ip():
    while True:
        try:
            ip_addr = input("Enter IPv4 Address: ").split(".")
            if all(x in range(0, 256) for x in map(int, ip_addr)) and (len(ip_addr) == 4):
                return ip_addr
            print("invalid ip address!")
        except ValueError:
            print("ip address should be in dotted decimal format")


def valid_mask():
    while True:
        try:
            ip_mask = int(input("Enter a mask [1 - 30]: "))
            if ip_mask in range(1, 31):
                return ip_mask
        except ValueError:
            print('invalid mask')


def addr_type(ip_addr: list) -> str:
    dic = {
        net(ip_addr, mask): 'network', broad(ip_addr, mask): 'broadcast'
    }
    return dic.get(''.join(ip_addr), 'host')


def to_dotted_decimal(ip_list):
    return '.'.join(map(str, ip_list))


chars = 80
print("#" * chars)
print('Subnet calculator v0.2 by don_simone')

ip = valid_ip()
mask = valid_mask()

octet = mask // 8
subnet_bits = mask % 8
total_subnets = 2 ** subnet_bits

host_bits = 32 - mask

bin_ip = [f"{x:08b}" for x in list(map(int, ip))]
subnet_mask_bin = str_split(f"{mask * '1':0<32}")
subnet_mask_dec = decimal(subnet_mask_bin)

net_addr_bin = str_split(net(bin_ip, mask))
net_addr_dec = decimal(net_addr_bin)
wildcard_bin = str_split(f"{mask * '0':1<32}")
wildcard_dec = decimal(wildcard_bin)
my_subnet = [[ip, bin_ip], [subnet_mask_dec, subnet_mask_bin]]

total_hosts = 2 ** host_bits
usable_hosts = total_hosts - 2
scope = addr_scope(bin_ip)
class_ip = ip_class(bin_ip)
hex_id = "0x" + "".join([f"{x:02x}" for x in map(int, ip)])
arpa = f'{".".join([x for x in ip[::-1]])}.in-addr.arpa.'
ipv4_mapped = f"::ffff:{hex_id[:4]}.{hex_id[4:8]}"
stats = [total_hosts, usable_hosts, scope, class_ip, hex_id, arpa, ipv4_mapped]

print("=" * chars)
print(f'all {total_subnets} possible /{mask} networks for {".".join(ip[:octet]) + (4 - octet) * ".*"}')
print("=" * chars)

base_mask = mask - (mask % 8)
sub_step = 256 // total_subnets
base_sub_bin = str_split(net(bin_ip, base_mask))
curr_subnet_bin = base_sub_bin
all_addresses = []

for i in range(total_subnets):
    mark = ''
    curr_subnet_bin[octet] = f"{sub_step * i:08b}"
    broadcast = str_split(broad(curr_subnet_bin, mask))
    first = str_split(first_usable(curr_subnet_bin))
    last = str_split(last_usable(broadcast))

    if net_addr_dec == decimal(curr_subnet_bin):
        my_subnet.extend([[decimal(curr_subnet_bin), curr_subnet_bin], [decimal(broadcast), broadcast],
                          [decimal(first), first], [decimal(last), last]])

        mark = '<--'

    all_addresses.append([decimal(curr_subnet_bin), decimal(first), decimal(last), decimal(broadcast), [mark]])

pd.options.display.max_colwidth = None
df = pd.DataFrame(all_addresses, columns=['network address', 'first usable', 'last usable', 'broadcast address', 'you'])
df = df.map(to_dotted_decimal)

print(df)

print("=" * chars)
print(f'{".".join(ip)} /{mask} is a {addr_scope(bin_ip)} {addr_type(bin_ip)} address')
print("=" * chars)

my_subnet.append([wildcard_dec, wildcard_bin])
df_a = pd.DataFrame(my_subnet,
                    columns=['decimal', 'binary'],
                    index=['ip address', 'subnet mask', 'network address', 'broadcast address',
                           'first usable', 'last usable', 'wildcard mask'])

df_a = df_a.map(to_dotted_decimal)
df_b = pd.DataFrame(stats,
                    columns=[''],
                    index=['total hosts', 'usable hosts', 'scope', 'class', 'hex id', 'arpa', 'ipv4 mapped'])

print(df_a)
print("=" * chars)
print(df_b)
# df.to_csv('data.csv', index=False, na_rep='')