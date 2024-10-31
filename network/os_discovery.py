import subprocess


# Host = ip or hostname

# OS detection


def os_discovery(Host):

    service = f"nmap {Host} -sV -version-intensity 8 -T4 --host-timeout 120"
    oS = f"nmap {Host} -O -T4 --host-timeout 120"
    output = subprocess.check_output(service, shell=True).decode('utf-8')
    services = []
    for line in output.splitlines():
        if "open" in line:
            parts = line.split()
            service_name = parts[2]
            services.append(service_name)
    return services
