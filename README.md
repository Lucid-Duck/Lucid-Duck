# Lucid Duck

Linux kernel debugging. Wireless security research. Finding bugs that weren't supposed to exist.

**[Upstream Kernel Contributions](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca)** | **devinwittmayer@gmail.com**

---

### Security Research (March 2026)

**eSIM Provisioning Server -- Zero Authentication on Nation-Wide Critical Infrastructure**
- Discovered that the production eSIM provisioning server for a major carrier -- the single system responsible for every eSIM activation on the entire network -- was accepting commands from anyone on the internet with zero authentication. Confirmed sixteen management functions including download SIM profile data, delete profile, enable/disable profile, and batch operations all returned successful responses. Industry specifications explicitly mandate mutual TLS authentication on this interface; there was none. Mapped seven hostnames on the same TLS certificate, including device-manufacturer-specific provisioning endpoints for major phone brands, all completely exposed. This is one of the most sensitive systems in telecom infrastructure, and it had no access control whatsoever.

**SIM Swap Attack -- Complete Chain Proven on Production**
- Built and executed a complete SIM port-in attack chain against a live carrier network using credentials extracted from earlier APK reverse engineering: triggered a one-time password to an arbitrary mobile number, brute-forced the 6-digit code with zero per-attempt rate limiting (3,866 consecutive wrong attempts in five minutes with no lockout or penalty), and completed the port authorization -- the server returned automatic approval with no human review. Any phone number on the network was vulnerable. Additionally discovered that the application's shared API quota could be exhausted with approximately 15,000 requests, causing a denial-of-service condition affecting all legitimate users of the mobile app.

**OAuth Login Flow Bypass -- Multi-Million-Dollar WAF Rendered Useless**
- Identified a critical flaw in a mobile app's login API serving millions of users: the two-step authentication flow protected Step 1 with an enterprise web application firewall, but the security token binding between steps was checked for presence only, not cryptographic validity -- any arbitrary string passed. Proved it with differential server error codes: one response when the token is absent (rejected before credential check), a completely different response when any fake value is supplied (credentials actually verified against the backend). A single forged HTTP header bypasses the WAF entirely, exposing the password endpoint to direct brute-force from the open internet.

**SSO Desktop Authenticator -- SYSTEM Service Exploitation + 13 Vulnerabilities**
- Decompiled 16 .NET assemblies (1,348 source files) from a widely-deployed identity provider's desktop authenticator and conducted a comprehensive security audit, uncovering 13 distinct vulnerabilities. Highlights: found unauthenticated named pipe injection granting any local user command execution in a SYSTEM-level service (I confirmed callback in under one second), identified CORS origin reflection on a local passwordless authentication server that would allow any website on the internet to hijack the authentication flow, proved data-protection encryption used null entropy rendering it purely decorative, and discovered a race condition in the auto-updater enabling arbitrary code execution as SYSTEM.

**Feature Flag Platform -- Complete Security Architecture Exfiltration**
- Extracted a production SDK key from compiled bytecode and dumped an entire feature flag management platform: 627 flags, 78 user segments, 654 employee email addresses, and 19 developer device IDs. This wasn't just a data leak -- it was a complete blueprint of the application's security posture. Systematically analyzed every flag to produce a prioritized attack roadmap: mapped exactly which payment endpoints had fraud detection and which were completely unprotected, identified three independent paths to bypass identity verification (with regulatory implications), confirmed 3D Secure was disabled for most regions, and extracted the precise conditions under which every security control could be overridden from the client side.

---

### Security Research (February 2026)

**Telecom Webmail -- Proven Account Takeover Affecting Millions of Users**
- Built a multi-threaded brute-force tool that cracked a 6-digit one-time password on a production webmail service (serving millions of subscribers) in 15 minutes -- 560,164 verification attempts at 610 requests/sec with zero rate limiting, zero account lockout, and zero failed-attempt penalties. Server-side date-of-birth validation was completely non-functional (any value accepted, or no value at all). An unauthenticated configuration endpoint independently confirmed lockout duration was hardcoded to zero and two-factor authentication was globally disabled across the platform. Valid session token received and verified, proving full authentication bypass. Any email address on the entire platform could be completely taken over knowing nothing but the address itself.

