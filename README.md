# Lucid Duck

Security researcher and ethical hacker. Finding bugs that weren't supposed to exist.

**[Upstream Kernel Contributions](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca)** | **devinwittmayer@gmail.com**

---

### Security Research (March 2026)

**eSIM Provisioning Server -- Zero Authentication on Nation-Wide Critical Infrastructure**
- Discovered that the production eSIM provisioning server for a major carrier -- the single system responsible for every eSIM activation on the entire network -- was accepting commands from anyone on the internet with zero authentication. Sixteen management functions including downloading SIM profiles, deleting profiles, and batch operations were all completely exposed across seven hostnames. Industry specifications explicitly mandate mutual TLS on this interface; there was none. One of the most sensitive systems in telecom infrastructure, wide open.

**SIM Swap Attack -- Complete Chain Proven on Production**
- Proved that any phone number on a major carrier's network could be stolen via SIM port-in by chaining credentials extracted from earlier APK reverse engineering with a brute-forceable one-time password that had no rate limiting or lockout. Built the full attack chain end-to-end on a live production system -- the server approved the port automatically with no human review. Millions of subscribers were at risk.

**OAuth Login Flow Bypass -- Multi-Million-Dollar WAF Rendered Useless**
- Identified a critical flaw in a mobile app's login API serving millions of users: the enterprise web application firewall protecting the login flow was completely bypassable with a single forged HTTP header. The security token between authentication steps was checked for presence only, not validity -- any arbitrary string worked. Proved it with differential server responses that show credentials being checked against the backend. The entire WAF investment was worthless.

**SSO Desktop Authenticator -- SYSTEM Service Exploitation + 13 Vulnerabilities**
- Decompiled 16 .NET assemblies from a widely-deployed identity provider's desktop authenticator and uncovered 13 distinct vulnerabilities. Found unauthenticated command injection into a SYSTEM-level service from any local user, CORS origin reflection on a passwordless auth server that would let any website hijack the authentication flow, encryption with null entropy rendering it decorative, and a race condition in the auto-updater enabling arbitrary code execution as SYSTEM.

**Feature Flag Platform -- Complete Security Architecture Exfiltration**
- Extracted a production SDK key from compiled bytecode and dumped an entire feature flag platform: 627 flags, 654 employee emails, and 19 developer device IDs. This wasn't just a data leak -- it was a complete blueprint of the application's security posture. Mapped which payment endpoints had fraud detection and which were wide open, found three independent paths to bypass identity verification, confirmed 3D Secure was disabled for most regions, and extracted the exact conditions under which every security control could be client-side overridden.

---

### Security Research (February 2026)

**Telecom Webmail -- Proven Account Takeover Affecting Millions of Users**
- Proved that any email account on a production webmail platform serving millions of subscribers could be completely taken over knowing nothing but the email address. Built a tool that cracked the one-time password in 15 minutes with no rate limiting, no lockout, and no penalties. Server-side date-of-birth validation was non-functional. An unauthenticated configuration endpoint confirmed lockout was hardcoded to zero and two-factor authentication was globally disabled. Received a valid session token proving full authentication bypass.

**Telecom Webmail -- Zero-Click Stored XSS to Email Account Takeover**
- Discovered two novel bypasses in a custom HTML sanitizer affecting the same millions of users. The zero-click chain exploits DOM attribute enumeration order so that an attacker-controlled `sandbox` attribute overrides the sanitizer's safe default -- JavaScript executes the instant the victim opens the email with zero interaction. Combined with wildcard CORS and disabled two-factor auth, a single crafted email silently takes over the entire account.

**Enterprise VPN -- Three Independent Privilege Escalations from One Product**
- Reverse engineered an enterprise VPN product deployed across thousands of organizations and found three distinct privilege escalation chains:
  - *Windows TOCTOU to SYSTEM:* Extracted a hardcoded 3DES encryption key from the IPC protocol, forged service commands, then exploited a race condition between signature verification and process execution using a filesystem oplock for deterministic timing. 15/15 test runs achieved SYSTEM.
  - *Linux IPC Command Injection to Root:* Two messages to an unauthenticated Unix socket -- shell metacharacters concatenated directly into `system()` as root. Any unprivileged user to full root in under two seconds.
  - *Linux Symlink Following to Root:* Newline injection writes attacker-controlled content to any file as root. Chained to persistent root code execution via `/etc/ld.so.preload` -- the injected shared library loads on every subsequent process execution system-wide.

**Mobile App Reverse Engineering -- 27 Production Secrets from a Single APK**
- Fully decompiled a major mobile application protected by commercial DRM and found every production secret hidden behind a trivially reversible XOR S-box. Extracted 27 credentials spanning 13 environments and chained them into increasingly severe exploits: bearer token generation, a login flow with no rate limiting, real phone number allocation from the live provisioning system, payment API tokens, and SIM authentication sessions where the app's proprietary RC4+MD5 encryption was fully replicated and accepted by the production subscriber database.

**Virtual Gateway Firmware -- Fleet-Wide Certificate Forgery**
- Extracted a hardcoded CA private key from enterprise gateway firmware -- generated once in 2016, identical across every deployment worldwide. Built a working man-in-the-middle proxy that forges trusted certificates for any installation on earth. Also found a production domain's private TLS key deployed as the default web server certificate on every boot. Delivered extracted keys, forged certificates, working MITM proxy, and a decrypted TLS capture showing intercepted credentials in plaintext.

**Fintech Mobile App -- Deep Binary Reverse Engineering + CDN Bypass Pipeline**
- Reverse engineered a financial application compiled to Hermes bytecode -- a binary format that stops most security researchers cold. Patched an open-source decompiler to support a version it couldn't handle, then analyzed 127MB of decompiled output to extract 14 distinct vulnerability classes across authentication, payments, identity verification, and fraud detection. Separately built a CDN bot-management bypass pipeline: rooted emulator, live memory dump at addresses standard tools can't reach, token extraction, and TLS-fingerprint-spoofed replay for full authenticated API access.

**eSIM Infrastructure -- Unauthenticated Production API with Subscriber Enumeration**
- Found five eSIM management endpoints on a major carrier's production gateway that accepted commands with zero authentication. Discovered a response oracle that reveals active subscriber phone numbers, then enumerated tens of thousands of numbers and confirmed hundreds of active subscribers. Demonstrated that a single machine could map every active subscriber in a million-number prefix in under four days.

**Corporate Identity Infrastructure -- Host Header Authentication Bypass**
- Discovered that a corporate federation server's entire authentication layer could be bypassed with a single HTTP header, exposing the full identity backend. Leveraged this to find a 75x timing oracle for employee username enumeration, extracted internal domain architecture via NTLM metadata, and confirmed unlimited credential spray capability. Identified six real employee accounts through timing analysis alone.

---

### Security Research (January 2026)

**Enterprise Endpoint Protection**
- Reverse engineered a proprietary binary IPC protocol to discover quarantine bypass and cloud log injection in a major security vendor's Linux EDR. Malware can survive detection indefinitely; audit logs can be poisoned with fabricated entries visible in the cloud admin console. CVSS 7.1-7.3 (High).

**Network Monitoring Appliance**
- Discovered local privilege escalation to root in an enterprise network monitoring agent via symlink following + ld.so.preload injection. Any local user achieves persistent root access affecting all process execution system-wide. CVSS 8.8-9.3 (Critical).

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
