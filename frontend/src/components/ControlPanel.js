import React from "react";
import api from "../api";

function ControlPanel({ reloadCases }) {

  const runClean = async () => {
    await api.post("/run-clean");
    alert("Data cleaned");
  };

  const runCompare = async () => {
    await api.post("/run-compare");
    alert("Entity matching completed");
    reloadCases();
  };

  const runAlert = async () => {
    await api.post("/run-alert");
    alert("Alerts sent");
  };

  const runPipeline = async () => {
    await api.post("/run-pipeline");
    alert("Pipeline completed");
    reloadCases();
  };

  return (
    <div className="controls">

      <button onClick={runClean}>Clean Data</button>

      <button onClick={runCompare}>Match Entities</button>

      <button onClick={runAlert}>Send Alerts</button>

      <button onClick={runPipeline}>Run Full Pipeline</button>

    </div>
  );
}

export default ControlPanel;