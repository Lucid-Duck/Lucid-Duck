# Lucid Duck

Linux kernel debugging. Wireless security research. Finding bugs that weren't supposed to exist.

**[Upstream Kernel Contributions](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca)**

---

### Security Research (January 2026)

**Enterprise Endpoint Protection**
- Reverse engineered proprietary binary IPC protocol to discover quarantine bypass and cloud log injection vulnerabilities in a major security vendor's Linux EDR product. Malware can survive detection indefinitely; audit logs can be poisoned with fabricated paths visible in the cloud admin console. CVSS 7.1-7.3 (High).

**Network Monitoring Appliance**
- Discovered local privilege escalation to root RCE in an enterprise network monitoring agent via symlink following + ld.so.preload injection. Any local user achieves persistent root access affecting all process execution system-wide. CVSS 8.8-9.3 (Critical).

**Enterprise VPN Infrastructure**
- Binary analysis of virtual gateway firmware revealed empty root password, hardcoded single-character credentials, and permissive PAM configuration. Achieved root shell access; SSH authentication bypass proven. CVSS 9.8 (Critical).
- Command injection in enterprise VPN client's route handling—user-controlled XML data flows through snprintf() directly to system() as root. Full code path traced through static analysis from profile parsing to code execution. CVSS 9.0 (Critical).

**IoT/Embedded Systems**
- Unauthenticated D-Bus RCE on network camera firmware. Reverse engineered binary event condition serialization format to trigger arbitrary command execution via user-controllable virtual inputs. Privilege escalation grants hardware GPIO, storage, and messaging access.

---

### Kernel Driver Work

**Upstream Patches**
- [rtw89 USB TX flow control fix](https://github.com/morrownr/rtw89/pull/52) — Fixed mac80211 contract violation causing packet loss under load
- [mt7921u TX power reporting](https://github.com/Lucid-Duck/mt7921u-debugging) — Traced INT_MIN bug through mac80211 subsystem, patches submitted upstream

**Security Research**
- [WiFi adapter pentest comparison](https://github.com/Lucid-Duck/wifi-pentest-comparisons) — RTL8832AU vs MT7921U for wireless security assessments

**Blog**
- [justthetip.ca](https://justthetip.ca) — Technical write-ups on driver debugging and security research

---

### What I Do

- Vulnerability research in enterprise security products (EDR, VPN, network monitoring)
- Binary reverse engineering without source code or documentation
- Protocol analysis and proprietary format decoding
- Root cause analysis in kernel subsystems (mac80211, USB, wireless drivers)
- Exploit development and proof-of-concept creation
- Technical writing that gets bugs fixed

---

### Looking For

Remote security research, vulnerability research, or driver development roles.

---

### Contact

- **Email:** lucid_duck@justthetip.ca
- **Location:** Vancouver Island, BC
- **Availability:** Remote work, flexible hours
