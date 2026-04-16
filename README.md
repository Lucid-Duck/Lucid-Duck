# Lucid Duck

I reverse engineer the systems vendors assume no one will look at: licensing-locked firmware, undocumented drivers, and proprietary bytecode formats that open-source tools can't even read. I patch whatever breaks along the way, trace bugs from user space through the kernel to the RF layer, and push the fixes upstream.

**First CVE:** [CVE-2026-20161](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-te-agentfilewrite-tqUw3SMU) -- Cisco ThousandEyes Enterprise Agent, published 2026-04-15.

Three more vendor-confirmed CVEs in the pipeline, plus the ones that will never see daylight thanks to NDAs. More advisories to follow as disclosure windows close.

_Stripped binaries, hardened targets, my goldmine._

**[Upstream Kernel Contributions](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca)** | Contact: **lucid_duck@justthetip.ca** or **devinwittmayer@gmail.com**

---

### Linux Driver & Kernel Work

Upstream contributions, debugging, and reverse engineering of Linux wireless and USB drivers.

**Upstream Patches**
- [`wifi: rtw89: usb: fix TX flow control by tracking in-flight URBs`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=80119a77e5b0) -- **Merged to mainline 2026-04-02** (commit `80119a77e5b0`). Acked-by + Signed-off-by: Ping-Ke Shih (Realtek rtw89 maintainer). Fixes a mac80211 TX flow control contract violation in the rtw89 USB driver. Development history: [tx-resources-flow-control](https://github.com/Lucid-Duck/tx-resources-flow-control).
- [`wifi: mt76: connac: use a helper to cache txpower_cur`](https://lore.kernel.org/linux-wireless/?q=txpower_cur) -- MediaTek engineer Sean Wang's v2 series on linux-wireless (2026-04-01). Carries `Reported-by`, `Tested-by`, `Co-developed-by`, and `Signed-off-by: Devin Wittmayer <lucid_duck@justthetip.ca>` on the lead patches. Fixes bogus 3 dBm txpower for all MT7921/MT7922/MT7925 devices. Awaiting Felix Fietkau merge. Development history: [mt7921-txpower-fix](https://github.com/Lucid-Duck/mt7921-txpower-fix).
- [Netgear A8500 VID-PID for mt7925u](https://lore.kernel.org/linux-wireless/?q=A8500) -- trivial ID-table addition submitted 2026-03-26, awaiting review.
- [mt76 RX bitrate reporting for MT7921/MT7922/MT7925](https://github.com/Lucid-Duck/mt76-rxrate) -- patch complete, soliciting community Tested-by before upstream submission.

**Driver Research**
- [rtw89 USB 2 to USB 3 switch-mode gap](https://github.com/Lucid-Duck/rtw89-usb3-gap) -- Empirical proof that mainline rtw89 is missing the USB 2 to USB 3 switch-mode code that lives in `morrownr/rtw89`, silently capping every Realtek WiFi 6/6E/7 USB adapter at USB 2.0 high-speed. Measured 258 Mbps stock to 802 Mbps with the out-of-tree driver on the same DWA-X1850 hardware (3.1x upload).
- [WiFi adapter pentest comparison](https://github.com/Lucid-Duck/wifi-pentest-comparisons) -- RTL8832AU vs MT7921U for wireless security assessments.

Focus: USB Wi-Fi driver debugging, cross-layer analysis (USB <-> kernel <-> RF), and reverse engineering undocumented hardware behaviour. Write-ups at [justthetip.ca](https://justthetip.ca).

---

### Reverse Engineering & Vulnerability Research

**March 2026**

*Major Telecom -- Nation-Wide eSIM Infrastructure Exposure + SIM Hijacking.* A carrier's production eSIM provisioning server -- the single system behind every eSIM activation on the network -- was exposed to the open internet with zero authentication and a full suite of management functions including profile download, deletion, and batch ops. No mutual TLS where the standard mandates it. Separately chained earlier APK research into a complete SIM port-in hijack executed end-to-end on production, auto-approved with no human review. Also bypassed the WAF with a single forged HTTP header.

*SSO Desktop Authenticator.* Decompiled the .NET assemblies from a widely-deployed identity provider's desktop authenticator and surfaced over a dozen distinct issues: unauthenticated command injection into a SYSTEM-level service, CORS origin reflection on a passwordless auth server, null-entropy encryption, and a race condition in the auto-updater yielding SYSTEM RCE.

*Feature Flag Platform -- Security Architecture Exfiltration.* Extracted a production SDK key from compiled bytecode and dumped hundreds of feature flags, employee emails, and developer device IDs -- a full map of which payment endpoints had fraud detection, which didn't, and multiple independent paths to bypass identity verification.

**February 2026**

*Major Telecom -- Proven Webmail Account Takeover + Infrastructure Audit.* Built a tool that cracked the one-time password in minutes and received a valid session token -- lockout hardcoded to zero, 2FA globally disabled, DOB validation non-functional. Any account vulnerable knowing nothing but the email address. Broader engagement also surfaced a zero-click stored XSS (novel sanitizer bypass exploiting DOM attribute enumeration order), dozens of production secrets extracted from the Android app's obfuscated native library, multiple unauthenticated eSIM management endpoints, and a host header bypass that defeated the corporate identity server's entire auth layer.

*Enterprise VPN -- Three Privilege Escalations From One Product.*
- *Windows TOCTOU to SYSTEM* -- Extracted a hardcoded 3DES key from the IPC protocol, forged service commands, then exploited a race between signature verification and execution using a filesystem oplock for deterministic timing. 15/15 SYSTEM. **CVE pending -- vendor PSIRT confirmed credit attribution.**
- *Linux IPC Command Injection to Root* -- Two messages to an unauthenticated Unix socket; shell metacharacters straight into `system()` as root. Unprivileged to root in under two seconds.
- *Linux Symlink Following to Root* -- Newline injection writes attacker-controlled content to any file as root. Chained to persistent system-wide RCE via `/etc/ld.so.preload`. **CVE pending; vendor-confirmed via sister submission in same disclosure batch.**

*Virtual Gateway Firmware -- Fleet-Wide Certificate Forgery.* Extracted a hardcoded CA private key identical across every deployment worldwide. Built a working MITM proxy that forges trusted certificates for any installation on earth. Also surfaced a production private TLS key deployed as the default web cert on every boot.

*Fintech Mobile App -- Deep Bytecode RE + CDN Bypass.* Patched an open-source decompiler to handle a proprietary bytecode version it couldn't, analysed the decompiled output, and extracted over a dozen distinct vulnerability classes across authentication, payments, identity verification, and fraud detection. Separately built a CDN bot-management bypass: rooted emulator, live memory dump at unreachable addresses, TLS-fingerprint-spoofed replay for full authenticated API access.

*Enterprise Endpoint Protection -- DNS Parser Stack Overflow.* A single crafted UDP packet triggers a stack overflow in a major vendor's network filter service on Windows. 100% reproducible persistent DoS across multiple crash dumps. **Vendor reproduced and confirmed fix. CVE and advisory pending.**

**January 2026**

*Enterprise VPN -- Reconstruction From Binaries Alone.* Licensing blocked normal operation, so I reverse engineered the whole system from compiled binaries -- no docs, no source. Rebuilt the XML profile schema by tracing code paths through disassembly, patched unrelated binary bugs just to reach the vulnerable paths, and surfaced: virtual gateway firmware with weak default credentials yielding SSH authentication bypass (Critical), and command injection in VPN client route handling where user-controlled XML traced through `snprintf()` directly into `system()` as root (Critical).

*Enterprise Linux EDR.* Reverse engineered a proprietary binary IPC protocol to discover quarantine bypass and cloud log injection. Malware survives detection indefinitely; audit logs poison-able with fabricated entries visible in the cloud admin console. High severity.

*Network Monitoring Agent (Cisco ThousandEyes Enterprise Agent).* Local privesc to root via symlink following + `ld.so.preload` injection. Persistent system-wide root from any unprivileged user. **Published as [CVE-2026-20161](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-te-agentfilewrite-tqUw3SMU) on 2026-04-15 (CWE-59, CVSS 5.5 Medium).**

*Network Camera.* Unauthenticated RCE via reverse-engineered binary event condition serialisation -- arbitrary command execution through user-controllable virtual inputs.

---

### What I Do

- Linux kernel and wireless driver debugging, upstream contributions, and repo maintenance
- Binary reverse engineering without source or documentation
- Mobile application RE (Android, React Native, JavaScript bytecode formats, native libraries)
- Vulnerability research in enterprise software (EDR, VPN, identity providers, telecom)
- Exploit development and proof-of-concept creation
- Protocol analysis and proprietary format reconstruction

---

### Looking For

Remote roles in Linux driver development, reverse engineering contracts, and vulnerability research.

**Contact:** devinwittmayer@gmail.com | Vancouver Island, BC, Canada | Available immediately
