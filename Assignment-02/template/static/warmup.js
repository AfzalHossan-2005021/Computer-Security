/* Find the cache line size by running `getconf -a | grep CACHE` */
/**
 * Constants
 */
const LINESIZE = 64;          // Cache line size in bytes
const NUM_MEASUREMENTS = 10;  // Number of measurements to take for reliability

/**
 * Measures the median access latency when reading n cache lines.
 * 
 * @param {number} n - Number of cache lines to read
 * @return {number} Median access latency in milliseconds
 */
function readNlines(n) {
  // 1. Allocate a buffer of size n * LINESIZE.
  const bufferSize = n * LINESIZE;
  const buffer = new Uint8Array(bufferSize);

  // 2. Read each cache line (read the buffer in steps of LINESIZE) 10 times.
  const times = [];
  for (let i = 0; i < NUM_MEASUREMENTS; i++) {

    // 3. Collect total time taken in an array using `performance.now()`.
    const start = performance.now();
    for (let j = 0; j < bufferSize; j += LINESIZE) {
      buffer[j];
    }
    const end = performance.now();
    times.push(end - start);
  }

  // 4. Return the median of the time taken in milliseconds.
  times.sort((a, b) => a - b);
  const mid = Math.floor(NUM_MEASUREMENTS / 2);
  const median = (NUM_MEASUREMENTS & 1) === 0 ? (times[mid - 1] + times[mid]) / 2 : times[mid];
  return median;
}

self.addEventListener("message", function (e) {
  if (e.data === "start") {
    const results = {};

    /* Call the readNlines function for n = 1, 10, ... 10,000,000 and store the result */
    for (let n = 1; n <= 10000000; n *= 10) {
      results[n] = readNlines(n);
    }

    self.postMessage(results);
  }
});
