import dns.resolver


def get_ip_address(hostname):
    """
    Performs a DNS lookup using the dnspython library.
    """

    resolver = dns.resolver.Resolver()
    try:
        answers = resolver.resolve(hostname, "A")  # Query for A records
        return str(answers[0].address)  # Return the first IP address
    except dns.resolver.ResolverError as e:
        print(f"DNS lookup error: {e}")
        return None
