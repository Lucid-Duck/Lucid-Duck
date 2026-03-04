# Lucid Duck

Linux kernel debugging. Wireless security research. Finding bugs that weren't supposed to exist.

**[Upstream Kernel Contributions](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca)** | **devinwittmayer@gmail.com**

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
- Unauthenticated D-Bus RCE on network camera firmware. Reverse engineered binary event condition serialization format to trigger arbitrary command execution via user-controllable virtual inputs. Privilege escalation grants hardware GPIO, storage, and messaging access.

---

### Security Research (February 2026)

**Telecom Webmail -- Proven Account Takeover**
- Built a multi-threaded brute-force tool that cracked a 6-digit one-time password on a production webmail service in 15 minutes -- 560,164 verification attempts at 610 requests/sec with zero rate limiting, zero lockout, and zero failed-attempt penalties. Server-side date-of-birth validation was completely non-functional. An unauthenticated configuration endpoint independently confirmed lockout duration was set to zero and two-factor authentication was globally disabled. Valid session token received, proving full authentication bypass. Any email address on the platform could be taken over knowing nothing but the address itself.

**Telecom Webmail -- Zero-Click Stored XSS to Email Takeover**
- Discovered two novel bypasses in a custom HTML sanitizer deployed instead of an established library. The zero-click chain exploits DOM attribute enumeration order: an `<iframe srcdoc>` with an attacker-controlled `sandbox` attribute survives sanitization because `setAttribute` processes the attacker's value last, overriding the safe default. JavaScript executes the instant the email is opened -- no clicks required. Combined with wildcard CORS and disabled two-factor authentication, a single malicious email achieves complete email account takeover.

**Enterprise VPN -- Three Independent Privilege Escalations from One Product**
- Reverse engineered the same VPN product family to find three distinct privilege escalation chains, each a different vulnerability class:
  - *Windows TOCTOU to SYSTEM:* Extracted a hardcoded 3DES encryption key from the IPC protocol via static analysis, forged service commands, then exploited a time-of-check-time-of-use race between signature verification and process creation using a filesystem oplock for deterministic timing. 15 out of 15 test runs successful. Full working proof-of-concept delivered.
  - *Linux IPC Command Injection to Root:* Two messages to an unauthenticated Unix domain socket -- the first sets a path containing shell metacharacters, the second concatenates it into `system()` as root. Unprivileged user to root in under two seconds, stock binary, zero prerequisites.
  - *Linux Symlink Following to Root:* File open without `O_NOFOLLOW` combined with zero output escaping. Newline injection writes attacker-controlled content to any file as root. Chained to persistent root code execution via `/etc/ld.so.preload` -- the dynamic linker silently ignores invalid XML lines and loads injected shared libraries.

**Mobile App Reverse Engineering -- 27 Production Secrets from a Single APK**
- Fully decompiled a major mobile application (34,678 Java classes) protected by commercial DRM. A native library contained all production secrets behind a 64-byte XOR S-box -- trivially reversible. Extracted 27 credentials spanning 13 environments and chained them into: direct bearer token generation, a login flow with zero rate limiting, real phone number allocation from the provisioning system, payment API tokens via a cloud identity provider, and SIM authentication sessions where the app's proprietary RC4+MD5 encryption was fully replicated and accepted by the production backend.

**Virtual Gateway Firmware -- Fleet-Wide Certificate Forgery**
- Firmware image ships with a hardcoded CA private key generated in 2016, baked into a read-only initramfs, identical across every deployment worldwide. Built a working man-in-the-middle proxy that forges certificates trusted by every installation on earth. Also discovered a production domain's private TLS key deployed as the default web server certificate on every boot. Delivered extracted keys, forged certificates, working MITM proxy, and a decrypted TLS session capture with visible credentials.

