LOG_FILE_CONTENT = """
*.amazon.co.uk    89
*.doubleclick.net    139
*.fbcdn.net    212
*.in-addr.arpa    384
*.l.google.com    317
1.client-channel.google.com    110
6.client-channel.google.com    45
a.root-servers.net    1059
apis.google.com    43
clients4.google.com    71
clients6.google.com    81
connect.facebook.net    68
edge-mqtt.facebook.com    56
graph.facebook.com    150
mail.google.com    128
mqtt-mini.facebook.com    47
ssl.google-analytics.com    398
star-mini.c10r.facebook.com    46
staticxx.facebook.com    48
www.facebook.com    178
www.google.com    162
www.google-analytics.com    127
www.googleapis.com    87
"""


def get_clean_domains(log_file):
    clean_domains = []
    for line in log_file.split('\n'):
        if line.strip() == '':
            continue
        domain = line.split()[0]
        domain_parts = domain.split('.')
        if len(domain_parts) == 3 and domain_parts[1] in ('co', 'com'):
            clean_domain = '.'.join(domain_parts[0:3])
        else:
            clean_domain = '.'.join(domain_parts[-2:])
        clean_domains.append(clean_domain)
    return clean_domains


def count_accesses(log_file, clean_domains):
    domain_accesses = {}
    for line in log_file.split('\n'):
        if line.strip() == '':
            continue
        domain, accesses = line.split()
        clean_domain = clean_domains.pop(0)
        if clean_domain in domain_accesses:
            domain_accesses[clean_domain] += int(accesses)
        else:
            domain_accesses[clean_domain] = int(accesses)
    return domain_accesses


def format_output(domain_accesses, min_hits=0):
    total_accesses = {}
    for domain, accesses in domain_accesses.items():
        domain_name = '.'.join(domain.split('.')[-2:])
        if domain_name in total_accesses:
            total_accesses[domain_name] += accesses
        else:
            total_accesses[domain_name] = accesses
    sorted_domains = sorted(total_accesses.items(), key=lambda x: x[1], reverse=True)
    output_lines = []
    for domain_name, accesses in sorted_domains:
        if accesses >= min_hits:
            output_lines.append(f'{domain_name} ({accesses})')
    return '\n'.join(output_lines)


def count_domains(log_file, min_hits=0):
    clean_domains = get_clean_domains(log_file)
    domain_accesses = count_accesses(log_file, clean_domains)
    output_str = format_output(domain_accesses, min_hits)
    return output_str


def main():
    log_file = LOG_FILE_CONTENT
    min_hits = 500
    output_str = count_domains(log_file, min_hits)
    print(output_str)


if __name__ == "__main__":
    main()