**Telecom Webmail -- Zero-Click Stored XSS to Email Account Takeover**
- Discovered two novel bypasses in a custom HTML sanitizer that a webmail provider deployed instead of an established security library, affecting the same millions of users. The zero-click chain exploits DOM attribute enumeration order: an `<iframe srcdoc>` with an attacker-controlled `sandbox` attribute survives sanitization because `setAttribute` processes the attacker's value last, overriding the safe default. JavaScript executes the instant the victim opens the email -- zero clicks, zero interaction. Combined with wildcard CORS headers and platform-wide disabled two-factor authentication, a single carefully crafted email achieves complete, silent email account takeover.

**Enterprise VPN -- Three Independent Privilege Escalations from One Product**
- Reverse engineered the same enterprise VPN product family (deployed across thousands of organizations) to find three distinct privilege escalation chains, each a different vulnerability class with a different exploitation technique:
  - *Windows TOCTOU to SYSTEM:* Extracted a hardcoded 3DES encryption key from the IPC protocol via static binary analysis, forged authenticated service commands, then exploited a time-of-check-time-of-use race between signature verification and process creation using a filesystem oplock for deterministic timing. 15 out of 15 test runs achieved SYSTEM. Full working proof-of-concept delivered.
  - *Linux IPC Command Injection to Root:* Two messages to an unauthenticated Unix domain socket -- the first sets a path containing shell metacharacters, the second concatenates it directly into `system()` as root. Any unprivileged user to full root in under two seconds. Stock unmodified binary, zero prerequisites.
  - *Linux Symlink Following to Root:* File open without `O_NOFOLLOW` combined with zero output escaping. Newline injection writes attacker-controlled content to any file on the system as root. Chained to persistent root code execution via `/etc/ld.so.preload` injection -- the dynamic linker silently ignores invalid XML tag lines and loads the injected shared library on every subsequent process execution system-wide.

**Mobile App Reverse Engineering -- 27 Production Secrets from a Single APK**
- Fully decompiled a major mobile application (34,678 Java classes) protected by commercial DRM that defeats most automated analysis. A native library contained every production secret behind a 64-byte XOR S-box -- trivially reversible. Extracted 27 credentials spanning 13 environments (production, staging, UAT, SIT, and more) and chained them into increasingly severe exploits: direct bearer token generation with 24-hour lifetimes, a login flow with zero rate limiting (50 consecutive attempts, no lockout), real phone number allocation from the live provisioning system, payment API tokens via a cloud identity provider, and SIM authentication sessions where the app's proprietary RC4+MD5 encryption scheme was fully reverse engineered, replicated, and accepted by the production subscriber database.

**Virtual Gateway Firmware -- Fleet-Wide Certificate Forgery**
- Extracted a hardcoded CA private key from an enterprise virtual gateway firmware image -- generated once in 2016, baked into a read-only initramfs, identical across every deployment worldwide. Built a working man-in-the-middle proxy that forges trusted certificates for any installation on earth, proving every organization running this product is vulnerable. Also found a production domain's private TLS key deployed as the default web server certificate on every boot. Delivered the complete evidence package: extracted keys, forged certificates, a working MITM proxy, and a decrypted TLS session capture showing intercepted credentials in plaintext.

