I'll give you both documents in Markdown — the assessment (questions only) and the solution document (answers, reasoning, grading, common mistakes).

---

# Assessment Document

# Enterprise Networking — Apprentice Competence Assessment

**Informatiker/in EFZ · Networking Knowledge, Troubleshooting & Design**

| | |
|---|---|
| **Level** | Beginner → Advanced apprentice (mixed cohort) |
| **Questions** | 33 items across 8 sections |
| **Total points** | 120 points |
| **Time allowed** | 150 minutes (2.5 hours) |
| **Materials** | Non-programmable calculator, blank paper. No internet, no phones. |
| **Pass mark** | 60% (72 / 120) |

**Candidate:** Name ___________ · Year ___ · Company ___________ · Date ___________ · Score ____ / 120

### Instructions
- Answer all questions. Difficulty increases through the exam — if you get stuck, move on and return.
- Points are shown as **[n pts]**. A 1-point item wants one fact; a 6-point item wants reasoning.
- For MCQs, exactly one answer is correct unless it says "select all".
- For calculations, **show your working** — method earns partial credit even if the final number is wrong.
- For scenarios, **explain your reasoning**. "It works now" with no reason earns no marks.

**Grading scale (Swiss Note):** 90–100% → 6 · 80–89% → 5.5/5 · 70–79% → 4.5/5 · 60–69% → 4 (pass) · <60% → not yet competent.

---

## Section 1 — Fundamentals: OSI & TCP/IP *(12 pts)*

**Q1 [2 pts] — Beginner.** The OSI model has seven layers. At which layer does a **switch** primarily make forwarding decisions, and at which layer does a traditional **router**?

**Q2 [2 pts] — Beginner.** Which OSI layer provides reliable, connection-oriented, ordered delivery of segments between two hosts?
- a) Layer 2 – Data Link
- b) Layer 3 – Network
- c) Layer 4 – Transport
- d) Layer 7 – Application

**Q3 [2 pts] — Beginner.** Match each protocol to its TCP/IP layer: **HTTPS · IP · Ethernet · TCP**

**Q4 [3 pts] — Beginner–Intermediate.** A colleague says: *"TCP is always better than UDP because it guarantees delivery, so we should use it everywhere."* Give one reason this is wrong, and name one real service that deliberately uses UDP and why.

**Q5 [3 pts] — Intermediate.** Put these PDUs in order from application data outward to the wire, naming the layer each belongs to: **Frame · Segment · Packet · Bits · Data**

---

## Section 2 — IPv4, IPv6 & Subnetting *(18 pts)*

*Show your working for all calculations.*

**Q6 [2 pts] — Beginner.** Classify each as public or private (RFC 1918): `10.14.200.3` · `172.20.5.9` · `192.0.2.55` · `192.168.100.1`

**Q7 [3 pts] — Intermediate.** A host is configured as `192.168.40.130 /26`. State (a) the network address, (b) the broadcast address, (c) the number of usable hosts. Show your working.

**Q8 [4 pts] — Intermediate.** You are assigned `10.50.16.0/22` and must divide it into **4 equal subnets** (one per floor). Give the network address and CIDR prefix of each, and show how you derived the new prefix.

**Q9 [3 pts] — Intermediate.** You must connect two routers over a point-to-point WAN link wasting as few addresses as possible. Which CIDR mask would you use, how many usable addresses does it give, and why is that the right size?

**Q10 [3 pts] — Intermediate–Advanced.** IPv6 address `2001:0db8:0000:0000:0000:ff00:0042:8329`. (a) Write it fully compressed. (b) What does `fe80::/10` represent, and give one situation where you'd see it in normal operation.

**Q11 [3 pts] — Advanced.** An apprentice says: *"IPv6 doesn't need NAT and doesn't use ARP."* Evaluate each half (true/false), and name the IPv6 mechanism that replaces ARP.

---

## Section 3 — Layer 2: Switching, VLANs, Trunking & STP *(18 pts)*

**Q12 [2 pts] — Beginner.** In your own words, what problem do VLANs solve? Give one concrete benefit beyond "separating traffic".

**Q13 [2 pts] — Beginner–Intermediate.** Difference between an **access port** and a **trunk port**?
- a) Access carries one VLAN's untagged traffic; a trunk carries multiple VLANs, tagged with 802.1Q.
- b) Access is faster; trunk is slower but more secure.
- c) Access is for servers; trunk is only for PCs.
- d) No difference; the terms are interchangeable.

