# Lucid Duck

**Four months ago I started doing this full-time. 3,183 GitHub contributions later:**

- One mainline Linux kernel commit upstreamed ([rtw89 USB TX flow control](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=80119a77e5b0)), with more in the queue.
- One published CVE ([CVE-2026-20161](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-te-agentfilewrite-tqUw3SMU), Cisco ThousandEyes) and three more vendor-confirmed and CVE-pending.
- An active automotive keyless-entry firmware reverse-engineering contract -- nine firmware images across five microcontroller families, byte-exact C ports of the cryptography in each.
- Stewardship of [morrownr/mt76](https://github.com/morrownr/mt76), the community out-of-tree MediaTek WiFi driver tree.
- 38 active bug bounty engagements and counting.
- Wrote and shipped end-user [install / uninstall scripts](https://github.com/morrownr/mt76/blob/main/install-driver.sh) for the patched MediaTek WiFi drivers, so anyone who can copy-paste a one-liner can run them without ever opening a kernel source tree.

The records match the pace: 45+ GitHub repos built from scratch, every email and message timestamped, every receipt, TODO, and invoice logged at granularity that probably crosses a line. Really making the "try" in "try-hard" pay dividends.

**Available for remote contracts:** Linux driver development, reverse engineering, vulnerability research.
lucid_duck@justthetip.ca | devinwittmayer@gmail.com | Vancouver Island, BC, Canada | [justthetip.ca](https://justthetip.ca)

---

### Linux kernel and driver work

- **Merged to mainline (2026-04-02):** rtw89 USB TX flow control fix, see above.

- **In review on linux-wireless:** Sean Wang's [`wifi: mt76: connac: use a helper to cache txpower_cur`](https://lore.kernel.org/linux-wireless/20260401182322.64355-1-sean.wang@kernel.org/) v2 series (3 patches, 2026-04-01), credited Reported-by + Tested-by on all three patches and Co-developed-by + Signed-off-by on the first two. MediaTek MT7921 / MT7922 / MT7925 adapters were reporting transmit power as 3 dBm regardless of the regulatory limit, because the cached value was overwritten on every channel scan. Awaiting merge by mt76 maintainer Felix Fietkau. Local history: [mt7921-txpower-fix](https://github.com/Lucid-Duck/mt7921-txpower-fix).

- **Awaiting community Tested-by reports:** [mt76 RX bitrate reporting fix](https://github.com/Lucid-Duck/mt76-rxrate) for MT7921 / MT7922 / MT7925. Patch is posted; needs independent test confirmations from other users before maintainer merge.

- **Submitted, awaiting review:** [Netgear A8500 USB device ID for mt7925u](https://lore.kernel.org/linux-wireless/20260326190346.415226-1-lucid_duck@justthetip.ca/), 2026-03-26.

- **Open research, patch path identified:** [rtw89 USB 2 to USB 3 switch-mode gap](https://github.com/Lucid-Duck/rtw89-usb3-gap). Mainline rtw89 silently caps Realtek WiFi 6/6E/7 USB adapters at high-speed (USB 2) rates because the code that switches them into SuperSpeed (USB 3) mode lives in an out-of-tree driver and was never upstreamed. Same DWA-X1850 hardware: 258 Mbps stock vs 802 Mbps with the out-of-tree driver.

---

### Embedded firmware reverse engineering -- active contract

**April 2026.** Automotive keyless-entry firmware reverse engineering for a law-enforcement security vendor. Nine firmware images across five microcontroller families: STM8, ARM Cortex-M0, PIC mid-range, HCS12 / HCS12X, V850. Per-image deliverable was a byte-exact C reimplementation of the firmware's cryptographic and key-derivation routines, validated against captured radio traffic or instruction-accurate emulator output.

The hard part wasn't the cryptography. It was getting from a stripped flash dump to a function map you could reason about. Ghidra's automatic analysis does not handle HCS12X paged flash or V850 reliably, so I wrote a custom HCS12X function walker and an instruction-accurate V850 emulator from scratch. Cipher work covered KeeLoq variants, XTEA, AES-128 ECB, a custom 6-byte block cipher, a custom PIC nibble cipher, a DST80-family stream cipher, and lagged-Fibonacci / multiplicative-LCG pseudo-random number generators. Vendor and affected vehicle platforms are under NDA.

---

### Vulnerability research

All findings disclosed to affected vendors through coordinated disclosure. Most have shipped fixes. Vendor names are withheld where embargoes still apply.

- **Local root on a major networking vendor's Linux monitoring agent.** Symlink-following plus a Linux loader feature lets any local user gain persistent system-wide root. Published as CVE-2026-20161 on 2026-04-15.

- **Three independent privilege escalations in an enterprise VPN client.** A Windows race condition that yields SYSTEM-level access, a Linux command injection that runs as root from an unauthenticated local socket, and a Linux file-write primitive that becomes system-wide remote code execution. Three CVEs pending.

- **Remote code execution in a Windows endpoint protection product.** A single crafted UDP packet causes a memory corruption bug in the network filter service. Vendor reproduced and confirmed the fix. CVE pending.

- **Cross-customer impersonation on a virtual gateway product.** A certificate authority private key was hardcoded into the firmware and identical across every deployment worldwide, allowing forged certificates trusted by any installation.

- **Account takeover on a national telecom's webmail.** Login OTP lockout was hardcoded to zero, two-factor authentication was globally disabled, and date-of-birth validation was non-functional. Same engagement also produced stored XSS via a sanitiser bypass and secret extraction from the Android app's obfuscated native library.

- **Production provisioning server exposed to the internet at a telecom carrier.** An eSIM provisioning API reachable without authentication, allowing profile download, deletion, and batch operations. Chained earlier mobile-app research into a production SIM port-in flow that auto-approved without human review.

- **Feature flag platform compromise.** SDK key extracted from compiled mobile-app bytecode, exposing employee emails, developer device identifiers, and the routing of fraud-detection flags across payment endpoints.

- **Unauthenticated remote code execution on a network camera.** Reverse-engineered binary event-condition protocol allows arbitrary commands through user-controllable virtual inputs.

- **Audit-log poisoning on an enterprise Linux EDR.** Binary IPC protocol reverse engineered, surfacing both quarantine bypass and a primitive that injects fabricated entries into audit logs visible in the cloud admin console.

- **Enterprise VPN reconstructed from compiled binaries.** Two issues surfaced: weak default credentials on the virtual gateway giving SSH bypass, and command injection in route handling where user-controlled XML reaches a system call as root.

- **Fintech mobile app analysis.** Patched an open-source decompiler to handle a proprietary bytecode version it could not read, then walked through authentication, payments, identity verification, and fraud-detection flows.

Additional findings on undisclosed vendors under NDA.