**Fintech Mobile App -- Hermes Bytecode Reverse Engineering + CDN Bypass**
- Reverse engineered a React Native application compiled to Hermes bytecode -- a binary format most security researchers can't read. Patched an open-source decompiler to support a bytecode version it didn't handle, then analyzed 127MB of decompiled output to extract 14 distinct vulnerability classes across authentication, payments, identity verification, and fraud detection. Built a separate CDN bot-management bypass pipeline: rooted emulator with DRM intact, dumped process memory at 48-bit heap addresses that standard tools can't reach, extracted live tokens, and replayed them through a TLS-fingerprint-spoofing proxy for full authenticated API access.

**eSIM Infrastructure -- Unauthenticated Production Endpoints**
- Five eSIM management endpoints on a production telecom API gateway accepted commands with zero authentication. Discovered a differential response oracle that reveals active subscriber phone numbers. Enumerated 36,000 numbers across 13 mobile prefixes, confirming 414 active subscribers with hit rates consistent with real density patterns. Zero rate limiting -- a single IP could enumerate every active number in a million-number prefix in under four days.

**Corporate Identity Infrastructure -- Host Header Authentication Bypass**
- A reverse proxy enforced credential checks on all requests to a corporate federation server. Sending the correct `Host` header completely bypassed authentication, exposing the full backend. Through this bypass: discovered a 75x timing oracle for directory username enumeration (valid users responded in 37-72ms, invalid users in ~3,000ms), extracted internal domain metadata via NTLM challenge disclosure, and confirmed unlimited credential spray capability via SOAP-based authentication endpoints.

---

### Security Research (March 2026)

**eSIM Provisioning Server -- Zero Authentication on Critical Infrastructure**
- The production eSIM provisioning server -- the system handling every eSIM activation on a carrier's network -- was accepting commands from anyone on the internet with zero authentication. Sixteen management functions including download SIM profile data, delete profile, enable/disable profile, and batch operations all processed successfully. Industry specifications explicitly mandate mutual TLS on this interface; there was none. Seven hostnames on the same certificate, including device-manufacturer-specific endpoints, were all equally exposed.

**SIM Swap Chain -- Proven End-to-End**
- Demonstrated a complete SIM port-in attack using credentials extracted from the earlier APK reverse engineering work: trigger a one-time password to any mobile number on the network, brute-force the 6-digit code with zero per-attempt rate limiting (3,866 consecutive attempts in five minutes, no lockout), and complete the port authorization. The server returned automatic approval with no human review. Also discovered that the application's shared API quota could be exhausted with approximately 15,000 requests, causing service disruption for all legitimate users.

**OAuth Login Flow Bypass -- Web Application Firewall Rendered Useless**
- A mobile app login API used a two-step flow where Step 1 was protected by a web application firewall. The security token binding between steps was checked for presence only, not validity -- any arbitrary string passed. Proven with differential server error codes: one response when the token is absent (rejected before credential check), a different response with any fake value (credentials actually verified against the backend). The entire WAF investment was defeated by a single forged HTTP header.

**SSO Desktop Authenticator -- SYSTEM Service Exploitation + 13 Vulnerabilities**
- Decompiled 16 .NET assemblies (1,348 source files) from a major identity provider's desktop authenticator. Identified 13 distinct vulnerabilities including: unauthenticated named pipe injection into a SYSTEM-level service (confirmed callback in under one second), CORS origin reflection on a local passwordless authentication server enabling potential remote authentication bypass from any website, data-protection encryption with null entropy rendering it decorative, and a race condition in the auto-updater's installer execution path.

**Feature Flag Platform -- Full Security Architecture Exfiltration**
- Extracted a production SDK key from compiled bytecode and dumped an entire feature flag management platform: 627 flags, 78 user segments, 654 employee email addresses, and 19 developer device IDs. Systematically analyzed every flag to produce a complete attack roadmap: mapped which payment endpoints had fraud detection coverage and which didn't, identified three independent paths to bypass identity verification, confirmed 3D Secure was disabled for most regions, and extracted the exact conditions under which security controls could be overridden client-side.

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