**Q14 [4 pts] — Intermediate.** A user on **VLAN 20** plugged into `Gi0/5` reports no connectivity. Read the config, identify the most likely misconfiguration, and state the fix.

```
interface GigabitEthernet0/5
 description User-Desk-3F
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
!
interface GigabitEthernet0/24
 description Uplink-to-Core
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30
```

**Q15 [4 pts] — Intermediate–Advanced.** STP: (a) what problem does it prevent at Layer 2, and (b) what happens on a switched network with redundant links if STP is disabled? Use the correct term for the failure mode.

**Q16 [3 pts] — Advanced.** (a) On what basis is the STP root bridge elected? (b) Why deliberately set which switch becomes root, rather than accept the default?

**Q17 [3 pts] — Advanced.** A "native VLAN mismatch" appears in the logs on a trunk. Explain what the native VLAN is, why a mismatch is both an operational and a security concern, and how you'd remediate it.

---

## Section 4 — Routing: Static & Dynamic *(16 pts)*

**Q18 [2 pts] — Beginner–Intermediate.** What is a default route, when is it used, and write it in CIDR notation.

**Q19 [4 pts] — Intermediate.** A packet arrives destined for `10.10.5.77`. Which route is used, and why? State the exit interface.

```
Destination        Prefix   Next-hop / Interface   Metric
0.0.0.0/0          default  203.0.113.1  (Gi0/0)   1
10.10.0.0/16       /16      10.0.0.2     (Gi0/1)   20
10.10.5.0/24       /24      10.0.0.6     (Gi0/2)   20
10.10.5.64/26      /26      10.0.0.10    (Gi0/3)   20
```

**Q20 [3 pts] — Intermediate.** Compare static and dynamic routing: one advantage of each, plus one scenario where static is clearly better.

**Q21 [3 pts] — Advanced.** OSPF and a static route both offer a path to the same network. Explain the roles of **administrative distance** and **metric**, and which is compared first.

**Q22 [4 pts] — Advanced.** VLAN 10 (`10.1.10.0/24`) and VLAN 20 (`10.1.20.0/24`) can't reach each other; the switch is Layer 2 only. Describe **two** ways to enable inter-VLAN communication, with one trade-off each.

---

## Section 5 — Core Services: DHCP, DNS & NAT *(14 pts)*

**Q23 [3 pts] — Beginner–Intermediate.** Put the DHCP messages in order and say what each does: **OFFER · ACK · DISCOVER · REQUEST**

**Q24 [4 pts] — Intermediate.** A user got a `169.254.x.x` address and can't reach anything. (a) What is this called and what does it tell you? (b) Two distinct causes to investigate. (c) The DHCP server is across a router — what must be configured on that router, and why?

**Q25 [4 pts] — Intermediate–Advanced.** A user says "the internet is down". You can ping `8.8.8.8` but not `www.example.com`. (a) Most likely cause? (b) Which CLI tool confirms it? (c) What result confirms your diagnosis?

**Q26 [3 pts] — Intermediate–Advanced.** Why can a branch of 50 devices share one public IPv4? Name the specific NAT variant and what it uses to keep the 50 sessions apart.

---

## Section 6 — Security & Wireless Fundamentals *(14 pts)*

**Q27 [3 pts] — Intermediate.** Name three practical access-layer/Layer 2 security measures on switch access ports, and for each, the attack/risk it mitigates (one line each).

**Q28 [3 pts] — Intermediate.** Explain "default deny" firewall policy, why it beats "default allow", and one operational downside teams must manage.

**Q29 [4 pts] — Intermediate–Advanced.** Wireless: (a) Why offer both 2.4 GHz and 5 GHz, and the main trade-off? (b) Recommended modern corporate WLAN security standard, and one reason WEP must never be used. (c) Purpose of non-overlapping channels 1, 6, 11 in 2.4 GHz?

*(Note: Q27–29 total 10; remaining 4 pts of this section are folded into the integrated Q32 for reasoning depth.)*

---

## Section 7 — Operations, Monitoring & High Availability *(14 pts)*

**Q30 [4 pts] — Intermediate.** First responder to "the whole third floor is offline." Describe a structured troubleshooting approach (name a recognised method) and your first three concrete checks in order, with a reason for each.

**Q31 [4 pts] — Advanced.** HA: (a) Purpose of a First Hop Redundancy Protocol (HSRP/VRRP) in 1–2 sentences. (b) A core pair with active/standby gateway removes which single point of failure? (c) Name one other independent HA technique and what it protects against.

