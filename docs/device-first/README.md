# CoDevice Bridge R0 | Real-device proof, one device at a time

**October 24, 2026.** Public browser-first experiment. No enrolled devices or independent hardware acceptance is claimed.

## First two-minute trial

On a non-X2 phone or tablet, open the public CoDevice Bridge URL and click **Run local capability check**. This observes only permission-free browser API availability, not identity or sensors. It does not submit data.

If supported, click **Enable offline shell** while online. Then test a real offline reload. The registration message alone does not qualify an offline PASS. **Remove offline shell** explicitly unregisters this app-scoped worker and removes app-prefixed caches. No other site should be disturbed.

Optional: Browser A generates a harmless HELLO using a random challenge and SHA-256 digest. A person carries it into browser B, which verifies the digest and generates an ACK. The person carries ACK to browser A for a matching check. This proves at most a user-mediated text roundtrip, not independent hardware identity, secure transport, source authentication, or an active receiver fleet. No credential or private data belongs in the packet.

## Architecture and permissions

CoCivium's [device enrollment policy](https://github.com/CoCivium/CoCivium/blob/main/ai/device-enrollment-policy.json) still says NO_DEVICE_ENROLLED and PRIMARY_X2_PILOT_FIRST for dependent endpoints. This is a public opt-in browser experience, not dependent-device enrollment. X2 is under a separate hold and is not accessed.

The CoOnramp/browser substrate research treats the browser as a useful cross-platform projection, not a durable privileged control plane. Native RickBar, CoGateway, authenticated leases, persistent cross-device session restore, CoPhoenix independence, and CoStead custody remain unproven by this app.

## Source and independent acceptance

- Static source/JS syntax pass is not real browser use.
- Successful GitHub Pages workflow is not independent outside-host reachability.
- A non-X2 device must independently load the exact page and report one actual useful capability.
- Opt-in offline availability must be tested by real reload with connectivity disabled.
- Two distinct devices must be witnessed exchanging a packet and ACK to establish a real dual-device trial, though still not cryptographic hardware attestation.
- Mobile/keyboard/screenreader accessibility needs actual observation.
- Preserve all FAIL, HELD, INCONCLUSIVE and NOT_RUN results with a source version and meaningful repair condition.

The opt-in service worker uses only same-origin GET requests for the public app shell. It never caches user packets, sends analytics, asks for microphone/camera/location access, or runs an autonomous background agent. User text resides in tab memory until cleared or reloaded.

**Proof ladder:** GitHub source -> Pages -> independent HTTPS -> real device -> offline reload -> dual-device ACK -> separately authorized native receiver. No step substitutes for the next.

Source: https://github.com/CoCivium/CoAcademy/blob/master/docs/device-first/index.html

Existing fleet contract: https://github.com/CoCivium/CoCivium/blob/main/docs/UX/COFLEET_RICKBAR_R4.md

CoEx beats CoInt. Pointer is not ACK. Offline browser shell is not disaster recovery.
