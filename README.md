# Lucid Duck

> **Linux internals · reverse engineering · vulnerability research**

[![CVE-2026-20161](https://img.shields.io/badge/CVE--2026--20161-Cisco_ThousandEyes-critical)](https://nvd.nist.gov/vuln/detail/CVE-2026-20161) [![Linux mainline contributor](https://img.shields.io/badge/Linux_kernel-mainline_contributor-orange?logo=linux&logoColor=white)](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca) [![morrownr/mt76 collaborator](https://img.shields.io/badge/morrownr%2Fmt76-collaborator-blue)](https://github.com/morrownr/mt76) [![Available for contracts](https://img.shields.io/badge/available-remote_contracts-success)](mailto:devinwittmayer@gmail.com?subject=Contract%20inquiry)

A patch in the mainline Linux kernel, a published CVE, a from-scratch reverse-engineered Wi-Fi driver, and a paid embedded-firmware reverse-engineering contract - **all built since January 2026**, when I went full-time on Linux internals, reverse engineering, and vulnerability research.

**Available for remote contracts** - Linux driver development · reverse engineering · vulnerability research
📍 Vancouver Island, BC, Canada &nbsp;·&nbsp; ✉️ devinwittmayer@gmail.com &nbsp;·&nbsp; 🌐 [justthetip.ca](https://justthetip.ca)

---

## 🐧 Linux kernel & driver work

### 🚧 Flagship: AICSEMI AIC8800 SoftMAC driver - *in progress*

The AIC8800 USB Wi-Fi family has **no mainline Linux support**: the vendor ships a closed firmware blob and an out-of-tree module that breaks on every recent kernel. I'm writing a clean mac80211 (SoftMAC) driver from scratch, with **no source and no datasheet**, by reverse-engineering the firmware's host-side IPC protocol straight from the disassembly.

> **Working today:** &nbsp;✅ chip ID &nbsp;·&nbsp; ✅ firmware load &nbsp;·&nbsp; ✅ full bring-up &nbsp;·&nbsp; ✅ TX (injected frames) &nbsp;·&nbsp; ✅ RX (live beacons via monitor) &nbsp;·&nbsp; ✅ scan (`iw scan` returns real APs)

**Two routes to upstream, in parallel:** a pure host-side SoftMAC driver, and a chip-side trampoline that patches the vendor blob at runtime.
**Bench:** a self-built Wi-Fi 7 access point on a BPi-R4 Pro, with x86 and aarch64 clients. Target: mainline once the association layer lands.

### 📦 Upstream contributions

| Contribution | Status |
|---|---|
| rtw89 USB TX flow-control fix ([`80119a77e5b0`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=80119a77e5b0)) | ✅ **Mainline** |
| mac80211 monitor-mode injection fix (`d832f6b83d48`) | ✅ **Merged**, lands in 7.2 |
| Netgear A8500 USB device ID (`mt7925u`) | ✅ **Accepted** (wireless-next) |
| USB RF-calibration timeout fix (crash log + 5 tester confirmations) | ✅ **Merged** |
| MediaTek txpower reporting (carried in MediaTek's own series) | 🔄 In review |
| mt76 `set_sniffer` · RX-bitrate · BADFCS · teardown NULL-deref | 🔄 In review / staged |

### 📡 Also

- **rtw89 USB 2 to USB 3 switch-mode gap** - proved mainline silently caps Realtek Wi-Fi 6/6E/7 USB adapters at USB 2 speeds (**258 vs 802 Mbps** on identical hardware), across 4 adapters, 3 chipsets, and 2 host architectures.
- **[morrownr/mt76](https://github.com/morrownr/mt76) stewardship** - write/triage collaborator; liaison between the repo, linux-wireless, and MediaTek.
- **End-user [install / uninstall scripts](https://github.com/morrownr/mt76/blob/main/install-driver.sh)** - anyone who can paste a one-liner can run the patched MediaTek drivers without ever opening a kernel tree.

---

## 🔬 Embedded firmware reverse engineering - *contract, 2026*

Automotive keyless-entry firmware RE for a hardware-security vendor: **a dozen firmware images** delivered and in flight, each a **byte-exact C reimplementation** of the firmware's cryptography and key-derivation routines, validated against captured radio traffic or instruction-accurate emulation.

- **Seven MCU families:** `STM8` · `ARM Cortex-M0` · `PIC` · `HCS12 / HCS12X` · `V850` · `R32C` · `8051`
- **The hard part wasn't the cryptography:** it was getting from a stripped flash dump to a function map. Where stock tooling fell down on paged flash and uncommon cores, I wrote a custom **function walker, disassembler, and instruction-accurate emulator** from scratch.
- **Ciphers:** KeeLoq variants · XTEA · AES-128 · custom block & S-box ciphers · a DST80-family stream cipher · several PRNG designs.

---

## 🛡️ Vulnerability research

*All findings disclosed through coordinated disclosure; most have shipped fixes. Vendor names are withheld where embargoes or NDAs apply.*

- **Local root on a Linux network-monitoring agent** - [CVE-2026-20161](https://nvd.nist.gov/vuln/detail/CVE-2026-20161) (Cisco ThousandEyes), my first CVE. Symlink-following plus a Linux loader feature lets any local user gain persistent system-wide root.
- **Three privilege escalations in an enterprise VPN client:** a Windows race to SYSTEM, a Linux command injection running as root from an unauthenticated local socket, and a Linux file-write primitive that becomes system-wide RCE. Three CVEs pending; the same product also leaked credentials via a world-readable shared-memory region.
- **Remote code execution in a Windows endpoint-protection product:** one crafted UDP packet corrupts memory in the network-filter service. Vendor-confirmed, fix shipped.
- **Cross-customer impersonation on a virtual-gateway product:** a certificate-authority private key hardcoded into firmware and identical across every deployment worldwide, allowing forged certificates trusted by any install. The same product line also yielded an RSA-512 license-signing key forgery (512-bit modulus factored, private key recovered), validated on a live appliance.
- **Network-appliance SSRF to cloud IAM credential theft** via a DNS-rebinding filter bypass that reaches the instance metadata service.
- **Audit-log poisoning on an enterprise Linux EDR:** binary IPC protocol reverse-engineered into a quarantine bypass and a primitive that injects fabricated entries into the cloud admin console's audit log.

*Plus 6 further findings across identity, telecom, fintech, and IoT.*

---

<sub>45+ repositories and counting - built, tested, and documented as I go.</sub>