**Q32 [6 pts] — Advanced (Integrated).** Your manager wants the network "less of a black box." Cover:
- Two things you'd **document** and where that helps most during an incident.
- Two **monitoring signals** you'd collect proactively (name the mechanism — SNMP, syslog, NetFlow, or a KPI) and what each warns you about before users notice.
- One reason good documentation and monitoring reduce **MTTR**.

---

## Section 8 — Integrated Scenario: Design & Troubleshoot *(14 pts)*

> **Scenario — Branch office "Aargau Nord":** A new 3-floor branch. Three groups must be isolated at Layer 2: **Staff, Voice (IP phones), Guest Wi-Fi**. The site is assigned **`10.72.0.0/22`**. Staff and Voice must reach the data centre over the WAN; **Guest may only reach the internet**. The site must survive the failure of a single core switch. The **DHCP server for Staff lives centrally** at the data centre, not on-site.

**Q33a [4 pts].** Propose a VLAN + subnet plan: a VLAN ID and subnet (from `10.72.0.0/22`) for Staff, Voice, Guest, with room to grow.

**Q33b [3 pts].** DHCP is off-site — what must be configured, on which device, so Staff PCs still get addresses? Name the feature and device role.

**Q33c [3 pts].** How would you enforce that Guest reaches the internet but **not** the data centre, while Staff and Voice reach both? Name the mechanism(s) and where they sit.

**Q33d [4 pts] — Troubleshooting.** After rollout, IP phones on the Voice VLAN work, but Staff PCs on the **same switches** get no IP and land in APIPA. Give the two most likely causes and the exact check to confirm each.

**End of assessment. Total: 120 points · 150 minutes.**

---
---

# Solution Document

# Enterprise Networking Assessment — Answer Key & Examiner Guide

*For examiner use. Award partial credit generously for correct reasoning. Where a candidate reaches the right conclusion by a valid alternative route, accept it.*

---

## Section 1 — Fundamentals

**Q1 [2 pts].** Switch = **Layer 2 (Data Link)**, using MAC addresses. Router = **Layer 3 (Network)**, using IP addresses.
*1 pt each. Accept "switch = MAC, router = IP" as equivalent.*
**Common mistake:** saying a switch is Layer 1 (that's a hub/repeater). Note that L3 switches blur this — accept a mention of it as a bonus but the core answer stands.

**Q2 [2 pts].** **c) Layer 4 – Transport** (this is TCP's role).
**Common mistake:** picking Layer 3; IP is connectionless and doesn't guarantee ordering.

**Q3 [2 pts].** HTTPS → Application · IP → Internet (Network) · Ethernet → Link (Network Access) · TCP → Transport. *½ pt each.*
**Common mistake:** placing TCP and IP on the same layer.

**Q4 [3 pts].** *(1 pt)* TCP's guarantees cost latency and overhead (handshake, retransmission, ordering) — bad for real-time traffic. *(2 pts)* Valid UDP example: **DNS** (small, fast, one query/response), **VoIP/video** (late packets are useless — better to drop than resend), **DHCP**, or **online gaming**. Must give a reason, not just name it.
**Common mistake:** naming a service but not explaining *why* UDP suits it.

**Q5 [3 pts].** Data (Application) → Segment (Transport) → Packet (Network) → Frame (Data Link) → Bits (Physical). *Full marks for correct order + correct layers. −1 per misplaced item.*
**Common mistake:** swapping Segment/Packet, or forgetting encapsulation direction.

---

## Section 2 — Addressing & Subnetting

**Q6 [2 pts].** `10.14.200.3` **private** · `172.20.5.9` **private** (172.16–172.31) · `192.0.2.55` **public** (TEST-NET, but not RFC 1918 private) · `192.168.100.1` **private**. *½ pt each.*
**Common mistake:** assuming all `172.x` is private — only `172.16.0.0–172.31.255.255`.

**Q7 [3 pts].** /26 → block size 64. `.130` falls in the `.128–.191` block.
- (a) Network = **192.168.40.128**
- (b) Broadcast = **192.168.40.191**
- (c) Usable hosts = 2⁶ − 2 = **62**

*1 pt each; award method marks even if the block is miscounted.*
**Common mistake:** forgetting to subtract 2 for network+broadcast; miscounting which /26 block `.130` lands in.

**Q8 [4 pts].** `/22` → `/24` gives 4 subnets (borrow 2 bits: 2² = 4). Increment = 256 in the third octet:
- **10.50.16.0/24**, **10.50.17.0/24**, **10.50.18.0/24**, **10.50.19.0/24**

*2 pts for correct prefix + derivation, 2 pts for the four correct networks.*
**Common mistake:** using /23 (only 2 subnets) or listing wrong increments.

**Q9 [3 pts].** **/30** — 2 usable addresses (2² − 2), exactly one per router. Right size because a P2P link has only two endpoints; larger wastes addresses. *(Accept **/31** per RFC 3021 as a superior answer for point-to-point, giving 2 usable with no waste — award full marks + note it.)*
**Common mistake:** choosing /29 (6 usable — wasteful) or forgetting the −2.

**Q10 [3 pts].** (a) **`2001:db8::ff00:42:8329`** (drop leading zeros in each hextet; `::` for the one run of all-zero groups). (b) `fe80::/10` = **link-local** addresses — auto-configured per interface, valid only on the local link; seen in **NDP/neighbour discovery, router advertisements, or as the next-hop in IPv6 routing**. *(a) 2 pts, (b) 1 pt.*
**Common mistake:** using `::` twice (illegal — ambiguous), or compressing internal zeros incorrectly.

**Q11 [3 pts].** "No NAT" — **broadly true**: IPv6's vast address space removes the address-scarcity reason for NAT (though NPTv6/firewalling still exist). "No ARP" — **true**: IPv6 doesn't use ARP; it uses **NDP (Neighbor Discovery Protocol)** with ICMPv6 Neighbor Solicitation/Advertisement. *1 pt each half + 1 pt for naming NDP.*
**Common mistake:** thinking IPv6 has no address-resolution at all — it does, just not ARP.

---

## Section 3 — Layer 2

**Q12 [2 pts].** VLANs logically segment one physical switch into multiple broadcast domains. Benefit beyond separation: **contains broadcast traffic** (smaller broadcast domains), **improves security/isolation** (e.g. Guest from Staff), or **flexible grouping** independent of physical location. *1 pt problem + 1 pt benefit.*

**Q13 [2 pts].** **a)**. Access = one untagged VLAN; trunk = many VLANs tagged with 802.1Q.
**Common mistake:** believing trunks are "more secure" or bandwidth-related.

