# Lucid Duck

> **Linux internals · reverse engineering · vulnerability research**

[![CVE-2026-20161](https://img.shields.io/badge/CVE--2026--20161-Cisco_ThousandEyes-critical)](https://nvd.nist.gov/vuln/detail/CVE-2026-20161) [![Linux mainline contributor](https://img.shields.io/badge/Linux_kernel-mainline_contributor-orange?logo=linux&logoColor=white)](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca) [![morrownr/mt76 collaborator](https://img.shields.io/badge/morrownr%2Fmt76-collaborator-blue)](https://github.com/morrownr/mt76) [![Available for contracts](https://img.shields.io/badge/available-remote_contracts-success)](mailto:devinwittmayer@gmail.com?subject=Contract%20inquiry) [![Support on Ko-fi](https://img.shields.io/badge/Ko--fi-support_my_work-FF5E5B?logo=kofi&logoColor=white)](https://ko-fi.com/lucid_duck)

Since January 2026 I've been full-time on Linux internals, reverse engineering, and vulnerability research. Since then: patches merged to the mainline Linux kernel, a published CVE (CVE-2026-20161), a clean-room Wi-Fi driver I'm building from the firmware disassembly, and a paid embedded-firmware reverse-engineering contract.

**Available for remote contracts.** Linux driver development, reverse engineering, vulnerability research.
📍 Vancouver Island, BC, Canada &nbsp;·&nbsp; ✉️ devinwittmayer@gmail.com &nbsp;·&nbsp; 🌐 [justthetip.ca](https://justthetip.ca) &nbsp;·&nbsp; ☕ [Ko-fi](https://ko-fi.com/lucid_duck)

---

## 🐧 Linux kernel and driver work

### Upstream contributions

Merged to mainline. I've labelled my role on each, since some I authored and others I co-developed or reported and tested:

| Patch | Commit | Role |
|---|---|---|
| rtw89: fix USB TX flow control by tracking in-flight URBs | [`80119a77e5b0`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=80119a77e5b0) | Author |
| mt76 / mt7925: add Netgear A8500 USB device ID | [`291b067a02b9`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=291b067a02b9) | Author |
| mt76 / mt7921: assert sniffer on chanctx change | [`a7d35545c2ce`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=a7d35545c2ce) | Author |
| mt76 / connac: cache txpower_cur via a helper | [`8286bbf62dcc`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8286bbf62dcc) | Co-developed |
| mt76 / connac: factor out rate power limit calculation | [`317bc1a0590e`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=317bc1a0590e) | Co-developed |
| mt76 / mt792x: report txpower for the requested vif link | [`879d754e48f6`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=879d754e48f6) | Reported, Tested |
| rtw89 / phy: increase RF calibration timeouts for USB transport | [`5055188134c3`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=5055188134c3) | Reported, Tested |
| mac80211: fix monitor mode frame capture for real chanctx drivers | [`d832f6b83d48`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=d832f6b83d48) | Tested, Signed-off |

In review on linux-wireless: mt76 NPU/PPE checks restricted to MMIO devices, mt7925 usb/sdio TX headroom, mt7925 mlo_pm_work cancel-on-stop (use-after-free), mt76 TXRX_NOTIFY dropped on non-MMIO buses (three chips), and mt76x02 fcsfail monitor-mode RX fixes.

Write and triage collaborator on [morrownr/mt76](https://github.com/morrownr/mt76): review, tester coordination, and liaison between the repo, linux-wireless, and MediaTek. The end-user [install and uninstall scripts](https://github.com/morrownr/mt76/blob/main/install-driver.sh) let anyone run the patched drivers without opening a kernel tree.

### AIC8800 open-firmware Wi-Fi driver (clean-room, in progress)

The AICSemi AIC8800 USB Wi-Fi family has no mainline Linux support: the vendor ships a closed firmware blob and an out-of-tree module that breaks on current kernels. I'm building an open mac80211 SoftMAC for it the way carl9170 and b43-openfwwf were built, my own firmware on the chip and mac80211 on the host, with no vendor blob and no hybrid.

Where it stands: I've reverse-engineered the chip's boot and init, the USB datapath, the TX and RX DMA rings, the firmware load mechanism, and the RF calibration (LOFT/IQ) path, all from the disassembly with no source and no datasheet. The open firmware is written and runs on the silicon; it is pre-first-light, with no RF emitted yet. The remaining work is the live TX pipeline and the calibration that first light depends on.

Bench: a self-built Wi-Fi 7 access point on a BPi-R4 Pro, with x86 and aarch64 clients.

### rtw89 USB 2 to USB 3 mode gap

Proved that mainline silently caps several Realtek Wi-Fi 6/6E/7 USB adapters at USB 2 speeds (258 vs 802 Mbps on identical hardware), across four adapters, three chipsets, and two host architectures. Evidence and crash reports: [rtw89-usb3-gap](https://github.com/Lucid-Duck/rtw89-usb3-gap).

---

## 🔬 Embedded firmware reverse engineering (contract, 2026)

Automotive keyless-entry firmware RE for a hardware-security vendor: a dozen firmware images delivered and in flight, each a byte-exact C reimplementation of the firmware's cryptography and key-derivation, validated against captured radio traffic or instruction-accurate emulation.

- Seven MCU families: STM8, ARM Cortex-M0, PIC, HCS12 / HCS12X, V850, R32C, 8051.
- The hard part was getting from a stripped flash dump to a function map. Where stock tooling fell down on paged flash and uncommon cores, I wrote a function walker, disassembler, and instruction-accurate emulator from scratch.
- Ciphers: KeeLoq variants, XTEA, AES-128, custom block and S-box ciphers, a DST80-family stream cipher, several PRNG designs.

---

## 🛡️ Vulnerability research

All findings disclosed through coordinated disclosure; most have shipped fixes. Vendor names are withheld where embargoes or NDAs apply.

- **Local root on a Linux network-monitoring agent:** [CVE-2026-20161](https://nvd.nist.gov/vuln/detail/CVE-2026-20161) (Cisco ThousandEyes), my first CVE. Symlink-following plus a Linux loader feature lets any local user gain persistent system-wide root.
- **Three privilege escalations in an enterprise VPN client:** a Windows race to SYSTEM, a Linux command injection running as root from an unauthenticated local socket, and a Linux file-write primitive that becomes system-wide RCE. The same product also leaked credentials via a world-readable shared-memory region.
- **Remote code execution in a Windows endpoint-protection product:** one crafted UDP packet corrupts memory in the network-filter service. Vendor-confirmed, fix shipped.
- **Cross-customer impersonation on a virtual-gateway product:** a certificate-authority private key hardcoded into firmware and identical across every deployment worldwide, plus an RSA-512 license-signing key forgery (512-bit modulus factored, private key recovered), validated on a live appliance.
- **Network-appliance SSRF to cloud IAM credential theft** via a DNS-rebinding filter bypass that reaches the instance metadata service.
- **Audit-log poisoning on an enterprise Linux EDR:** a binary IPC protocol reverse-engineered into a quarantine bypass and a primitive that injects fabricated entries into the cloud admin console's audit log.

Reported through authorized programs on Bugcrowd and HackerOne, with further findings across identity, telecom, fintech, and IoT.

---

<sub>More at [github.com/Lucid-Duck](https://github.com/Lucid-Duck) and [justthetip.ca](https://justthetip.ca), built and documented as I go.</sub>
