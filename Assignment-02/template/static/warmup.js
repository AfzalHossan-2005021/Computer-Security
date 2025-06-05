/* Find the cache line size by running `getconf -a | grep CACHE` */
const LINESIZE = 64;          // Cache line size in bytes
const NUM_MEASUREMENTS = 10;  // Number of measurements to take for reliability

/*
 * Measures the median access latency when reading n cache lines.
 * 
 * @param {number} n - Number of cache lines to read
 * @return {number} Median access latency in milliseconds
 * 
 * 1. Allocate a buffer of size n * LINESIZE.
 * 2. Read each cache line (read the buffer in steps of LINESIZE) 10 times.
 * 3. Collect total time taken in an array using `performance.now()`.
 * 4. Return the median of the time taken in milliseconds.
 */
function readNlines(n) {
  const bufferSize = n * LINESIZE;
  const buffer = new Uint8Array(bufferSize);

  const times = [];
  for (let read = 0; read < NUM_MEASUREMENTS; read++) {
    const start = performance.now();
    for (let index = 0; index < bufferSize; index += LINESIZE) {
      buffer[index];
    }
    const end = performance.now();
    times.push(end - start);
  }

  times.sort((a, b) => a - b);
  const mid = Math.floor(NUM_MEASUREMENTS / 2);
  const median = (NUM_MEASUREMENTS & 1) === 0 ? (times[mid - 1] + times[mid]) / 2 : times[mid];
  return median;
}

/*
 * Event listener for the worker to start measuring cache line access latencies.
 * 
 * 1. Call the readNlines(n) function in the worker thread with n = 1, 10, . . . 10,000,000
 * 2. Store the results in an object with n as the key and the median access latency as the value.
 * 3. If for some value of n the function fails, just break the loop.
 * 4. Return the results to the main thread.
 */
self.addEventListener("message", function (e) {
  if (e.data === "start") {
    const results = {};

    for (let n = 1; n <= 10000000; n *= 10) {
      try {
        results[n] = readNlines(n);
      } catch (err) {
        console.error(`Error when measuring with n=${n}:`, err);
        break;
      }
    }

    self.postMessage(results);
  }
});
