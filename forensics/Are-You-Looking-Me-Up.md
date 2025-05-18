# Are You Looking Me Up?
Description:
```markdown
The network has a DNS server that's been receiving a lot of traffic. You've been handed a set of raw network logs. Your job? Hunt down the DNS server that has received the most DNS requests.

Use the log file found [here](https://byu.box.com/s/2rong02xtfx7sfo52nos3ra2waifogv2)

Analyze the logs and find the impostor.

Flag format: `byuctf{IP1}`
```

**Author**: `Welsh Dragon`

## Writeup
Look for which devices have a lot of UDP port 53 traffic:

```bash
cat logs.txt | grep udp | awk -F',' '$22 == 53 {print $20}' | sort | uniq -c | sort -nr | head
```

**Flag** - `byuctf{172.16.0.1}`