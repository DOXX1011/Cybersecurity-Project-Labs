# Wazuh SIEM with Cisco Network Telemetry

## Overview

This project documents the design and implementation of a small detection lab built for a university Security Operations and Incident Management assessment. The lab was created to simulate a realistic small-business network where infrastructure events, endpoint activity, outages, and attack traffic could be collected, correlated, and investigated through a SIEM.

The main goal was not to prevent attacks, but to prove that the environment could detect, collect, and surface security-relevant events across network devices and endpoints.

## Project Goals

- Build a working SIEM environment based on the provided network topology
- Configure Cisco router and switches with secure management settings
- Connect Windows and Ubuntu endpoints with the correct addressing
- Forward Cisco syslog to the SIEM server
- Deploy Wazuh agents to Windows and Ubuntu endpoints
- Generate realistic test activity and validate detection visibility
- Simulate outages and attacks from Kali Linux systems
- Investigate how network telemetry and endpoint telemetry complement each other

## Lab Topology

The lab was based on a small segmented network with:

- Cisco Router (**R1**)
- Cisco Switches (**S1** and **S2**)
- Windows endpoint
- Ubuntu endpoint
- SIEM server
- Internal Kali attacker
- External Kali attacker

<!-- Add topology image here -->
<!-- Example:
![Lab Topology](./images/network-diagram.png)
-->

## Technologies Used

### Core Platform

- **Wazuh** for SIEM, agent management, log analysis, and vulnerability visibility
- **Suricata** for network intrusion detection
- **Ubuntu Server** for the SIEM host
- **Windows** and **Ubuntu** endpoints for telemetry generation
- **Kali Linux** for attack simulation

### Network Infrastructure

- **Cisco Router 2811**
- **Cisco Catalyst Switches 3750**
- Syslog forwarding from Cisco IOS to Wazuh
- SPAN / port mirroring to feed traffic into Suricata

### Offensive / Test Tools

- **Nmap** for network reconnaissance
- **Medusa** for SSH brute-force testing

## What I Built

I implemented a working detection lab that combined endpoint telemetry, network telemetry, and infrastructure logging into one investigation environment.

The build included:

- Secure configuration of Cisco router and switches
- IP addressing and gateway configuration for all devices
- Verified network connectivity across the topology
- Cisco syslog forwarding to the SIEM server
- Wazuh agent deployment on Windows and Ubuntu
- Suricata integration for passive inspection of mirrored traffic
- Attack simulation from both internal and external attacker positions
- Detection validation inside the SIEM dashboard
- Custom rule work to improve visibility for specific events

## Security Configuration Highlights

The Cisco devices were configured using standard hardening measures, including:

- **SSHv2** for remote administration
- Local user authentication
- RSA key-based SSH setup
- Disabled Telnet access
- Encrypted passwords
- MOTD warning banner
- Disabled unnecessary HTTP services
- Syslog forwarding to the SIEM server
- Management IP addressing and gateway configuration

This part of the project gave me practical experience with real Cisco device configuration rather than only using virtual appliances.

## Detection Scenarios Completed

### 1. Infrastructure Logging

I configured Cisco switches and router to send syslog messages to the SIEM server. This allowed infrastructure-level events to appear alongside endpoint alerts inside Wazuh.

**Examples of visible events:**

- Login success / failure events
- Interface state changes
- Link up / link down messages
- Administrative shutdown events

### 2. Endpoint Visibility

I installed Wazuh agents on both Windows and Ubuntu systems and confirmed they were actively sending logs.

This created visibility for:

- Windows Security events
- Ubuntu/Linux logs
- Vulnerability data
- Host-level activity relevant to investigations

### 3. Administrative Change Detection

A new administrative user was created on the Windows client and successfully captured in the SIEM.

**Example event:**

- Windows Security Event ID `4728`

### 4. Power Outage / Availability Simulation

I simulated outages by shutting down switch interfaces and disconnecting endpoints. These events were captured by the SIEM and supported with custom detection logic.

### 5. Internal Reconnaissance Detection

I used the internal Kali system to scan the `192.168.1.0/24` range. Suricata inspected mirrored traffic and generated detection events.

**Example detections included:**

- `SURICATA ICMPv4 unknown code`
- `SURICATA SMB malformed request dialects`
- TCP handshake anomalies
- `ET SCAN Possible Nmap User-Agent Observed`

### 6. External Reconnaissance Detection

I repeated reconnaissance from the external Kali system to validate that attack traffic crossing the routed boundary could still be observed and surfaced in the SIEM.

