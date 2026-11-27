# CoChirp+ R1 integration contract (proposal)

Status: DRAFT / REVIEW ONLY. The R0 browser demo simulates events, not actual sessions or physical audio routing.

## Typed event envelope
A real producer must emit events over an explicitly authorized, authenticated transport. Example:

```json
{
  "schema": "CoChirp.SessionEvent.R1",
  "event_id": "unique-id",
  "session_id": "pseudonymous-per-session-id",
  "sequence": 42,
  "occurred_at": "ISO-8601",
  "observed_at": "ISO-8601",
  "source": "app-audio-state-controller",
  "kind": "received",
  "claim": "local-input-captured",
  "confidence": "observed",
  "route": "unknown",
  "speech_active": false,
  "consent_scope": "local-cues-only"
}
```

Required invariants:
- No `received` claim until the producer identifies the boundary: local input captured, network acknowledged, or server accepted. These are NOT interchangeable.
- Sequence numbers must increase within a source/session; duplicates are idempotent, late arrivals labeled stale.
- `processing` is not proof that any remote model is executing. Provide the exact observed boundary.
- `interrupted` means a specific stream/transport/route condition, not guessed device or whole-machine failure.
- `restored` requires a verified return of the same relevant capability, not merely a timer or cheerful beep.
- A receiver must never announce a user's sensitive content through a cue without consent.
- Never imply device pairing, OS routing, playback in a specific earbud, or human hearing from Web Audio scheduling.
- Real-time audio must be cancellable when speech starts, mute activates, tab loses foreground, output focus changes, or accessibility preferences require silence.
- Rate limit pulses, bound all timers, prefer backoff when uncertain. Distinguish silence-by-design, muted, idle, unavailable and stale.
- Emit pseudonymous records with monotonic timestamp where feasible, explicit trust boundary, policy version and redaction state.
- Outputs may render text, sound, vibration, light, or virtual character actions, according to consent, local capability and quiet-hours policy.

## Failure domains for CoRecover+
| Layer | Distinguishing observation | Disallowed inference |
| --- | --- | --- |
| microphone/input | permission, input energy, local input accept | model heard the meaning |
| transport | active channel, ACK, replay state | request was processed |
| inference | authoritative job/result event | user heard audio |
| output | audio context, output-route hint, scheduler | right/left ear audible |
| device | independently authenticated agent heartbeat | whole physical computer online |
| session | session ID and resume token where supported | cross-session continuity proven |

## Acceptance tests before integration
1. Independent browser test passes on supported CI runner with a linked run receipt.
2. Actual phone/earbud loopback tests with opt-in; no presumption of specific-ear delivery.
3. Instrumented latency from input accept through playback and acknowledgment. Report p50/p95 and uncertainty.
4. Speech-overlap test: no cues play while speech is active, including already scheduled oscillators.
5. Tab hide, mute, zero-volume and audio context interruption cancel in-flight sounds.
6. Disconnected, stale, duplicate, out-of-order and prolonged-silence simulations all fail closed.
7. Accessibility: screen reader, visual-only, haptic-only, hearing sensitivity, quiet-hours, and no startle cues.
8. Local privacy tests: no audio/video capture, network analytics or persistent ID without explicit separate permission.
9. Recovery receipts identify the real event boundary and what remains unverified.

## Release boundary
GitHub source and CI are development artifacts. Draft PR is not deployed release. Neither X2 nor any microphone, PineBuds/earbuds, ChatGPT voice runtime or CoStead relay is enrolled or controlled by this document.

## Next evolution
CoChirp (feedback) + CoHear (input evidence) + CoRoute (output policy) + CoRecover (state repair) + CoReceipts (proof) feed CoSurface/CoOrbWare embodiment, never replacing direct uncertainty with theatrical animation.
