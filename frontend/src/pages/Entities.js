import { useState } from "react";

function Entities() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState("");

  const runScraper = async () => {
    setLoading(true);
    setLogs(["Starting scraper..."]);
    setStatus("");

    try {
      const res = await fetch("http://127.0.0.1:8000/run-scraper");
      const data = await res.json();

      // show logs
      setLogs(data.logs || []);

      // show status
      if (data.status === "success") {
        setStatus(`✅ Success | Records: ${data.records}`);
      } else {
        setStatus(`❌ Failed: ${data.error}`);
      }

    } catch (err) {
      setStatus("❌ Error: " + err.message);
    }

    setLoading(false);
  };

  return (
    <div>
      <h1>Entities</h1>

      <button onClick={runScraper} disabled={loading}>
        {loading ? "Running..." : "Run Scraper"}
      </button>

      {/* STATUS */}
      <h3 style={{ marginTop: "20px" }}>{status}</h3>

      {/* LOGS */}
      <div
        style={{
          marginTop: "10px",
          background: "#000",
          color: "#0f0",
          padding: "10px",
          height: "300px",
          overflowY: "auto",
          fontFamily: "monospace"
        }}
      >
        {logs.map((log, i) => (
          <div key={i}>▶ {log}</div>
        ))}
      </div>
    </div>
  );
}

export default Entities;
