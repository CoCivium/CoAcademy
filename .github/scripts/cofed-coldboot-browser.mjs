// Clean-archive loopback cold boot test, explicitly not independent-provider recovery.
import assert from "node:assert/strict";
import fs from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";
import { chromium } from "playwright";

const directory=path.resolve(".ci/coldboot/restored/site");
const host="http://127.0.0.1:8765/";
const resultPath=".ci/coldboot/boot-receipt.json";
const views=[
  {name:"desktop",viewport:{width:1440,height:900},reducedMotion:"no-preference"},
  {name:"mobile-reduced-motion",viewport:{width:390,height:844},reducedMotion:"reduce"},
];
const report={schema:"CoFed.LocalColdBootBrowserReceipt.R0",
  source_commit:process.env.GITHUB_SHA||"UNBOUND",
  scope:"CLEAN_ZIP_EXTRACT_TO_LOOPBACK__HOSTED_GITHUB_RUNNER__NO_INDEPENDENT_PROVIDER",
  result:"HOLD",tests:[],network_boundary:"LOOPBACK_ONLY_THEN_OFFLINE_AFTER_LOAD",
  nonclaims:["LOOPBACK_BOOT_NE_SECOND_PROVIDER","LOADED_PAGE_SURVIVAL_NE_REMOTE_COLD_RESTORE",
   "BROWSER_TEST_NE_HUMAN_ACCEPTANCE","NO_CELL_HANDSHAKE_OR_EXACT_REMOTE_RECEIVER_ACK"]};
let server,browser;
try{
  assert.ok((await fs.stat(path.join(directory,"index.html"))).size>1000);
  server=spawn("python3",["-m","http.server","8765","--bind","127.0.0.1","--directory",directory],
    {stdio:"ignore"});
  browser=await chromium.launch({headless:true,args:["--no-sandbox"]});
  for(const item of views){
    const context=await browser.newContext({viewport:item.viewport,reducedMotion:item.reducedMotion,acceptDownloads:true,serviceWorkers:"block"});
    const page=await context.newPage();
    let blocked=0;const errors=[];
    await page.route("**/*",route=>{
      const u=route.request().url();
      if(!u.startsWith(host)){blocked++;return route.abort();}
      return route.continue();
    });
    page.on("pageerror",err=>errors.push(err.name));
    let response=null;
    for(let i=0;i<12;i++){
      try{response=await page.goto(host,{waitUntil:"load",timeout:3500});break;}
      catch(e){if(i===11)throw e;await new Promise(resolve=>setTimeout(resolve,300));}
    }
    assert.equal(response?.status(),200);
    assert.ok((await page.title()).includes("CoGibber"));
    const dims=await page.evaluate(()=>({
      width:document.documentElement.clientWidth,
      scroll:document.documentElement.scrollWidth,
      reduced:matchMedia("(prefers-reduced-motion: reduce)").matches,
    }));
    assert.ok(dims.scroll<=dims.width+2,"horizontal overflow in clean coldboot");
    assert.equal(dims.reduced,item.reducedMotion==="reduce");
    await context.setOffline(true);
    await page.locator("#exampleOne").click();
    assert.ok((await page.locator("#raw").inputValue()).includes("Review"));
    await page.locator("#convert").click();
    assert.equal(await page.locator("#results").isVisible(),true);
    const itemCount=await page.locator("#items .record").count();
    assert.ok(itemCount>=2,"no useful extracted items");
    await page.locator("#items .record input").first().fill("Review one public proof");
    const candidate=JSON.parse(await page.locator("#jsonPreview").textContent());
    assert.ok(JSON.stringify(candidate).includes("Review one public proof"),"offline edit not reflected");
    assert.ok(candidate.items.length>=2);
    assert.equal(blocked,0,"non-loopback request attempted");
    assert.deepEqual(errors,[],"browser runtime error");
    report.tests.push({
      view:item.name,result:"PASS",startup:"CLEAN_ARCHIVE_LOOPBACK",offline_after_load:true,
      candidate_items:itemCount,edited_result_reflected:true,untrusted_requests:blocked,
      reduced_motion:dims.reduced,horizontal_overflow:false,page_errors:0
    });
    await context.close();
  }
  report.result="PASS_SCOPED_LOOPBACK_COLD_BOOT_TWO_VIEWPORTS";
}catch(e){
  report.failure_class=e?.name||"Error";
  report.failure=String(e?.message||e).slice(0,420);
  process.exitCode=1;
}finally{
  if(browser)await browser.close();
  if(server)server.kill("SIGTERM");
  await fs.mkdir(path.dirname(resultPath),{recursive:true});
  await fs.writeFile(resultPath,JSON.stringify(report,null,2)+"\n");
  console.log(JSON.stringify({result:report.result,tests:report.tests.length,
    failure_class:report.failure_class||null}));
}