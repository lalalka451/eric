import fs from "fs";
import path from "path";
import puppeteer from "puppeteer-extra";
import StealthPlugin from "puppeteer-extra-plugin-stealth";
import dotenv from "dotenv";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

// Add Stealth plugin to puppeteer
puppeteer.use(StealthPlugin());

async function visit4chan() {
  const browserOptions = {
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--proxy-server=127.0.0.1:10809"],
    headless: false, // Set to false to show the browser window
  };

  const browser = await puppeteer.launch(browserOptions);
  const page = await browser.newPage();

  try {
    // Navigate to 4chan /a/ board
    await page.goto('https://www.facebook.com/groups/592850912909945/', { waitUntil: 'networkidle0' });
    console.log('Successfully loaded 4chan /a/ board');

    // Example: Get the title of the page
    const title = await page.title();
    console.log('Page title:', title);

    // Example: Count the number of threads on the page
    const threadCount = await page.$$eval('.thread', threads => threads.length);
    console.log('Number of threads:', threadCount);

    // Keep the browser window open
    await new Promise(resolve => {}); // This will keep the script running indefinitely
  } catch (error) {
    console.error('An error occurred:', error);
  }
  // Remove the 'finally' block to prevent automatic browser closure
}

visit4chan();