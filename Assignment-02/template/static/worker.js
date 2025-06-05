/* Find the cache line size by running `getconf -a | grep CACHE` */
const LINESIZE = 64;
/* Find the L3 size by running `getconf -a | grep CACHE` */
const LLCSIZE = 12 * 1024 * 1024;
/* Collect traces for 10 seconds; you can vary this */
const TIME = 10000;
/* Collect traces every 10ms; you can vary this */
const P = 10;


/*
 * Implement this function to run a sweep of the cache.
 *
 * @param {number} P - The time period in milliseconds for each sweep.
 * @return {Array<number>} An array of counts for each cache line read in the time period.
 * 
 * 1. Allocate a buffer of size LLCSIZE.
 * 2. Read each cache line (read the buffer in steps of LINESIZE).
 * 3. Count the number of times each cache line is read in a time period of P milliseconds.
 * 4. Store the count in an array of size K, where K = TIME / P.
 * 5. Return the array of swap counts.
 */
function sweep(P) {
    const bufferSize = LLCSIZE;
    const buffer = new Uint8Array(bufferSize);

    const K = TIME / P;
    const swapCounts = new Array(K).fill(0);

    for (let read = 0; read < K; read++) {
        const startTime = performance.now();
        while (performance.now() - startTime < P) {
            for (let index = 0; index < bufferSize; index += LINESIZE) {
                buffer[index];
            }
            swapCounts[read]++;
        }
    }

    return swapCounts;
}   

/* 
 * Event listener for the worker to start measuring sweep counts.
 *
 * 1. Call the sweep function and return the result
 */
self.addEventListener('message', function(e) {
    if (e.data === 'start') {
        try {
            const results = sweep(P);
            self.postMessage(results);
        } catch (err) {
            console.error('Error during sweep:', err);
        }
    }
});