function app() {
  return {
    /* This is the main app object containing all the application state and methods. */
    // The following properties are used to store the state of the application

    // results of cache latency measurements
    latencyResults: null,
    // local collection of trace data
    traceData: [],
    // Local collection of heapmap images
    heatmaps: [],

    // Current status message
    status: "",
    // Is any worker running?
    isCollecting: false,
    // Is the status message an error?
    statusIsError: false,
    // Show trace data in the UI?
    showingTraces: false,

    // Collect latency data using warmup.js worker
    async collectLatencyData() {
      this.isCollecting = true;
      this.status = "Collecting latency data...";
      this.latencyResults = null;
      this.statusIsError = false;
      this.showingTraces = false;

      try {
        // Create a worker
        let worker = new Worker("warmup.js");

        // Start the measurement and wait for result
        const results = await new Promise((resolve) => {
          worker.onmessage = (e) => resolve(e.data);
          worker.postMessage("start");
        });

        // Update results
        this.latencyResults = results;
        this.status = "Latency data collection complete!";

        // Terminate worker
        worker.terminate();
      } catch (error) {
        console.error("Error collecting latency data:", error);
        this.status = `Error: ${error.message}`;
        this.statusIsError = true;
      } finally {
        this.isCollecting = false;
      }
    },

    /* 
     * Collect trace data using worker.js and send to backend
    
     * 1. Create a worker to run the sweep function.
     * 2. Collect the trace data from the worker.
     * 3. Send the trace data to the backend for temporary storage and heatmap generation.
     * 4. Fetch the heatmap from the backend and add it to the local collection.
     * 5. Handle errors and update the status.
     */
    async collectTraceData() {
      this.status = "Collecting trace data...";
      this.isCollecting = true;
      this.statusIsError = false;
      this.showingTraces = true;

      try {
        // Create a worker
        let worker = new Worker("worker.js");

        // Start the measurement and wait for result
        const results = await new Promise((resolve) => {
          worker.onmessage = (e) => resolve(e.data);
          worker.postMessage("start");
        });

        // Update results
        this.traceData.push(results);
        this.status = "Collecting trace complete, sending to server...";

        // Send data to the backend
        const response = await fetch('/collect_trace', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 'trace_data': results }),
        });

        if (!response.ok) {
          throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        // Add the new heatmap to the collection
        if (data.image) {
          this.heatmaps.push(data);
          this.status = "Trace data collected and visualized using matplotlib.";
        }

        // Terminate worker
        worker.terminate();
      } catch (error) {
        console.error("Error collecting trace data:", error);
        this.status = `Error: ${error.message}`;
        this.statusIsError = true;
      } finally {
        this.isCollecting = false;
      }
    },

    /* 
     * Download the trace data as JSON (array of arrays format for ML)
     *
     * 1. Fetch the latest data from the backend API.
     * 2. Create a download file with the trace data in JSON format.
     * 3. Handle errors and update the status.
     */
    async downloadTraces() {
      try {
        this.status = "Preparing download...";
        this.statusIsError = false;
        // Use the current trace data in memory
        if (!this.traceData || this.traceData.length === 0) {
          this.status = "No trace data available to download!";
          setTimeout(() => { this.status = ""; }, 2000);
          return;
        }
        // Create a JSON blob
        const jsonData = JSON.stringify(this.traceData);
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        // Create a download link
        const a = document.createElement('a');
        a.href = url;
        a.download = `dataset.json`;
        document.body.appendChild(a);
        a.click();
        // Clean up
        setTimeout(() => {
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
          this.status = "Download complete!";
          setTimeout(() => { this.status = ""; }, 2000);
        }, 100);
      } catch (error) {
        console.error("Error downloading traces:", error);
        this.status = `Error: ${error.message}`;
        this.statusIsError = true;
      }
    },

    /* 
     * Clear all results from the server
     *
     * 1. Send a request to the backend API to clear all results.
     * 2. Clear local copies of trace data and heatmaps.
     * 3. Handle errors and update the status.
     */
    async clearResults() {
      try {
        this.status = "Clearing results...";
        this.statusIsError = false;
        // Call the API to clear server-side data
        const response = await fetch('/api/clear_results', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        });
        if (!response.ok) {
          throw new Error(`Server returned ${response.status}: ${response.statusText}`);
        }
        // Clear local data
        this.traceData = [];
        this.heatmaps = [];
        this.latencyResults = null;
        this.showingTraces = false;
        this.status = "All results cleared!";
        setTimeout(() => { this.status = ""; }, 2000);
      } catch (error) {
        console.error("Error clearing results:", error);
        this.status = `Error: ${error.message}`;
        this.statusIsError = true;
      }
    },
  };
}
