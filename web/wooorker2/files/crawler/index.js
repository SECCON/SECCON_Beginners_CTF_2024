const { chromium } = require('playwright');
const { v4: uuidv4 } = require("uuid");
const Redis = require("ioredis");
const connection = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
});

const ADMIN_USERNAME = process.env.ADMIN_USERNAME; 
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD; 
const APP_URL = process.env.APP_URL;

const crawl = async (path, ID) => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  try {
    // (If you set `login?next=/` as path in Report page, admin accesses `https://wooorker2.quals.beginners.seccon.jp/login?next=/` here.)
    const targetURL = APP_URL + path;
    console.log("target url:", targetURL);
    await page.goto(targetURL, {
        waitUntil: "domcontentloaded",
        timeout: 3000, 
    }); 
    await page.waitForSelector("input[id=username]");
    await page.type("input[id=username]", ADMIN_USERNAME);
    await page.type("input[id=password]", ADMIN_PASSWORD);
    await page.click("button[type=submit]");

    await page.waitForTimeout(1000);

    await page.close();
  } catch (err) {
    console.error("crawl", ID, err.message);
  } finally {
    await browser.close();
    console.log("crawl", ID, "browser closed");
  }
};

(async () => {
  while (true) {
    console.log(
      "[*] waiting new query",
      await connection.get("queued_count"),
      await connection.get("proceeded_count")
    );
    const ID = uuidv4();
    await connection
      .blpop("query", 0)
      .then((v) => {
        const path = v[1];
        console.log("crawl", ID, path);
        return crawl(path, ID);
      })
      .then(() => {
        console.log("crawl", ID, "finished");
        return connection.incr("proceeded_count");
      })
      .catch((e) => {
        console.log("crawl", ID, e);
      });
  }
})();