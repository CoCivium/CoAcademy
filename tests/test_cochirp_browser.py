"""Minimal headless browser regression for CoChirp R0.

Requires Playwright and the Chromium browser.  This verifies simulated event
logic only, not speakers, earbuds, microphone, network, or actual speech delay.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

PAGE = Path(__file__).resolve().parents[1] / "docs" / "cochirp" / "index.html"

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    errors = []
    external_requests = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: external_requests.append(request.url) if request.url.startswith(("http:", "https:")) else None)
    page.goto(PAGE.as_uri())

    assert "Sounds off by default" in page.locator("#audio-status").inner_text()
    assert page.locator("[data-event]").count() == 6

    page.locator('[data-event="received"]').click()
    assert page.locator("#state").inner_text() == "Received"
    rows = [json.loads(line) for line in page.locator("#receipts").inner_text().splitlines()]
    assert rows[-1]["kind"] == "received"
    assert rows[-1]["audio"] == "muted"
    assert rows[-1]["source"] == "user-triggered-browser-simulation"

    page.locator("#speech").check()
    page.locator('[data-event="ready"]').click()
    rows = [json.loads(line) for line in page.locator("#receipts").inner_text().splitlines()]
    assert rows[-1]["audio"] == "suppressed-speech-active"
    assert rows[-1]["haptic"] == "suppressed-speech-active"

    page.locator("#speech").uncheck()
    # Virtual time verifies that a changed state cancels queued processing pulses.
    page.clock.install()
    page.locator('[data-event="processing"]').click()
    page.locator('[data-event="restored"]').click()
    assert page.locator("#state").inner_text() == "Restored"
    prior = [json.loads(line) for line in page.locator("#receipts").inner_text().splitlines()]
    page.clock.run_for(4100)
    later = [json.loads(line) for line in page.locator("#receipts").inner_text().splitlines()]
    assert len(later) == len(prior), "stale processing pulse survived state change"

    # Processing pulses are finite: a maximum of three follow-up notifications.
    page.locator('[data-event="processing"]').click()
    page.clock.run_for(13200)
    rows = [json.loads(line) for line in page.locator("#receipts").inner_text().splitlines()]
    pulse_count = sum(row["kind"] == "processing-pulse" for row in rows)
    assert pulse_count == 3, f"expected three bounded pulses, got {pulse_count}"
    page.clock.run_for(5000)
    rows_after = [json.loads(line) for line in page.locator("#receipts").inner_text().splitlines()]
    assert sum(row["kind"] == "processing-pulse" for row in rows_after) == 3
    page.locator('[data-event="failed"]').click()
    assert page.locator("#state").inner_text() == "Failed"

    # Receipt retention is bounded, even under repeated user-triggered events.
    for _ in range(85):
        page.locator('[data-event="received"]').click()
    rows = [json.loads(line) for line in page.locator("#receipts").inner_text().splitlines()]
    assert len(rows) == 80
    assert rows[-1]["kind"] == "received"
    assert all(row["route"] == "unverified" for row in rows)

    page.locator("#self-test").click()
    assert "PASS" in page.locator("#test-status").inner_text()
    page.locator("#clear").click()
    assert page.locator("#receipts").inner_text() == "No receipts yet."
    assert page.locator("#state").inner_text() == "Waiting for a simulated event"
    assert not errors, errors
    assert not external_requests, external_requests
    browser.close()

print("PASS: CoChirp R0 headless simulated-event UX. No hardware or real connection test.")
