// Actual public-HTTPS browser interactions, not a synthetic DOM shim or a user study.
// No credentials, third-party navigation, storage, arbitrary clicks or OS actions.
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import { chromium } from "playwright";

const BASE = "https://cocivium.github.io/CoAcademy/";
const reports = [];
const output = "public-first-use-browser-receipt.json";
const cases = [
  { name: "desktop", viewport: { width: 1440, height: 900 }, reducedMotion: "no-preference" },
  { name: "mobile-reduced-motion", viewport: { width: 390, height: 844 }, reducedMotion: "reduce" },
];

function checkOrigin(request, stray) {
  const url = new URL(request.url());
  if (url.origin !== new URL(BASE).origin) {
    stray.push({ kind: request.resourceType(), blocked: true });
  }
}
function assertNoHorizontalOverflow(result) {
  assert.ok(result.scrollWidth <= result.clientWidth + 2,
    "horizontal overflow: " + result.scrollWidth + " > " + result.clientWidth);
}
function checkPacket(packet) {
  assert.equal(packet.schema, "CoGbx.SurfaceParity.R1");
  assert.equal(packet.work_id, "cogbx:synthetic:one-work");
  assert.equal(packet.evidence_class, "SYNTHETIC_OFFLINE_FIXTURE");
  assert.equal(packet.currentness, "FIXTURE_ONLY");
  assert.equal(packet.remote_receiver, "UNKNOWN");
  assert.equal(packet.real_device_observation, "NOT_PERFORMED");
  assert.equal(packet.authority, "LOCAL_REVERSIBLE_INPUT_ONLY");
  assert.equal(packet.external_effects, 0);
  assert.equal(packet.provider_calls, 0);
}
async function checkCogbx(browser, item) {
  const context = await browser.newContext({
    viewport: item.viewport,
    reducedMotion: item.reducedMotion,
    serviceWorkers: "block",
  });
  const page = await context.newPage();
  const external = [];
  const browserErrors = [];
  page.on("request", req => checkOrigin(req, external));
  page.on("pageerror", err => browserErrors.push(err.name));
  try {
    const response = await page.goto(BASE + "cogbx/", { waitUntil: "load", timeout: 30000 });
    assert.equal(response?.status(), 200);
    await page.locator("#machineProof").waitFor({ state: "attached" });
    await page.waitForFunction(() => Boolean(document.querySelector("#machineProof")?.textContent));
    assert.equal(await page.locator("#humanCurrentness").textContent(), "fixture only");
    const jsonA = await page.locator("#machineProof").textContent();
    const jsonB = await page.locator("#textMachineProof").textContent();
    assert.equal(jsonA, jsonB, "two views must expose exact same machine packet");
    const packet = JSON.parse(jsonA);
    checkPacket(packet);

    await page.locator("#textBtn").focus();
    await page.keyboard.press("Enter");
    assert.equal(await page.locator("#textBtn").getAttribute("aria-pressed"), "true");
    assert.equal(await page.locator(".textview").isVisible(), true);
    await page.locator("#ambientBtn").click();
    assert.equal(await page.locator("#ambientBtn").getAttribute("aria-pressed"), "true");
    await page.locator("#mapBtn").click();
    assert.equal(await page.locator("#mapBtn").getAttribute("aria-pressed"), "true");
    await page.locator("#threeBtn").click();
    assert.equal(await page.locator("#threeBtn").getAttribute("aria-pressed"), "true");
    await page.locator("#threeBtn").click();
    assert.equal(await page.locator("#threeBtn").getAttribute("aria-pressed"), "false");

    await page.locator('[data-node="unknown"]').click();
    assert.match(await page.locator("#focusText").textContent(), /UNKNOWN stays explicit/);
    const initial = "A bounded synthetic question";
    await page.locator("#draft").fill(initial);
    await page.locator("#acceptBtn").click();
    assert.match(await page.locator("#draft").inputValue(), /compare recovery before materialization/);
    assert.match(await page.locator("#receipt").textContent(), /SEND 0.*EXECUTE 0/);
    await page.locator("#undoBtn").click();
    assert.equal(await page.locator("#draft").inputValue(), initial);
    await page.locator("#rejectBtn").click();
    assert.match(await page.locator("#receipt").textContent(), /SEND 0.*EXECUTE 0/);

    await page.locator("summary").filter({ hasText: "Inspect the work behind this view" }).click();
    assert.equal(await page.locator("#machineProof").isVisible(), true);
    assert.equal(await page.locator("#machineProof").textContent(), jsonA);
    assert.equal(await page.locator("#textMachineProof").textContent(), jsonB);

    const dims = await page.evaluate(() => ({
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      reduceMotion: window.matchMedia("(prefers-reduced-motion: reduce)").matches,
    }));
    assertNoHorizontalOverflow(dims);
    assert.equal(dims.reduceMotion, item.reducedMotion === "reduce");
    assert.deepEqual(external, [], "no third-party requests");
    assert.deepEqual(browserErrors, [], "no uncaught browser exceptions");
    return { view: item.name, result: "PASS", http_status: response.status(),
             source_work_id: packet.work_id, packet_bytes: jsonA.length,
             mode_switches: 5, keyboard_toggle: "PASS", local_accept_undo: "PASS",
             known_unknown_preserved: true, horizontal_overflow: false,
             reduced_motion: dims.reduceMotion, third_party_requests: 0, page_errors: 0 };
  } finally {
    await context.close();
  }
}
async function checkMega(browser, item) {
  const context = await browser.newContext({
    viewport: item.viewport, reducedMotion: item.reducedMotion, serviceWorkers: "block",
  });
  const page = await context.newPage();
  const external = [];
  const browserErrors = [];
  page.on("request", req => checkOrigin(req, external));
  page.on("pageerror", err => browserErrors.push(err.name));
  try {
    const response = await page.goto(BASE + "megascroller/#highlights", {waitUntil: "load",timeout: 30000});
    assert.equal(response?.status(), 200);
    assert.equal(await page.locator(".highlight-card").count(), 10);
    assert.equal(await page.locator(".highlight-art").count(), 10);
    const result = await page.locator(".highlight-card").evaluateAll(anchors => anchors.map(a => ({
      id: a.getAttribute("data-asset-id"), href: a.getAttribute("href"),
      title: a.querySelector("strong")?.textContent,
      art: a.querySelector("svg")?.getAttribute("aria-label"),
    })));
    assert.equal(new Set(result.map(x=>x.id)).size, 10);
    for (const link of result) {
      assert.ok(link.id && link.title && link.art, "missing a source-bound visual card");
      assert.ok(link.href?.startsWith("https://github.com/CoCivium/CoCivium/blob/main/"),
        "source link missing or unexpected destination");
    }
    const dims = await page.evaluate(() => {
      const vw = document.documentElement.clientWidth;
      const overshooting = [...document.querySelectorAll("body *")]
        .map(el => {
          const rect = el.getBoundingClientRect();
          return {
            name: el.tagName.toLowerCase(), id: el.id || null,
            classes: String(el.className?.baseVal || el.className || "").slice(0,75),
            right: Math.round(rect.right), left: Math.round(rect.left),
            width: Math.round(rect.width),
          };
        })
        .filter(el => el.right > vw + 2 && el.left < vw + 1000)
        .sort((a,b)=>b.right-a.right)
        .slice(0,12);
      return {
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: vw, overshooting,
      };
    });
    if (dims.scrollWidth > dims.clientWidth + 2)
      console.error("ATLAS_MOBILE_OVERFLOW_ELEMENTS " + JSON.stringify(dims.overshooting));
    assertNoHorizontalOverflow(dims);
    assert.deepEqual(external, []);
    assert.deepEqual(browserErrors, []);
    return {view: item.name, result:"PASS", http_status:response.status(),
            highlight_cards:result.length, distinct_ids:10,
            original_inline_svg:10, all_source_links_grounded:true,
            horizontal_overflow:false, third_party_requests:0, page_errors:0};
  } finally {
    await context.close();
  }
}
const report = {
  schema: "CoAcademy.PublicFirstUseBrowserReadback.R0",
  source_commit: process.env.GITHUB_SHA || "LOCAL_UNBOUND",
  evidence_scope: "GITHUB_RUNNER_REAL_CHROMIUM_HTTPS_AND_INTERACTIONS",
  tests: [],
  result: "HOLD",
  nonclaims: [
    "BROWSER_AUTOMATION_NE_REAL_HUMAN_COMPREHENSION",
    "PAGES_ON_GITHUB_NE_INDEPENDENT_FAILURE_DOMAIN",
    "CI_BROWSER_NE_X2_NATIVE_UI",
    "SYNTHETIC_LOCAL_ACCEPT_NE_AUTHORIZED_EXTERNAL_EFFECT",
    "MOBILE_VIEWPORT_NE_ACTUAL_USER_DEVICE",
  ],
};
let browser;
try {
  browser = await chromium.launch({headless:true, args:["--no-sandbox"]});
  for (const item of cases) {
    report.tests.push({surface:"cogbx", ...await checkCogbx(browser, item)});
    report.tests.push({surface:"megascroller", ...await checkMega(browser, item)});
  }
  report.result = "PASS_SCOPED_BROWSER_INTERACTIONS";
} catch (error) {
  report.failure_class = error?.name || "BrowserProbeError";
  report.failure_stage = "LIVE_BROWSER_ACCEPTANCE";
  console.error("HOLD_BROWSER_PROBE: " + String(error?.message || error).slice(0,420));
  process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  await fs.writeFile(output, JSON.stringify(report,null,2) + "\n", "utf8");
  console.log(JSON.stringify({schema:report.schema,result:report.result,tests:report.tests.length,
    failure_class:report.failure_class||null}));
}
