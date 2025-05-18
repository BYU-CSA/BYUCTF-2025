# Mine Over Matter
Description:
```markdown
Your SOC has flagged unusual outbound traffic on a segment of your network. After capturing logs from the router during the anomaly, they handed it over to you—the network analyst.

Somewhere in this mess, two compromised hosts are secretly mining cryptocurrency and draining resources. Analyze the traffic, identify the two rogue IP addresses running miners, and report them to the Incident Response team before your network becomes a crypto farm.

Use the log file found [here](https://byu.box.com/s/2rong02xtfx7sfo52nos3ra2waifogv2)

Flag format: `byuctf{IP1,IP2}` (*it doesn't which order the IPs are in*)
```

**Author**: `Welsh Dragon`

## Writeup
Create a solve script that does a reverse DNS lookup on all the destination IP addresses in the log file. 

See [`solve.py`](./solve.py).

**Flag** - `byuctf{172.16.0.5,172.16.0.10}` or `byuctf{172.16.0.10,172.16.0.5}`