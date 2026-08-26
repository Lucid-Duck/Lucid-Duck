# Lucid Duck

> **Linux internals · reverse engineering · vulnerability research**

[![CVE-2026-20161](https://img.shields.io/badge/CVE--2026--20161-Cisco_ThousandEyes-critical)](https://nvd.nist.gov/vuln/detail/CVE-2026-20161) [![Linux mainline contributor](https://img.shields.io/badge/Linux_kernel-mainline_contributor-orange?logo=linux&logoColor=white)](https://lore.kernel.org/linux-wireless/?q=lucid_duck%40justthetip.ca) [![morrownr/mt76 collaborator](https://img.shields.io/badge/morrownr%2Fmt76-collaborator-blue)](https://github.com/morrownr/mt76) [![Available for contracts](https://img.shields.io/badge/available-remote_contracts-success)](mailto:devinwittmayer@gmail.com?subject=Contract%20inquiry) [![CompTIA Security+](https://img.shields.io/badge/CompTIA-Security%2B-blueviolet?logo=comptia&logoColor=white)](https://cp.certmetrics.com/CompTIA/en/public/verify/credential/d083e581bcc54bfdaf2235d5759920f7) [![Support on Ko-fi](https://img.shields.io/badge/Ko--fi-support_my_work-FF5E5B?logo=kofi&logoColor=white)](https://ko-fi.com/lucid_duck)

Since January 2026 I've been full-time on Linux internals, reverse engineering, and vulnerability research. Since then: patches merged to the mainline Linux kernel, a published CVE (CVE-2026-20161), a clean-room Wi-Fi driver I'm building from the firmware disassembly, a paid embedded-firmware reverse-engineering contract, and CompTIA Security+.

**Available for remote contracts.** Linux driver development, reverse engineering, vulnerability research.
📍 Vancouver Island, BC, Canada &nbsp;·&nbsp; ✉️ devinwittmayer@gmail.com &nbsp;·&nbsp; 🌐 [justthetip.ca](https://justthetip.ca) &nbsp;·&nbsp; ☕ [Ko-fi](https://ko-fi.com/lucid_duck)

---

## 🐧 Linux kernel and driver work

### Upstream contributions

Merged to the mainline Linux kernel. I wrote all of these except the last pair, which I co-developed with MediaTek. Almost all of it is USB Wi-Fi, where bugs that PCIe never hits sit undisturbed for years.

**Kernel panic when bridging wired traffic to a Wi-Fi 7 USB adapter** [`ef3e34874d23`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ef3e34874d23)

The mt7925 transmit path pushes its own headers onto every outgoing frame and assumed the space for them was already reserved. It is, for traffic the machine generates itself. It is not for traffic forwarded in from another interface, so bridging ethernet to an mt7925 access point killed the kernel on the first forwarded frame that arrived short. Whether a given box hits it depends on how much slack the incoming interface happens to leave, which is why it looked random. Reproduced on a Raspberry Pi 5 bridging onboard ethernet to a Netgear A9000, originally reported on an OpenWrt router. Tagged for stable.

**A PCIe-only event crashing USB and SDIO adapters** [`da4082e91aca`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=da4082e91aca), [`feeff151c83e`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=feeff151c83e), [`39afc46c0243`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=39afc46c0243)

A hardware notification that only exists on PCIe was being handled on every bus. On USB and SDIO it reached a queue-cleanup callback those buses do not implement, so the receive worker called through a NULL pointer and the machine went down. The same defect had been copied into three drivers (mt7921, mt7925 and mt7615), so the series fixes all three. Tagged for stable.

**Realtek USB: transmit flow control was a placeholder value** [`80119a77e5b0`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=80119a77e5b0)

When the network stack asked the rtw89 USB driver how much transmit capacity was left, the driver answered with a hardcoded 42. That number is the brake the stack uses to slow a sender down, so nothing ever slowed down and in-flight transfers accumulated without limit under sustained load. The fix tracks them per hardware queue and reports the real figure. Benchmarked against the unpatched driver at full rate on two chipsets, no throughput cost, and the retransmits went to zero.

**A bus check reading the wrong half of a union** [`7981aca2bd28`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=7981aca2bd28)

Three bus types share one union in the mt76 device struct. A check asking whether a PCIe hardware offload engine was present read that memory on USB and SDIO devices too, found the unrelated USB fields non-zero, and answered yes. The driver then took the offload receive path, which skips putting received frames back in order, so the far end saw them out of order, read that as packet loss, and retransmitted. Heavy retransmission and poor throughput in access point mode across four chip families, on hardware that was working correctly. Tagged for stable.

**A timer outliving the device that scheduled it** [`81faf578320d`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=81faf578320d)

mt7925 queues a power-save work item five seconds out during multi-link setup and never cancelled it when the device stopped. Tear the device down inside that window and the timer fires into a workqueue that is already gone. Adds a stop callback that cancels the work first, covering both the PCIe and USB drivers. Tagged for stable.

**Two monitor-mode fixes for older MediaTek adapters** [`ddae0bcb01e7`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ddae0bcb01e7), [`81497634d9f8`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=81497634d9f8)

Ask an mt76x02 adapter to capture damaged frames and two things went wrong. The driver never passed the hardware's checksum-failure flag up the stack, so nothing in the resulting capture distinguished a corrupted frame from a clean one. And the bounds check on a hardware-supplied frame length was wrapped in a kernel warning, so any garbage frame off the air tainted the kernel, and brought down machines configured to treat warnings as fatal. Both showed up immediately with an MT7612U on a busy channel.

**A capture feature the firmware does not actually support** [`6f6c9800e54c`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=6f6c9800e54c)

mt76 advertised active monitor mode for every device it drives. On mt792x the firmware ignores it and turning it on stops reception altogether, so anything that asked for the feature it was promised got silence instead. Now gated behind a per-radio flag.

**Packet capture going quiet after a channel change** [`a7d35545c2ce`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=a7d35545c2ce)

Monitor mode has to be re-asserted to the firmware every time the channel changes. The mt7925 driver did that, mt7921 did not, so capture on mt7921 adapters went dead after any channel switch and reported no error to explain why. Brings the two drivers back in line with each other.

**Transmit power reported for the wrong channel** [`8286bbf62dcc`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8286bbf62dcc), [`317bc1a0590e`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=317bc1a0590e) (co-developed with MediaTek)

I reported that mt792x adapters were reporting a transmit power that did not match the channel actually in use. These two commits are the groundwork the fix sits on: the regulatory, SAR and per-rate power limit logic moves into shared helpers, so every caller derives power the same way instead of each one open-coding it.

**An adapter its own driver did not recognize** [`291b067a02b9`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=291b067a02b9)

One line. The mt7925 driver already handled the chip inside the Netgear A8500, it just did not carry the adapter's USB ID, so the kernel never bound to it and the device did nothing. It works on a stock kernel now, with no out-of-tree module.

Posted and in review on linux-wireless: an RCU fix in the mt76 USB and SDIO transmit completion path, unchecked power-state returns on the mt7921 and mt7925 PCIe reset paths, two lock-ordering fixes for the same drivers, a missing length check on the mt792x ACPI transmit-power tables, and an mt7615 fix to stop monitor interfaces tearing down connection state they do not own. Also co-developed on a MediaTek patch fixing a use-after-free in the mt792x SDIO transmit path.

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
