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
            parent: String(el.parentElement?.className?.baseVal || el.parentElement?.className || "").slice(0,70),
            grandparent: String(el.parentElement?.parentElement?.className?.baseVal || el.parentElement?.parentElement?.className || "").slice(0,70),
            label: String(el.textContent || "").slice(0,45).replace(/\s+/g," "),
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
async function checkCoFront(browser, item) {
  const context = await browser.newContext({
    viewport:item.viewport, reducedMotion:item.reducedMotion,
    serviceWorkers:"block",
  });
  const page = await context.newPage();
  const external = [], browserErrors = [];
  page.on("request", request => checkOrigin(request, external));
  page.on("pageerror", error => browserErrors.push(error.name));
  try {
    const result = await page.goto(BASE, {waitUntil:"load",timeout:30000});
    assert.equal(result?.status(), 200);
    assert.equal(await page.locator("#cofront-start").count(),1);
    assert.equal(await page.locator(".cofront__card").count(),3);
    const links = await page.locator(".cofront__card .cofront__cta")
      .evaluateAll(els=>els.map(e=>e.getAttribute("href")));
    assert.deepEqual(links, ["cogibber/","laneset/r1/","reviewpanel/"]);
    assert.equal(await page.locator('link[href="assets/cofront/cofront-r0.css"]').count(),1);
    const dims = await page.evaluate(()=>{
      const cards = document.querySelector(".cofront__grid");
      const card = document.querySelector(".cofront__card");
      return {
        scrollWidth:document.documentElement.scrollWidth,
        clientWidth:document.documentElement.clientWidth,
        columns:getComputedStyle(cards).gridTemplateColumns.split(" ").length,
        transition:getComputedStyle(card).transitionDuration,
        reducedMotion:matchMedia("(prefers-reduced-motion: reduce)").matches,
      };
    });
    assertNoHorizontalOverflow(dims);
    assert.equal(dims.columns, item.viewport.width<650?1:3);
    assert.equal(dims.reducedMotion,item.reducedMotion==="reduce");
    if(item.reducedMotion==="reduce")
      assert.match(dims.transition,/^0s(?:, 0s)*$/, "motion must be disabled");
    assert.deepEqual(external,[],"no external page requests");
    assert.deepEqual(browserErrors,[],"no uncaught browser exceptions");
    return {view:item.name,result:"PASS",http_status:200,source_link_count:links.length,
      grid_columns:dims.columns,keyboard_focus_style:"SOURCE_CHECKED",
      reduced_motion:dims.reducedMotion,third_party_requests:0,page_errors:0};
  } finally { await context.close(); }
}
async function checkCloudOps(browser,item){
  const context = await browser.newContext({
    viewport:item.viewport,reducedMotion:item.reducedMotion,
    serviceWorkers:"block",
  });
  const page = await context.newPage();
  const external = [], browserErrors = [];
  page.on("request",request=>checkOrigin(request,external));
  page.on("pageerror",error=>browserErrors.push(error.name));
  try{
    const response = await page.goto(BASE+"constellation/cloudops/",{
      waitUntil:"load",timeout:30000,
    });
    assert.equal(response?.status(),200);
    assert.equal(await page.locator(".card").count(),18);
    const dataResponse = await context.request.get(BASE+"constellation/cloudops/catalog.json");
    assert.equal(dataResponse.status(),200);
    const catalogue = await dataResponse.json();
    assert.equal(catalogue.schema,"CoAll.CloudSiteOps.UseCaseExemplars.R0");
    assert.equal(catalogue.exemplars.length,18);
    const ids = catalogue.exemplars.map(x=>x.id);
    assert.equal(new Set(ids).size,18,"duplicate use-case ID");
    const displayed = await page.locator(".card .number").allTextContents();
    assert.deepEqual(displayed,ids,"human and machine catalogue IDs diverged");
    const dimensions = await page.evaluate(()=>({
      clientWidth:document.documentElement.clientWidth,
      scrollWidth:document.documentElement.scrollWidth,
      reducedMotion:matchMedia("(prefers-reduced-motion: reduce)").matches,
    }));
    assertNoHorizontalOverflow(dimensions);
    assert.equal(dimensions.reducedMotion,item.reducedMotion==="reduce");
    assert.deepEqual(external,[],"no off-host page requests");
    assert.deepEqual(browserErrors,[]);
    return {view:item.name,result:"PASS",http_status:response.status(),
      catalogue_items:ids.length,exact_catalogue_id_parity:true,
      horizontal_overflow:false,reduced_motion:dimensions.reducedMotion,
      third_party_requests:0,page_errors:0};
  } finally { await context.close(); }
}