### 7. SSH Brute-Force Detection Against Cisco Devices

I used Medusa to brute-force SSH logins against the router and both switches. Detection was confirmed through Cisco IOS syslog events visible in the SIEM.

**Examples of visible evidence:**

- Multiple `LOGIN_FAILED` events
- Successful login events after repeated attempts

### 8. Vulnerability Visibility

Wazuh’s vulnerability module identified software vulnerabilities on enrolled endpoints by correlating package and software inventory with known vulnerability sources.

## Key Challenges and How I Solved Them

### SPAN Port Misconfiguration

One of the biggest problems was that Suricata initially received no useful traffic. The issue turned out to be incorrect switch mirroring.

**What I learned:** even when a SIEM and IDS are installed correctly, visibility depends on the network path being correct.

### Suricata Ruleset Issues

I had trouble getting ET rules to download correctly. Because of this, some scans did not trigger all the signatures I expected.

**What I learned:** detection quality depends heavily on ruleset management and not just tool installation.

### Log Parsing and Custom Rules

Some events did not appear in the way I expected inside Wazuh, so I had to create custom rules to improve event recognition.

**What I learned:** documentation is useful, but real environments often require troubleshooting and adaptation.

### Asset Inventory Limitation

Wazuh does not treat Cisco routers and switches as regular agent-based assets in the same way it treats endpoints. I worked around this by relying on network telemetry and log evidence to demonstrate visibility of network devices.

## What I Learned

This project taught me much more than how to deploy a SIEM in a lab environment. At the start, it looked like a technical build focused on configuration tasks, connectivity, and alert generation. By the end, it became a practical lesson in how security monitoring really works: visibility has to be designed, validated, and constantly questioned.

One of the most important things I learned was that successful detection is not just about installing tools. It is easy to assume that if Wazuh, Suricata, and syslog forwarding are configured, then meaningful alerts will automatically appear. In practice, that was not always true. I had to verify whether traffic was actually reaching the monitoring point, whether the rules were loaded correctly, whether the logs were being parsed in the expected format, and whether the SIEM was turning raw data into something useful for investigation. This made me think less like someone completing a checklist and more like a SOC analyst trying to prove that telemetry is real, reliable, and actionable.

The project also showed me the importance of combining different layers of visibility. Endpoint logs alone do not tell the full story, and network alerts alone can lack context. By integrating Cisco syslog, Wazuh agents, and Suricata detections into one environment, I was able to see how infrastructure events, host activity, and network behaviour support each other during analysis. That gave me a much better understanding of how incidents can be investigated from multiple angles rather than relying on a single source of truth.

Another major lesson was the value of troubleshooting. Some of the most useful learning came from things not working as expected. Incorrect SPAN configuration meant Suricata initially saw no useful traffic. Ruleset issues reduced the number of expected detections. Some logs needed custom rule adjustments in Wazuh before they became meaningful alerts. These problems were frustrating at first, but they forced me to understand the environment at a deeper level. Instead of only following documentation, I had to interpret symptoms, isolate causes, and make practical fixes. That experience was one of the most realistic parts of the project because real security environments are rarely perfect.

From a technical point of view, I strengthened my skills in SIEM deployment, Cisco device configuration, syslog integration, agent onboarding, IDS visibility, port mirroring, and attack simulation using tools such as Nmap and Medusa. I also became more confident in reading alerts, understanding their source, and connecting them to specific attacker actions or infrastructure changes. Just as importantly, I learned how to explain what happened in a clear and structured way, which is a critical part of SOC and incident response work.

The project also reinforced that security operations is not only a technical discipline. Monitoring systems process data about users, devices, logins, network behaviour, and system changes. Even in a lab, that creates an awareness of privacy, responsible monitoring, access control, and professional accountability. Building the lab made me more conscious of the fact that defensive visibility must always be balanced with legal, ethical, and professional considerations.

Overall, this lab increased both my technical ability and my confidence. It helped me move beyond theory and into the kind of practical work that reflects real blue-team activity: building visibility, validating detections, troubleshooting gaps, and proving that security monitoring works when it matters.

## Final Reflection

This project started as a university assessment, but it became much more useful than just a coursework submission. It gave me practical hands-on experience with SIEM deployment, IDS integration, Cisco logging, endpoint monitoring, and attack simulation. More importantly, it taught me that detection engineering and SOC work are rarely about perfect step-by-step guides. They are about building visibility, testing assumptions, troubleshooting failures, and proving that alerts really work when something important happens.