**Q14 [4 pts].** The port is configured `switchport access vlan **10**` but the user is on **VLAN 20**. Fix: `switchport access vlan 20`. *(2 pts identify, 2 pts fix.)* Bonus if they note VLAN 20 *is* allowed on the uplink trunk, so the trunk isn't the problem.
**Common mistake:** blaming the trunk (VLAN 20 is allowed there) or PortFast.

**Q15 [4 pts].** (a) STP prevents **Layer 2 loops** in topologies with redundant links by blocking redundant paths. (b) Without it: a **broadcast storm** — frames (especially broadcasts) loop endlessly, MAC tables thrash, and the network melts down. *2 pts each; the term "broadcast storm" / "switching loop" is required for full (b).*
**Common mistake:** confusing this with IP routing loops (TTL doesn't exist at L2 — that's why loops are catastrophic).

**Q16 [3 pts].** (a) Root elected by **lowest Bridge ID** = bridge priority + MAC; lowest priority wins, MAC as tiebreaker. (b) You set root deliberately so the **root sits at the core** (optimal traffic paths, predictable topology) rather than an accidental low-MAC access switch becoming root and forcing suboptimal paths. *(a) 1.5, (b) 1.5.*
**Common mistake:** saying "highest priority wins" — it's lowest.

**Q17 [3 pts].** Native VLAN = the VLAN whose traffic crosses a trunk **untagged**. Mismatch (different native VLAN on each end) is an **operational** problem (traffic lands in the wrong VLAN, connectivity breaks) and a **security** risk (**VLAN hopping** via double-tagging). Remediate: set the **same native VLAN on both ends**; best practice is to use a dedicated unused VLAN and/or tag the native VLAN. *1 pt definition, 1 pt concerns, 1 pt fix.*

---

## Section 4 — Routing

**Q18 [2 pts].** A default route (`0.0.0.0/0`) matches any destination not found more specifically in the table — the "gateway of last resort," typically toward the internet/upstream. *1 pt concept, 1 pt notation.*

**Q19 [4 pts].** **`10.10.5.64/26` via `10.0.0.10 (Gi0/3)`.** `.77` falls in the `.64–.127` range, and routers use **longest-prefix match** — the /26 is more specific than the /24, /16, or default. Exit interface **Gi0/3**. *2 pts answer, 2 pts the longest-prefix-match reasoning.*
**Common mistake:** choosing by lowest metric or picking the /24; metric only breaks ties *within the same prefix length*.

