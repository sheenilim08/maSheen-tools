
# maSheen-Tools

This is a collection of CLI-based client for public websites tooks like SSL Labs SSL Scanner.
## Support Tools
- SSL Labs SSL Scanner
- More will be added as I learn new stuff
## Demo
Clone this repo and enter the main folder. Issue the command below.

```
python3 main.py
```

When running the main file, you will get a menu of what tool you want to use.
 For now (as of Sept 17, 2026), only SSL Lab SSL Scanner is supported. You will be asked what public endpoint you want to scan.

NOTE: It is the sslscanner of SSL Labs that is doing the scanning. 

Sample Output (IP is deliberately changed to be wrong!):
```
maSheen-tools main  ❯ python3 main.py 

[+] Executing: SSL Labs SSL Scanner

Type in the endpiont you want to scan (e.g. vpn.myorg.com): vpn.myorg.org
URL https://api.ssllabs.com/api/v2/analyze?host=vpn.myorg.org&all=On&startNew=On
Scan is initiating.
Scan status: IN_PROGRESS
Scanning in progress, checking result again in 1 minute.
URL https://api.ssllabs.com/api/v2/analyze?host=vpn.myorg.org&all=On
Scan status: IN_PROGRESS
Scanning in progress, checking result again in 1 minute.
URL https://api.ssllabs.com/api/v2/analyze?host=vpn.myorg.org&all=On
Scan status: READY
Scan is complete, here is the result.
IP Address      | Grade Rating | Cert Common Name               | TLS Version    
321.269.472.300 | B            | vpn.myorg.org, vpn.myorg.org,  | TLS 1.0, TLS   
                |              | www.vpn.myorg.org              | 1.1, TLS 1.2 
```
## Authors

- [@sheenilim08](https://github.com/sheenilim08)

