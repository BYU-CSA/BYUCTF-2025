import subprocess, re

inputFile = "logs.txt" 
uniqueIPsDest = set()
uniqueIPsSrc = set()
ipDomainMap = {}

with open(inputFile, 'r') as file:
    for line in file:
        fields = line.strip().split(',')
        if len(fields) >= 20:
            destIP = fields[19]
            uniqueIPsDest.add(destIP)

for ip in sorted(uniqueIPsDest):
    try:
        result = subprocess.run(["nslookup", ip], capture_output=True, text=True, check=True)
        if 'mine' in result.stdout.strip():
            match = re.search(r'name\s*=\s*(.+)\.', result.stdout)
            domain = match.group(1)
            ipDomainMap[ip] = domain
            print(f"{ip} -> {domain}")
    except subprocess.CalledProcessError as e:
        pass

with open(inputFile, 'r') as file:
    for line in file:
        fields = line.strip().split(',')
        if len(fields) >= 20:
            srcIP = fields[19]
            for ip, domain in ipDomainMap.items():
                if ip == srcIP:
                    uniqueIPsSrc.add(fields[18])

print("Source Addresses For Miners")
for ip in uniqueIPsSrc:
    print(ip)
