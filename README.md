# Lucid Duck

Security researcher and ethical hacker. Stripped binaries, hardened targets, my goldmine.

**[Upstream Kernel Contributions](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca)** | **devinwittmayer@gmail.com**

---

### Security Research (March 2026)

**Major Telecom -- Nation-Wide eSIM Infrastructure Exposed + SIM Hijacking**
- Discovered that a carrier's production eSIM provisioning server -- the single system responsible for every eSIM activation on the network -- had zero authentication, with 16 management functions exposed to the open internet including downloading SIM profiles, deleting profiles, and batch operations. Industry standards mandate mutual TLS on this interface; there was none. Separately proved that any phone number on the network could be stolen via SIM port-in by chaining earlier APK research into a complete attack chain executed end-to-end on production -- the server approved the hijack automatically with no human review. Also found the carrier's WAF-protected login flow could be completely bypassed with a single forged HTTP header, rendering the entire firewall investment useless.

**SSO Desktop Authenticator -- SYSTEM Service Exploitation + 13 Vulnerabilities**
- Decompiled 16 .NET assemblies from a widely-deployed identity provider's desktop authenticator and uncovered 13 distinct vulnerabilities. Found unauthenticated command injection into a SYSTEM-level service from any local user, CORS origin reflection on a passwordless auth server that would let any website hijack the authentication flow, encryption with null entropy rendering it decorative, and a race condition in the auto-updater enabling arbitrary code execution as SYSTEM.

**Feature Flag Platform -- Complete Security Architecture Exfiltration**
- Extracted a production SDK key from compiled bytecode and dumped an entire feature flag platform: 627 flags, 654 employee emails, and 19 developer device IDs. This wasn't just a data leak -- it was a complete blueprint of the application's security posture. Mapped which payment endpoints had fraud detection and which were wide open, found three independent paths to bypass identity verification, confirmed 3D Secure was disabled for most regions, and extracted the exact conditions under which every security control could be client-side overridden.

---

### Security Research (February 2026)

**Major Telecom -- Proven Email Account Takeover + Full-Scope Infrastructure Audit**
- Proved complete email account takeover on a production webmail platform serving millions of subscribers -- built a tool that cracked the one-time password in 15 minutes, received a valid session token, and demonstrated that any account was vulnerable knowing nothing but the email address. Lockout was hardcoded to zero, two-factor authentication was globally disabled, and date-of-birth validation was non-functional. This was just the starting point for a broader engagement that uncovered: a zero-click stored XSS achieving the same account takeover from a single malicious email (novel sanitizer bypass exploiting DOM attribute enumeration order), 27 production secrets extracted from their Android app's obfuscated native library including credentials that authenticated against the live subscriber database, five unauthenticated eSIM management endpoints exposing active subscriber data on the production API, and a host header bypass that defeated the corporate identity server's entire authentication layer.

**Enterprise Endpoint Protection -- DNS Parser Stack Overflow**
- Discovered a stack overflow in a major endpoint security vendor's network filter service triggered by a single crafted UDP packet. 100% reproducible persistent denial of service on Windows -- confirmed across 13 crash dumps. Vendor reproduced the bug and confirmed a fix. CVE and security advisory pending.

**Enterprise VPN -- Three Independent Privilege Escalations from One Product**
- Reverse engineered an enterprise VPN product deployed across thousands of organizations and found three distinct privilege escalation chains:
  - *Windows TOCTOU to SYSTEM:* Extracted a hardcoded 3DES encryption key from the IPC protocol, forged service commands, then exploited a race condition between signature verification and process execution using a filesystem oplock for deterministic timing. 15/15 test runs achieved SYSTEM.
  - *Linux IPC Command Injection to Root:* Two messages to an unauthenticated Unix socket -- shell metacharacters concatenated directly into `system()` as root. Any unprivileged user to full root in under two seconds.
  - *Linux Symlink Following to Root:* Newline injection writes attacker-controlled content to any file as root. Chained to persistent root code execution via `/etc/ld.so.preload` -- the injected shared library loads on every subsequent process execution system-wide.

