# MinecraftServerScanner

A Server Scanner written in python, originally made with the purpose to find the LiveOverflow Server.

# Documentation

`-j` `--java` Scan for Minecraft Java Servers. Requires one or more CIDR Notated Ranges separated by spaces.  
`-b` `--bedrock` Scan for Minecraft Bedrock Servers. Requires one or more CIDR Notated Ranges separated by spaces.  
`-p` `--players` Scan for specific players in the playerlist.   
`-pO` `--port` Port to use. **DEFAULTS TO 25565 SO IT MUST BE USED WHEN SCANNING FOR BEDROCK SERVERS**  
`-d` `--debug` Logs to the console window for every server with status or error messages.  

# Features

 - Scans for either Bedrock or Java servers
 - Supports an exclude.conf file in the same format as masscan
 - Logs to a json file when servers are found. *It can and will make weird or invalid json if the file exists beforehand, so I'd rename or delete the old log file before rerunning the script.

# Other Info
When I ran it, it ran was jumping between 400-1000, and it took about an hour to scan ~2,600,000 IP adresses with a single port.

I wouldn't recommend using it on your home wifi if possible, because of a thing called https://abuseipdb.com. As far as i'm aware, it's mostly cosmetic, and doesn't appear to actually do anything. If you can get a good cloud provider though, you can often prevent dropped packets (if that actually occurs for this script) which can find servers eaiser.

You might get reported to your ISP if you do it too much though.
