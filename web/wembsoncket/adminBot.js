// puppeteerUtils.js
const puppeteer = require('puppeteer');
const jwt = require('jsonwebtoken');
const fs = require('fs');

// Secret key for signing JWT
const JWT_SECRET = fs.readFileSync('secret.txt', 'utf8').trim()

// Admin cookie for authentication
const adminCookie = jwt.sign({ userId: 'admin' }, JWT_SECRET);

// Function to visit a URL using Puppeteer
const visitUrl = async (url) => {
  // console.log('Visiting URL:', url);

  let browser;

  try {
    browser = await puppeteer.launch({
      headless: "new",
      pipe: true,
      dumpio: true,
      args: [
        '--no-sandbox',
        '--disable-gpu',
        '--disable-software-rasterizer',
        '--disable-dev-shm-usage',
        '--disable-setuid-sandbox',
        '--js-flags=--noexpose_wasm,--jitless',
      ]
    });

    // console.log('Opening page');
    const page = await browser.newPage();

    try {
      await page.setUserAgent('puppeteer');
      let cookies = [{
        name: 'token',
        value: adminCookie,
        domain: 'wembsoncket.chal.cyberjousting.com',
        httpOnly: true,
        sameSite: 'None',
        secure: true
      }];
      // console.log('Setting cookies:', cookies);
      await page.setCookie(...cookies);

      let statusCode = null;
      page.on('response', (response) => {
        if (response.url() === url) {
          statusCode = response.status();
        }
      });

      // console.log('Navigating to the URL');
      const response = await page.goto(url, { timeout: 10000, waitUntil: 'networkidle2' });

      if (!statusCode && response) {
        statusCode = response.status();
      }

      // console.log('Waiting for page content');
      await page.waitForSelector('body');

      if (statusCode === 200) {
        return 'success';
      } else if (statusCode) {
        return `Unexpected status code ${statusCode}`;
      } else {
        return 'No status code captured';
      }

    } catch (error) {
      console.error('Error navigating to page:', error.message);
      return `Navigation failed - ${error.message}`;
    } finally {
      // console.log('Closing page');
      await page.close();
    }

  } catch (error) {
    console.error('Error launching browser:', error.message);
    return `Browser launch failed - ${error.message}`;
  } finally {
    if (browser) {
      // console.log('Closing browser');
      await browser.close();
    }
  }
};

module.exports = { visitUrl };