**Virtual Gateway Firmware -- Fleet-Wide Certificate Forgery**
- Extracted a hardcoded CA private key from enterprise gateway firmware -- generated once in 2016, identical across every deployment worldwide. Built a working man-in-the-middle proxy that forges trusted certificates for any installation on earth. Also found a production domain's private TLS key deployed as the default web server certificate on every boot. Delivered extracted keys, forged certificates, working MITM proxy, and a decrypted TLS capture showing intercepted credentials in plaintext.

**Fintech Mobile App -- Deep Binary Reverse Engineering + CDN Bypass Pipeline**
- Reverse engineered a financial application compiled to Hermes bytecode -- a binary format that stops most security researchers cold. Patched an open-source decompiler to support a version it couldn't handle, then analyzed 127MB of decompiled output to extract 14 distinct vulnerability classes across authentication, payments, identity verification, and fraud detection. Separately built a CDN bot-management bypass pipeline: rooted emulator, live memory dump at addresses standard tools can't reach, token extraction, and TLS-fingerprint-spoofed replay for full authenticated API access.

---

### Security Research (January 2026)

**Enterprise Endpoint Protection**
- Reverse engineered a proprietary binary IPC protocol to discover quarantine bypass and cloud log injection in a major security vendor's Linux EDR. Malware can survive detection indefinitely; audit logs can be poisoned with fabricated entries visible in the cloud admin console. CVSS 7.1-7.3 (High). CVE pending.

**Network Monitoring Appliance**
- Discovered local privilege escalation to root in an enterprise network monitoring agent via symlink following + ld.so.preload injection. Any local user achieves persistent root access affecting all process execution system-wide. CVSS 8.8-9.3 (Critical). Vendor-confirmed fix; CVE and security advisory pending.

**Enterprise VPN Infrastructure**
- Vendor licensing restrictions blocked normal operation, so I reverse engineered the entire system from compiled binaries alone -- no documentation, no references, no source code. Reconstructed the complete XML profile schema by tracing code paths through disassembly. Fixed unrelated bugs in the binary just to reach the vulnerable code paths. This pure black-box analysis revealed:
  - Virtual gateway firmware with empty root password and single-character hardcoded credentials. Achieved root shell; SSH authentication bypass proven. CVSS 9.8 (Critical).
  - Command injection in VPN client route handling -- traced user-controlled XML data through snprintf() directly to system() as root. CVSS 9.0 (Critical).

**IoT/Embedded Systems**
- Found unauthenticated remote code execution on network camera firmware. Reverse engineered binary event condition serialization to trigger arbitrary command execution via user-controllable virtual inputs, achieving privilege escalation to hardware GPIO, storage, and messaging access.

---

### Kernel Driver Work

**Upstream Patches**
- [rtw89 USB TX flow control fix](https://github.com/morrownr/rtw89/pull/52) -- Fixed mac80211 contract violation causing packet loss under load
- [mt7921u TX power reporting](https://github.com/Lucid-Duck/mt7921u-debugging) -- Traced INT_MIN bug through mac80211 subsystem, patches submitted upstream

**Security Research**
- [WiFi adapter pentest comparison](https://github.com/Lucid-Duck/wifi-pentest-comparisons) -- RTL8832AU vs MT7921U for wireless security assessments

**Blog**
- [justthetip.ca](https://justthetip.ca) -- Technical write-ups on driver debugging and security research

---

### What I Do

- Vulnerability research in enterprise software (EDR, VPN, identity providers, telecom infrastructure)
- Binary reverse engineering without source code or documentation
- Mobile application reverse engineering (Android, React Native, Hermes bytecode, native libraries)
- Telecom security (eSIM provisioning, SIM authentication, OTP systems)
- Exploit development and proof-of-concept creation
- Protocol analysis and proprietary format decoding

---

### Looking For

Remote security research, vulnerability research, or offensive security roles.

**Contact:** devinwittmayer@gmail.com | Vancouver Island, BC | Available immediately