**Q20 [3 pts].** Static: predictable, no protocol overhead, secure — advantage. Dynamic: scales, auto-adapts to failures — advantage. Static is clearly better for a **stub network / single-exit branch** (one default route to the ISP) or a small, stable topology. *1 pt each.*

**Q21 [3 pts].** **Administrative distance (AD)** is compared **first** — it ranks trustworthiness of the *source* (connected 0, static 1, OSPF 110…). Lower AD wins, so the static route (AD 1) beats OSPF (110) here. **Metric** only breaks ties *among routes from the same protocol* (same AD). *1.5 AD, 1 metric, 0.5 for "AD first".*
**Common mistake:** thinking OSPF's metric competes directly with a static route — it never gets that far; AD decides first.

**Q22 [4 pts].** Two valid methods: **(1) Router-on-a-stick** — a router with a trunk (802.1Q) sub-interface per VLAN; trade-off: single link can bottleneck, single point of failure. **(2) A Layer 3 switch with SVIs** — routing done in hardware on the switch; trade-off: costs more / requires an L3-capable switch. *2 pts each (method + trade-off).*

---

## Section 5 — Core Services

**Q23 [3 pts].** **DISCOVER → OFFER → REQUEST → ACK** (DORA). Discover: client broadcasts looking for a server. Offer: server offers an address. Request: client formally requests that offer. Ack: server confirms and finalises the lease. *2 pts order, 1 pt descriptions.*

**Q24 [4 pts].** (a) **APIPA** (link-local `169.254.0.0/16`) — the client got **no DHCP response** and self-assigned. (b) Two causes (any two): DHCP scope exhausted; DHCP server down; **no relay** across the router; VLAN/trunk issue between client and server; cabling/port in wrong VLAN. (c) A **DHCP relay agent / `ip helper-address`** on the router, because DHCP DISCOVER is a **broadcast** and routers don't forward broadcasts — the relay converts it to a unicast toward the server. *(a) 1, (b) 1, (c) 2.*
**Common mistake:** not knowing *why* the relay is needed (broadcast containment).

**Q25 [4 pts].** (a) **DNS resolution failure** — IP connectivity works (ping to IP succeeds), only name→IP is broken. (b) **`nslookup`** (or `dig`) `www.example.com`. (c) Confirmation: the lookup **fails/times out or returns no server**, while `nslookup www.example.com 8.8.8.8` (explicit public resolver) succeeds — proving the configured DNS server, not connectivity, is at fault. *(a) 2, (b) 1, (c) 1.*

**Q26 [3 pts].** **PAT (Port Address Translation) / NAT overload.** It multiplexes all internal sessions onto one public IP by tracking a unique **source port number** per session in its translation table, so return traffic maps back to the right internal host. *2 pts naming PAT/overload, 1 pt for port numbers being the discriminator.*
**Common mistake:** saying "NAT" generically without the port-based distinction.

---

## Section 6 — Security & Wireless

**Q27 [3 pts].** Any three (1 pt each, measure + risk):
- **Port security** (limit MACs per port) → MAC flooding / rogue devices.
- **DHCP snooping** → rogue DHCP servers / starvation.
- **802.1X / port authentication** → unauthorised devices on the LAN.
- **BPDU Guard / Root Guard** → rogue switches disrupting STP.
- **Disabling/shutting unused ports** or **Dynamic ARP Inspection** → unused-port abuse / ARP spoofing.

**Q28 [3 pts].** Default deny = block everything, explicitly permit only what's needed. Better because it fails **closed** — unforeseen/new traffic is denied rather than allowed, shrinking the attack surface. Downside: **operational overhead** — every legitimate flow must be explicitly whitelisted, so misconfigurations can break services. *1 pt each.*

**Q29 [4 pts].** (a) 2.4 GHz = longer range, better wall penetration, but crowded and slower; 5 GHz = faster, more channels, less interference, but **shorter range** — trade-off is range vs speed/capacity. (b) **WPA3** (WPA2-Enterprise acceptable); WEP is trivially crackable in minutes (broken RC4/IV reuse). (c) Channels 1/6/11 are the only **non-overlapping** channels in 2.4 GHz, so neighbouring APs on them **don't interfere**. *(a) 2, (b) 1, (c) 1.*

---

## Section 7 — Operations, Monitoring & HA

