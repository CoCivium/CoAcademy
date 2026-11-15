// CoFed cold-start R1: no server, no previous page load, no network.
 // Source-only first-use acceptance. The GitHub runner is NOT an independent second provider.
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { chromium } from "playwright";

const root = path.resolve(".ci/coldboot/restored/site");
const entry = pathToFileURL(path.join(root,"index.html")).href;
const target = ".ci/coldboot/zero-network-receipt.json";
const views = [
  {name:"desktop",viewport:{width:1440,height:900},reducedMotion:"no-preference"},
  {name:"mobile-reduced-motion",viewport:{width:390,height:844},reducedMotion:"reduce"},
];
const receipt = {
  schema:"CoFed.ZeroNetworkColdStart.R1",
  source_commit:process.env.GITHUB_SHA||"UNBOUND",
  result:"HOLD",
  scope:"GITHUB_HOSTED_CHROMIUM__FILE_URL_FROM_CLEAN_ARCHIVE__OFFLINE_BEFORE_NAVIGATION",
  page_loaded_before_offline:false,
  network_needed_for_first_task:false,
  producer_is_independent_second_host:false,
  tests:[],
  nonclaims:[
    "BROWSER_FILE_COLD_START_NE_INDEPENDENT_PROVIDER",
    "SAME_RUNNER_TEST_NE_EXTERNAL_RECEIVER_ACK",
    "LOCAL_FILE_URL_NE_HTTPS_ORIGIN",
    "OFFLINE_TEST_NE_HUMAN_ACCEPTANCE",
    "NO_CIV2_COEX_CANON_OR_RUNTIME"
  ]
};
let browser;
try{
  assert.ok((await fs.stat(path.join(root,"index.html"))).size>1000);
  const desc = JSON.parse(await fs.readFile(path.join(root,"discovery.json"),"utf8"));
  assert.equal(desc.schema,"CoGibber.PublicDiscovery.R0");
  assert.equal(desc.implementation.model_calls,false);
  browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  for(const view of views){
    const context=await browser.newContext({
      viewport:view.viewport,reducedMotion:view.reducedMotion,
      acceptDownloads:true,serviceWorkers:"block"
    });
    let blockedHttp=0;
    await context.route(/^https?:\/\//,async route=>{
      blockedHttp++;
      await route.abort("internetdisconnected");
    });
    await context.setOffline(true); // BEFORE first navigation, not after.
    const page=await context.newPage();
    const errors=[];
    page.on("pageerror",err=>errors.push(err.name));
    const response=await page.goto(entry,{waitUntil:"load",timeout:15000});
    assert.ok(response===null || response.status()===200,"local file failed to load");
    assert.match(await page.title(),/CoGibber/);
    const dims=await page.evaluate(()=>({
      protocol:location.protocol,
      browserOnline:navigator.onLine,
      width:document.documentElement.clientWidth,
      scroll:document.documentElement.scrollWidth,
      reduced:matchMedia("(prefers-reduced-motion: reduce)").matches
    }));
    assert.equal(dims.protocol,"file:");
    assert.equal(dims.browserOnline,false);
    assert.equal(dims.reduced,view.reducedMotion==="reduce");
    assert.ok(dims.scroll<=dims.width+2,"horizontal overflow");
    await page.locator("#raw").fill("Review the source by Friday; is the note accurate? Maybe ask for evidence first.");
    await page.locator("#convert").focus();
    await page.keyboard.press("Enter");
    assert.equal(await page.locator("#results").isVisible(),true);
    const count=await page.locator("#items .record").count();
    assert.ok(count>=3,"candidate extraction unavailable");
    await page.locator("#items .record input").first().fill("Review the independently verified source");
    const obj=JSON.parse(await page.locator("#jsonPreview").textContent());
    assert.equal(obj.schema,"CoGibber.LocalNotePlan.R0");
    assert.equal(obj.items[0].text,"Review the independently verified source");
    assert.equal(obj.items.length,count);
    const downloadPromise=page.waitForEvent("download");
    await page.locator("#downloadJson").click();
    const download=await downloadPromise;
    assert.equal(download.suggestedFilename(),"cogibber-note-r0.json");
    const exported=JSON.parse(await fs.readFile(await download.path(),"utf8"));
    assert.deepEqual(exported,obj,"export != visible edited JSON");
    assert.equal(blockedHttp,0,"page attempted unexpected network access");
    assert.deepEqual(errors,[],"uncaught browser errors");
    receipt.tests.push({
      viewport:view.name,result:"PASS",entry_protocol:dims.protocol,
      browser_network_off_before_navigation:true,source_schema:desc.schema,
      candidate_items:count,edited_export_parity:true,download_verified:true,
      horizontal_overflow:false,reduced_motion:dims.reduced,
      unexpected_http_requests:blockedHttp,browser_errors:errors.length
    });
    await context.close();
  }
  receipt.result="PASS_NO_NETWORK_BEFORE_COLD_START_TWO_VIEWPORTS";
} catch(err){
  receipt.failure_class=err?.name||"Error";
  receipt.failure=String(err?.message||err).slice(0,480);
  process.exitCode=1;
} finally{
  if(browser)await browser.close();
  await fs.mkdir(path.dirname(target),{recursive:true});
  await fs.writeFile(target,JSON.stringify(receipt,null,2)+"\n","utf8");
  console.log(JSON.stringify({
    schema:receipt.schema,result:receipt.result,
    views:receipt.tests.length,
    failure_class:receipt.failure_class||null
  }));
}
