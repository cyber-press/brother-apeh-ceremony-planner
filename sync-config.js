// v3.5.0 shared-master synchronization configuration.
// Local development uses the FastAPI server at 127.0.0.1:8000.
// After deploying the backend, replace apiBaseUrl with its HTTPS URL.
window.PLANNER_SYNC_CONFIG = Object.freeze({
  enabled: true,
  apiBaseUrl: "http://127.0.0.1:8000",
  plannerId: "brother-apeh-master"
});