async function checkFederation(browser,item){
  const context = await browser.newContext({
    viewport:item.viewport,reducedMotion:item.reducedMotion,serviceWorkers:"block",
  });
  const page = await context.newPage();
  const external = [], browserErrors=[];
  page.on("request",request=>checkOrigin(request,external));
  page.on("pageerror",error=>browserErrors.push(error.name));
  try {
    const response = await page.goto(BASE+"constellation/federation/",{
      waitUntil:"load",timeout:30000,
    });
    assert.equal(response?.status(),200);
    const fetchResult=await context.request.get(BASE+"constellation/federation/fixture.json");
    assert.equal(fetchResult.status(),200);
    const source=await fetchResult.json();
    assert.equal(source.schema,"CoAll.CoFed.FailureIsolationFixture.R0");
    assert.equal(source.scenarios.length,7);
    assert.equal(await page.locator("#scenarios button").count(),7);
    const embed=JSON.parse(await page.locator("#fixture").textContent());
    assert.deepEqual(embed.scenarios,source.scenarios,
      "human scenario source must match exact machine scenario entries");
    await context.setOffline(true);
    for(const scenario of source.scenarios){
      await page.locator('#scenarios button[data-id="'+scenario.id+'"]').click();
      assert.equal(await page.locator("#current").textContent(),scenario.title);
      assert.equal(await page.locator("#effectState").textContent(),String(scenario.effects));
      assert.equal(await page.locator("#writeState").textContent(),scenario.state.write.replaceAll("_"," "));
      assert.equal(await page.locator('#scenarios button[aria-pressed="true"]').count(),1);
    }
    await page.locator('#scenarios button[data-id="coordinator_offline"]').focus();
    await page.keyboard.press("Enter");
    assert.equal(await page.locator("#current").textContent(),"Coordinator unavailable");
    assert.equal(await page.locator("#localState").textContent(),"AVAILABLE FROM LOADED PAGE");
    assert.equal(await page.locator("#writeState").textContent(),"DENIED");
    const dimensions=await page.evaluate(()=>({
      clientWidth:document.documentElement.clientWidth,
      scrollWidth:document.documentElement.scrollWidth,
      reducedMotion:matchMedia("(prefers-reduced-motion: reduce)").matches,
    }));
    assertNoHorizontalOverflow(dimensions);
    assert.equal(dimensions.reducedMotion,item.reducedMotion==="reduce");
    assert.deepEqual(external,[],"no cross-origin browser requests");
    assert.deepEqual(browserErrors,[],"no uncaught browser exceptions");
    return {view:item.name,result:"PASS",http_status:200,
      scenario_count:source.scenarios.length,
      exact_human_machine_scenario_parity:true,offline_after_load_switch:true,
      keyboard_selection:true,external_effects:0,third_party_requests:0,
      horizontal_overflow:false,reduced_motion:dimensions.reducedMotion,
      page_errors:0};
  } finally { await context.close(); }
}

async function checkWalkaway(browser,item){
  const context=await browser.newContext({viewport:item.viewport,
    reducedMotion:item.reducedMotion,serviceWorkers:"block"});
  const page=await context.newPage();
  const unexpected=[],runtimeErrors=[];let offsiteBeforeClick=0,githubQueries=0,allowGithub=false;
  page.on("request",request=>{
    const url=request.url();
    if(url.startsWith("https://api.github.com/")){
      githubQueries++;if(!allowGithub)offsiteBeforeClick++;return;
    }
    checkOrigin(request,unexpected);
  });
  page.on("pageerror",error=>runtimeErrors.push(error.name));
  await page.route("https://api.github.com/**",route=>route.fulfill({
    status:200,contentType:"application/json",
    headers:{"access-control-allow-origin":"*"},
    body:JSON.stringify({workflow_runs:[{
      status:"completed",conclusion:"success",event:"push",
      created_at:"2026-11-15T16:50:20Z",
      html_url:"https://github.com/CoCivium/CoAcademy/actions/runs/43737711829"
    }]})
  }));
  try{
    const resp=await page.goto(BASE+"constellation/walkaway/",{
      waitUntil:"load",timeout:30000,
    });
    assert.equal(resp?.status(),200);
    const machineResp=await context.request.get(BASE+"constellation/walkaway/status.json");
    assert.equal(machineResp.status(),200);
    const m=await machineResp.json();
    assert.equal(m.schema,"CoAll.CoWalkaway.PublicUXState.R0");
    const embedded=JSON.parse(await page.locator("#statusRecord").textContent());
    assert.deepEqual(embedded.proofs,m.proofs,"human proofs and machine proofs diverged");
    assert.deepEqual(embedded.modes,m.modes,"scenario parity failed");
    assert.equal(embedded.observed_at_utc,m.observed_at_utc);
    assert.equal(await page.locator(".proof").count(),8);
    assert.equal(await page.locator("#choices button").count(),5);
    assert.equal(githubQueries,0,"GitHub API must be opt-in");
    allowGithub=true;
    await page.locator("#refresh").click();
    await page.locator("#cloudLink").waitFor({state:"visible",timeout:6000});
    assert.equal(await page.locator("#cloudLink").isVisible(),true);
    assert.match(await page.locator("#cloudResult").textContent(),/Latest reported cloud run/);
    assert.equal(githubQueries,1,"one bounded public metadata request");
    await context.setOffline(true);
    for(const mode of m.modes){
      await page.locator('#choices button[data-id="'+mode.id+'"]').click();
      assert.equal(await page.locator("#modeName").textContent(),mode.label);
      assert.equal(await page.locator("#modeEffect").textContent(),mode.real_world_effect.replaceAll("_"," "));
      assert.equal(await page.locator('#choices button[aria-pressed="true"]').count(),1);
    }
    await page.locator('#choices button[data-id="no_human"]').focus();
    await page.keyboard.press("Enter");
    assert.equal(await page.locator("#modeName").textContent(),"Nobody answers");
    const dim=await page.evaluate(()=>({
      scrollWidth:document.documentElement.scrollWidth,
      clientWidth:document.documentElement.clientWidth,
      reducedMotion:matchMedia("(prefers-reduced-motion: reduce)").matches
    }));
    assertNoHorizontalOverflow(dim);
    assert.equal(dim.reducedMotion,item.reducedMotion==="reduce");
    assert.equal(offsiteBeforeClick,0);
    assert.deepEqual(unexpected,[]);
    assert.deepEqual(runtimeErrors,[]);
    return {view:item.name,result:"PASS",http_status:200,proofs:m.proofs.length,
      scenarios:m.modes.length,human_machine_parity:true,
      gitHub_query_only_after_click:true,github_queries:githubQueries,
      offline_scenarios:true,keyboard_selection:true,
      reduced_motion:dim.reducedMotion,horizontal_overflow:false,
      page_errors:0,external_effects:0};
  }finally{await context.close();}
}