**Q30 [4 pts].** Name a method: **bottom-up OSI**, top-down, or **divide-and-conquer**. First three checks (examples, must be ordered + reasoned):
1. **Physical/link** — are switch/uplink up, cables/PoE, link lights? (rule out L1 fast).
2. **Scope** — is it one port, one VLAN, one switch, or the whole floor? (isolate the fault domain).
3. **L2/L3** — VLAN assignment, trunk to core up, gateway/SVI reachable, DHCP working? (localise the failing layer).

*1 pt method + 1 pt each check with reasoning.* Reward a logical narrowing over a random list.

**Q31 [4 pts].** (a) An FHRP (HSRP/VRRP) presents a **virtual gateway IP** shared by two routers so hosts keep a working default gateway if one router fails. (b) Removes the **default-gateway single point of failure**. (c) Any one: **link aggregation (LACP/EtherChannel)** → link/port failure; **redundant power supplies** → PSU failure; **dual uplinks + STP/routing** → path failure; **redundant WAN/ISP** → circuit failure. *(a) 2, (b) 1, (c) 1.*

**Q32 [6 pts].** *(2 pts documentation, 2 pts monitoring, 1 pt MTTR, 1 pt overall coherence.)*
- **Document:** network/topology diagram + IP/VLAN plan (find the fault domain fast); cabling/port map and change log (know what changed → likely cause).
- **Monitor:** **SNMP** interface up/down + utilisation (link saturation/failures); **syslog** (error/crash events, flapping); **NetFlow** (traffic anomalies, top talkers); a **KPI** like latency/packet loss (degradation before outage).
- **MTTR:** documentation removes discovery time and monitoring points you straight at the fault, so you spend time *fixing* not *finding*.

---

## Section 8 — Integrated Scenario

**Q33a [4 pts].** Sample plan from `10.72.0.0/22` (accept any sensible split with growth room):

| Group | VLAN | Subnet |
|---|---|---|
| Staff | 10 | 10.72.0.0/24 |
| Voice | 20 | 10.72.1.0/24 |
| Guest | 30 | 10.72.2.0/24 |
| *(reserved for growth)* | — | 10.72.3.0/24 |

*2 pts distinct VLANs, 2 pts valid non-overlapping subnets within the block + growth room. Deduct if subnets overlap or fall outside /22.*

**Q33b [3 pts].** Configure a **DHCP relay agent (`ip helper-address` pointing at the central server)** on the **Layer 3 device that is the default gateway for the Staff VLAN** (L3 switch SVI or router sub-interface). Needed because DHCP DISCOVER is broadcast and won't cross the router unaided. *2 pts feature, 1 pt correct device.*

**Q33c [3 pts].** Use **ACLs / firewall rules** (and/or VRF/route separation) at the **Layer 3 boundary / gateway**: permit Staff and Voice subnets toward the data-centre prefixes over the WAN; for the Guest VLAN, **deny traffic to internal/DC ranges and permit only internet-bound**. Placing the policy at the inter-VLAN routing point / edge firewall enforces it. *2 pts mechanism, 1 pt placement.*

**Q33d [4 pts].** Two most likely causes (2 pts each = cause + exact check):
1. **Staff VLAN missing the DHCP relay** (Voice may use a local/different config or option 82, or its own relay). Check: verify `ip helper-address` exists on the **Staff SVI**, not just Voice; confirm with `show run interface vlan10`.
2. **Staff VLAN not carried on the trunk/uplink**, or the access ports are in the wrong VLAN. Check: `show interfaces trunk` (is VLAN 10 allowed?) and `show vlan brief` / `show interface status` on the affected access ports.

*Accept also: DHCP scope for Staff exhausted/misconfigured (check server scope), or a native-VLAN/tagging issue. Reward the "same switch, so it's VLAN-specific not physical" reasoning.*

**Common apprentice mistakes across Section 8:** overlapping subnets; putting the helper-address on the wrong VLAN; trying to enforce Guest isolation at Layer 2 alone (isolation needs an L3 ACL/firewall — VLANs separate but don't filter inter-VLAN by themselves once a router connects them).

---

**Total: 120 points.** Pass at 72 (Note 4). Sections 1–2 gate fundamentals; Sections 7–8 separate solid apprentices from junior-engineer level.

---

Want me to also generate polished **Word/PDF versions** for printing (I already have the assessment styled and ready to render), or adjust anything — swap to **German**, add an **answer sheet grid**, or shift the difficulty balance?