# Lucid Duck

Reverse engineering on systems where there is no source and the documentation is wrong or absent. Linux kernel and driver work, embedded firmware RE, and vulnerability research, in parallel since January.

- **Mainline kernel:** [`wifi: rtw89: usb: fix TX flow control by tracking in-flight URBs`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=80119a77e5b0) -- merged 2026-04-02 (`80119a77e5b0`). Acked-by + Signed-off-by Ping-Ke Shih (Realtek rtw89 maintainer). The bug: mac80211's TX flow contract requires drivers to wake stopped queues on completion; rtw89 USB tracked completions with a count that desynced under load, queues stayed asleep, throughput collapsed. Fix tracks in-flight URBs as a set. Notes: [tx-resources-flow-control](https://github.com/Lucid-Duck/tx-resources-flow-control).
- **First CVE:** [CVE-2026-20161](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-te-agentfilewrite-tqUw3SMU) -- Cisco ThousandEyes Enterprise Agent, 2026-04-15. Symlink-following + `ld.so.preload` injection on the agent's log path; persistent system-wide root from any unprivileged user.

**Contact:** lucid_duck@justthetip.ca | devinwittmayer@gmail.com | Vancouver Island, BC, Canada | [justthetip.ca](https://justthetip.ca)

---

### Linux kernel and driver work

- **Merged to mainline (2026-04-02):** rtw89 USB TX flow control fix, see above.
- **In flight on linux-wireless:** Co-developed-by + Tested-by + Reported-by + Signed-off-by on Sean Wang's [`mt76: connac: use a helper to cache txpower_cur`](https://lore.kernel.org/linux-wireless/?q=txpower_cur) v2 series (2026-04-01). Awaiting Felix Fietkau merge. The bug: bogus 3 dBm TX power on every MT7921/7922/7925 device because the cached value was being clobbered between scans. Notes: [mt7921-txpower-fix](https://github.com/Lucid-Duck/mt7921-txpower-fix).
- **Ready for community Tested-by:** [mt76 RX bitrate reporting](https://github.com/Lucid-Duck/mt76-rxrate) for MT7921/7922/7925.
- **Submitted, awaiting review:** [Netgear A8500 VID-PID for mt7925u](https://lore.kernel.org/linux-wireless/?q=A8500), 2026-03-26.
- **Open research, patch path identified:** [rtw89 USB 2 to USB 3 switch-mode gap](https://github.com/Lucid-Duck/rtw89-usb3-gap). Mainline rtw89 silently caps Realtek WiFi 6/6E/7 USB adapters at high-speed because the USB 2 to USB 3 switch-mode code that lives in `morrownr/rtw89` was never upstreamed. 258 Mbps measured stock, 802 Mbps with the out-of-tree driver, same DWA-X1850 hardware.

---

### Embedded firmware RE -- active contract

**April 2026.** Automotive keyless-entry firmware reverse engineering for a law-enforcement security vendor. Nine firmware images, five MCU families: STM8, ARM Cortex-M0, PIC mid-range, HCS12 / HCS12X, V850. Per-image deliverable was a byte-exact C port of the firmware's cryptographic and key-derivation routines, validated against captured traffic or instruction-accurate emulator output.

The hard part wasn't the cryptography -- it was getting from a stripped flash dump to a function map you could reason about. Ghidra's auto-recovery does not handle HCS12X paged flash or V850 reliably, so I wrote a custom HCS12X function walker and an instruction-accurate V850 emulator from scratch. Cipher work covered KeeLoq variants, XTEA, AES-128 ECB, a custom 6-byte block cipher, a custom PIC nibble cipher, a DST80-family stream cipher, and lagged-Fibonacci / multiplicative-LCG PRNGs. Vendor and affected vehicle platforms are under NDA.

---

### Vulnerability research

**2026-04**
- *CVE-2026-20161 published.* Cisco ThousandEyes Enterprise Agent Linux LPE.
- Additional findings on undisclosed vendors under NDA / disclosure embargo.

**2026-03**
- *Telecom carrier eSIM exposure.* Production provisioning server reachable from the internet without authentication; profile download, deletion, and batch operations exposed. Chained earlier APK research into a SIM port-in flow that auto-approved without human review on production. WAF bypass via forged HTTP header.
- *Feature flag platform.* SDK key pulled from compiled bytecode. Feature flags, employee emails, developer device identifiers, and the routing of fraud-detection flags across payment endpoints, all extracted.

**2026-02**
- *Enterprise VPN client (Linux + Windows), three independent privilege escalations.* Windows TOCTOU to SYSTEM via hardcoded 3DES IPC key plus filesystem oplock for race timing; PSIRT confirmed CVE credit. Linux IPC command injection: shell metacharacters into `system()` as root, two unauthenticated messages to a Unix socket. Linux symlink-following root file write, chained to system-wide RCE via `/etc/ld.so.preload`. Three CVEs pending. All resolved and rewarded.
- *Endpoint protection DNS parser (Windows).* One crafted UDP packet, stack overflow in the network filter service. Vendor reproduced and confirmed fix. Resolved; CVE pending.
- *Virtual gateway firmware.* Hardcoded CA private key, identical across every deployment worldwide. Working MITM proxy that forges trusted certificates for any installation.
- *Telecom webmail account takeover.* OTP brute-forced in minutes. Lockout hardcoded to zero, 2FA globally disabled, DOB validation non-functional. Same engagement: stored XSS via a sanitizer bypass exploiting DOM attribute enumeration order, secrets extracted from the Android app's obfuscated native library, host header bypass against the corporate identity server.
- *Fintech mobile app.* Patched an open-source decompiler to handle a proprietary bytecode version it could not read, then walked through authentication, payments, identity verification, and fraud-detection flows.

**2026-01**
- *Network monitoring agent (Cisco ThousandEyes Enterprise Agent).* Local privesc to root via symlink following + `ld.so.preload` injection. Disclosed to vendor; published as CVE-2026-20161 on 2026-04-15.
- *Enterprise VPN reconstructed from binaries.* Licensing blocked normal operation, so the system was rebuilt from compiled binaries. XML profile schema recovered by tracing through disassembly, unrelated bugs patched to reach the vulnerable paths. Two issues surfaced: weak default credentials on the virtual gateway giving SSH bypass, and command injection in VPN client route handling where user-controlled XML reaches `system()` as root.
- *Enterprise Linux EDR.* Reverse engineered a binary IPC protocol; surfaced quarantine bypass and cloud log injection where audit logs are poison-able with fabricated entries visible in the cloud admin console.
- *Network camera.* Unauthenticated RCE via reverse-engineered binary event-condition serialisation; arbitrary commands through user-controllable virtual inputs.

---

### Available

Remote Linux driver development, reverse engineering contracts, and vulnerability research.

**Contact:** lucid_duck@justthetip.ca | devinwittmayer@gmail.com | Vancouver Island, BC, Canada