async function checkPatterns(browser,item){
  const context=await browser.newContext({
    viewport:item.viewport,reducedMotion:item.reducedMotion,serviceWorkers:"block",
  });
  const page=await context.newPage(),unexpected=[],browserErrors=[];
  page.on("request",request=>checkOrigin(request,unexpected));
  page.on("pageerror",error=>browserErrors.push(error.name));
  try{
    const res=await page.goto(BASE+"constellation/patterns/",{waitUntil:"load",timeout:30000});
    assert.equal(res?.status(),200);
    const resp=await context.request.get(BASE+"constellation/patterns/registry.json");
    assert.equal(resp.status(),200);
    const registry=await resp.json();
    assert.equal(registry.schema,"CoAll.CoPatterna.LazyRelationalTestRegistry.R0");
    assert.equal(registry.families.length,7);
    assert.equal(registry.patterns.length,28);
    assert.equal(registry.cases.length,8);
    const embedded=JSON.parse(await page.locator("#patternSource").textContent());
    for(const key of ["patterns","cases","families","schema"])
      assert.deepEqual(embedded[key],registry[key],"source parity "+key);
    assert.equal(await page.locator(".family").count(),7);
    assert.equal(await page.locator("#caseButtons button").count(),8);
    assert.equal(await page.locator("#selectedOperators .selected-card").count(),4);
    await context.setOffline(true);
    for(const c of registry.cases){
      const button=page.locator('#caseButtons button[data-case="'+c.id+'"]');
      await button.click();
      assert.equal(await page.locator("#caseTitle").textContent(),c.title);
      const selected=await page.locator("#selectedOperators .selected-card .op").allTextContents();
      assert.deepEqual(selected,c.operators);
      assert.equal(await page.locator('#caseButtons button[aria-pressed="true"]').count(),1);
      assert.match(await page.locator("#expected").textContent(),new RegExp(c.expected_state));
    }
    await page.locator('#caseButtons button[data-case="no_delta"]').focus();
    await page.keyboard.press("Enter");
    assert.equal(await page.locator("#caseTitle").textContent(),"Nothing has changed");
    const dimensions=await page.evaluate(()=>({
      scrollWidth:document.documentElement.scrollWidth,
      clientWidth:document.documentElement.clientWidth,
      reducedMotion:matchMedia("(prefers-reduced-motion: reduce)").matches,
    }));
    assertNoHorizontalOverflow(dimensions);
    assert.equal(dimensions.reducedMotion,item.reducedMotion==="reduce");
    assert.deepEqual(unexpected,[]);
    assert.deepEqual(browserErrors,[]);
    return {view:item.name,result:"PASS",http_status:200,families:7,operators:28,
      cases:8,human_machine_parity:true,offline_case_selection:true,
      keyboard_selection:true,external_effects:0,third_party_requests:0,
      reduced_motion:dimensions.reducedMotion,horizontal_overflow:false,page_errors:0};
  }finally{await context.close();}
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
    report.tests.push({surface:"cofront", ...await checkCoFront(browser, item)});
    report.tests.push({surface:"cloudops", ...await checkCloudOps(browser, item)});
    report.tests.push({surface:"federation", ...await checkFederation(browser, item)});
    report.tests.push({surface:"walkaway", ...await checkWalkaway(browser, item)});
    report.tests.push({surface:"patterns", ...await checkPatterns(browser, item)});
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
