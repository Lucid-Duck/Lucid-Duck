# Lucid Duck

> **Linux internals · reverse engineering · vulnerability research**

[![CVE-2026-20161](https://img.shields.io/static/v1?label=CVE-2026-20161&message=Cisco%20ThousandEyes&color=blue)](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-te-agentfilewrite-tqUw3SMU) [![14 patches in Linux mainline](https://img.shields.io/badge/Linux_mainline-14_patches-orange?logo=linux&logoColor=white)](https://patchwork.kernel.org/project/linux-wireless/list/?submitter=219860&state=%2A&archive=both) [![morrownr collaborator](https://img.shields.io/badge/morrownr-collaborator-blue)](https://github.com/morrownr) [![Available for contracts](https://img.shields.io/badge/available-remote_contracts-success)](mailto:devinwittmayer@gmail.com?subject=Contract%20inquiry) [![CompTIA Security+](https://img.shields.io/badge/CompTIA-Security%2B-blueviolet?logo=comptia&logoColor=white)](https://cp.certmetrics.com/CompTIA/en/public/verify/credential/d083e581bcc54bfdaf2235d5759920f7)

Full-time on Linux internals, reverse engineering and vulnerability research since January 2026. Fourteen of my patches are in the mainline kernel. Also since January: a published CVE, two paid contracts, and an open Wi-Fi firmware I'm writing from the disassembly.

**Available for remote contracts.** Linux driver development, reverse engineering, vulnerability research.
📍 Vancouver Island, BC, Canada &nbsp;·&nbsp; ✉️ devinwittmayer@gmail.com &nbsp;·&nbsp; 🌐 [justthetip.ca](https://justthetip.ca) &nbsp;·&nbsp; ☕ [Ko-fi](https://ko-fi.com/lucid_duck)

---

## 🐧 Linux kernel

### In mainline

| Patch | Commit | Role | What was wrong |
|---|---|---|---|
| rtw89: fix USB TX flow control by tracking in-flight URBs | [`80119a77e5b0`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=80119a77e5b0) | Authored | Asked how much transmit room was left, the driver answered a hardcoded 42, so nothing ever throttled |
| mt76 / mt7925: ensure tx headroom in usb_sdio_tx_prepare_skb | [`ef3e34874d23`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ef3e34874d23) | Authored | Bridging wired traffic into a Wi-Fi access point panicked the kernel |
| mt76 / mt7921, mt7925, mt7615: drop TXRX_NOTIFY on non-MMIO buses | [`da4082e91aca`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=da4082e91aca), [`feeff151c83e`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=feeff151c83e), [`39afc46c0243`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=39afc46c0243) | Authored | An event that only exists on PCIe crashed USB and SDIO adapters |
| mt76: restrict NPU/PPE active checks to MMIO devices | [`7981aca2bd28`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=7981aca2bd28) | Authored | USB adapters read a field that means nothing off PCIe, skipped frame reordering, and lost throughput as access points |
| mt76 / mt7925: cancel mlo_pm_work on stop | [`81faf578320d`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=81faf578320d) | Authored | A power-save timer kept firing after the device it belonged to was gone |
| mt76 / mt76x02: report rx FCS errors to mac80211 | [`ddae0bcb01e7`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=ddae0bcb01e7) | Authored | Captures could not tell a corrupted frame from a clean one |
| mt76 / mt76x02: do not WARN on invalid rx descriptor length | [`81497634d9f8`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=81497634d9f8) | Authored | Any garbage frame off the air tainted the kernel, and killed it outright on some builds |
| mt76 / mt792x: do not advertise active monitor | [`6f6c9800e54c`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=6f6c9800e54c) | Authored | Turned off a capture mode that received nothing. I later traced the cause to the wireless stack itself and [posted a revert](https://lore.kernel.org/linux-wireless/20260903200947.27051-1-lucid_duck@justthetip.ca/) |
| mt76 / mt7921: assert sniffer on chanctx change | [`a7d35545c2ce`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=a7d35545c2ce) | Authored | Packet capture went dead after a channel change, with no error to explain it |
| mt76 / connac: cache txpower_cur via a helper | [`8286bbf62dcc`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=8286bbf62dcc) | Co-authored | Groundwork for a bug I reported: adapters reported transmit power for the wrong channel |
| mt76 / connac: factor out rate power limit calculation | [`317bc1a0590e`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=317bc1a0590e) | Co-authored | Same series. Folded three copies of the power-limit maths into one helper |
| mt76 / mt7925: add Netgear A8500 USB device ID | [`291b067a02b9`](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=291b067a02b9) | Authored | An adapter its own driver already supported but did not recognise |

Six carry a stable tag. Five have shipped in the stable trees, across six branches back to 6.1. The oldest bug in the table dates to 2017.

Most of them share a cause. USB and SDIO adapters, and monitor mode, run through code that was only ever tested on PCIe cards doing ordinary client traffic.

### ❤️ morrownr's repos

Write and triage collaborator on three of [morrownr](https://github.com/morrownr)'s repos. Review, tester coordination, and the link between them, linux-wireless and upstream.

- **[USB-WiFi](https://github.com/morrownr/USB-WiFi)**: adapter reviews, a list of what actually works on Linux, chipset tables and user support. I'm listed as one of its two site maintainers.
- **[mt76](https://github.com/morrownr/mt76)**: out-of-tree builds of the mt76 driver for kernels 6.12 through 7.2, so people get current fixes without waiting on a distro. The [install scripts](https://github.com/morrownr/mt76/blob/main/install-driver.sh) handle DKMS and Secure Boot.
- **[rtw89](https://github.com/morrownr/rtw89)**: the same job for the rtw89 series, writing and testing USB drivers with the aim of getting them upstream.

### AIC8800 open firmware (clean-room, in progress)

This USB Wi-Fi family has no mainline support. The vendor's own driver was told upstream to be redesigned from scratch first, and the licence on its firmware is still unresolved. So I'm writing a replacement: my firmware on the chip, the standard Linux stack on the host, no vendor blob.

    reverse engineered   boot and init, the USB data path, the transmit and receive
                         rings, firmware load, and the calibration that nulls carrier
                         leakage. From the disassembly, with no source and no datasheet
    written and running  the calibration, clean on silicon
    still to come        first light. No frame, no carrier, nothing on air yet
    on-silicon fires     14, each matching the vendor's own emitting register state
                         byte for byte, every one dark

---

## 🔬 Contract work

**Automotive keyless entry, 2026.** A dozen firmware images for a hardware-security vendor, delivered and in flight. Each delivery is a C reimplementation of that firmware's cryptography and key derivation, checked byte for byte against captured radio traffic or against an emulator.

    cores      STM8, ARM Cortex-M0, PIC, HCS12 and HCS12X, V850, R32C, 8051
    ciphers    KeeLoq variants, XTEA, AES-128, a DST80-family stream cipher,
               custom block and S-box designs, several PRNGs

The hard part was getting from a stripped flash dump to a function map. Stock tooling gave up on paged flash and the uncommon cores, so I wrote my own function walker, disassembler and emulator.

**Linux wireless driver, current.** Driver work for a module vendor so their USB part can carry long-range video links. Fixed-rate injection, narrow 5 and 10 MHz channels, and getting the result upstream.

---

## 🛡️ Vulnerability research

Reported through Bugcrowd and HackerOne. Vendor names are withheld where an embargo or agreement applies.

- **First CVE, arbitrary file overwrite as root.** [CVE-2026-20161](https://sec.cloudapps.cisco.com/security/center/content/CiscoSecurityAdvisory/cisco-sa-te-agentfilewrite-tqUw3SMU) (Cisco ThousandEyes). A monitoring agent running as root followed a symlink out of its own log directory, so a local user with low privileges could overwrite any file on the box. Fixed in 1.234.0.

- **Five privilege escalations in one enterprise VPN client.** A race to SYSTEM and a forced-authentication escalation on Windows. On Linux, a local socket that ran a caller's commands as root, a path traversal through that same socket, and arbitrary file write as root by symlink.

- **Windows logon passwords out of the same product.** A shared memory object any user could write held the address its credential provider sends passwords to. Point that at your own listener, decrypt with a key hardcoded in the product, and you have someone else's password.

- **Denial of service on a Windows endpoint-protection product.** A DNS response carrying a few thousand chained compression pointers makes the network filter recurse until it runs out of stack. The process dies and network-level protection stays down. The vendor reproduced it.

- **A certificate authority private key shipped inside firmware.** A virtual gateway's published image carries one CA key, generated once and identical in every deployment. Pull it out of the public image, forge a certificate the appliance trusts, sit on the management channel. Reproduced by the triager, then closed by the vendor as not applicable.

- **Licence forgery on a network management appliance.** The signing key was a 512-bit RSA modulus. Factored it, recovered the private key, forged licences on a live appliance.

- **SSRF to cloud credentials.** DNS rebinding walked through a cloud networking product's SSRF filter and reached the instance metadata service, which hands out the host's cloud credentials.

- **Quarantine bypass and audit log forgery on a Linux endpoint product.** A world-writable scanning socket speaking a binary protocol. Reverse engineered it into a quarantine bypass and into a way to write fabricated entries into the cloud console's audit log.

- **Two account takeovers at a telecom carrier.** One takes over a webmail account with no click, through a hole in the HTML sanitiser. The other resets any customer's password by brute forcing a one-time code that has no rate limit.

Further findings across identity, fintech and IoT.

---

<sub>[justthetip.ca](https://justthetip.ca): the writing, and every machine and radio on the lab bench.</sub>