**Fintech Mobile App -- Deep Binary Reverse Engineering + CDN Bypass Pipeline**
- Reverse engineered a React Native financial application compiled to Hermes bytecode -- a binary format that stops most security researchers cold. Patched an open-source decompiler to support a bytecode version it couldn't handle, then systematically analyzed 127MB of decompiled output to extract 14 distinct vulnerability classes spanning authentication, payments, identity verification, and fraud detection. Built a separate multi-stage CDN bot-management bypass pipeline: rooted Android emulator with DRM protections intact, dumped live process memory at 48-bit heap addresses that standard Linux tools physically cannot reach, extracted active authentication tokens, and replayed them through a TLS-fingerprint-spoofing proxy for full authenticated API access to every endpoint.

**eSIM Infrastructure -- Unauthenticated Production API with Subscriber Enumeration**
- Found five eSIM management endpoints on a major carrier's production API gateway that accepted commands with zero authentication -- no token, no API key, no credentials of any kind. Discovered a differential response oracle that reveals whether any given phone number belongs to an active subscriber, then used it to enumerate 36,000 numbers across 13 mobile prefixes, confirming 414 active subscribers with hit rates consistent with real-world density patterns. Zero rate limiting at sustained throughput -- demonstrated that a single IP could enumerate every active subscriber in a million-number prefix in under four days.

**Corporate Identity Infrastructure -- Host Header Authentication Bypass**
- Discovered that a corporate federation server's reverse proxy authentication could be completely bypassed with the correct `Host` header, granting unauthenticated access to the full identity backend. Leveraged this to find a 75x timing oracle for Active Directory username enumeration (valid users responded in 37-72ms, invalid users in ~3,000ms -- unmistakable signal), extracted internal domain architecture via NTLM challenge metadata disclosure, and confirmed unlimited credential spray capability against SOAP-based authentication endpoints. Identified six real employee accounts via timing analysis alone.

---

### Security Research (January 2026)

**Enterprise Endpoint Protection**
- Reverse engineered proprietary binary IPC protocol to discover quarantine bypass and cloud log injection vulnerabilities in a major security vendor's Linux EDR product. Malware can survive detection indefinitely; audit logs can be poisoned with fabricated paths visible in the cloud admin console. CVSS 7.1-7.3 (High).

**Network Monitoring Appliance**
- Discovered local privilege escalation to root RCE in an enterprise network monitoring agent via symlink following + ld.so.preload injection. Any local user achieves persistent root access affecting all process execution system-wide. CVSS 8.8-9.3 (Critical).

**Enterprise VPN Infrastructure**
- Vendor licensing restrictions blocked normal operation, so I reverse engineered the entire system from compiled binaries alone--no documentation, no references, no source code. Reconstructed the complete XML profile schema from scratch by tracing code paths through disassembly. Fixed unrelated bugs in the binary just to reach the vulnerable code paths. This pure black-box analysis revealed:
  - Virtual gateway firmware with empty root password and single-character hardcoded credentials. Achieved root shell via GRUB modification; SSH authentication bypass proven. CVSS 9.8 (Critical).
  - Command injection in VPN client route handling--traced user-controlled XML data through snprintf() directly to system() as root via static analysis. CVSS 9.0 (Critical).

**IoT/Embedded Systems**
- Found unauthenticated D-Bus RCE on network camera firmware. Reverse engineered binary event condition serialization format to trigger arbitrary command execution via user-controllable virtual inputs. Achieved privilege escalation granting hardware GPIO, storage, and messaging access.

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

- Vulnerability research in enterprise security products (EDR, VPN, network monitoring, identity providers)
- Binary reverse engineering without source code or documentation
- Mobile application reverse engineering (Android APK, React Native, Hermes bytecode, native libraries)
- Protocol analysis and proprietary format decoding
- Telecom infrastructure security (eSIM, SIM provisioning, OTP systems)
- Root cause analysis in kernel subsystems (mac80211, USB, wireless drivers)
- Exploit development and proof-of-concept creation
- Technical writing that gets bugs fixed

---

### Looking For

Remote security research, vulnerability research, or driver development roles.

**Contact:** devinwittmayer@gmail.com | Vancouver Island, BC | Available immediately
