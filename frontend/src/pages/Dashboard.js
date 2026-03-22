import { useEffect, useState } from "react";
import api from "../api";
import "./dashboard.css";
import FilterDropdown from "./FilterDropdown";

import {
  BarChart, Bar,
  PieChart, Pie, Cell,
  LineChart, Line,
  XAxis, YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";

const COLORS = ["#e5fa24", "#fcbf56", "#40c8e0", "#a64afc", "#4863b9"];

function Dashboard() {

  const [data, setData] = useState(null);

  // ✅ changed to array (multi select)
  const [entityFilter, setEntityFilter] = useState([]);
  const [stateFilter, setStateFilter] = useState([]);
  const [statusFilter, setStatusFilter] = useState([]);

  // ✅ date filter
  const [fromDate, setFromDate] = useState("");
  const [toDate, setToDate] = useState("");

  useEffect(() => {
    api.get("/dashboard").then(res => setData(res.data));
  }, []);

  if (!data) return <p className="loading">Loading dashboard...</p>;

  // ✅ UPDATED FILTER LOGIC (safe)
  const filteredCases = data.cases.filter(c => {

    const caseDate = c.registration_date ? new Date(c.registration_date) : null;

    return (
      (entityFilter.length === 0 || entityFilter.includes(c["Entity Name"])) &&
      (stateFilter.length === 0 || stateFilter.includes(c.state)) &&
      (statusFilter.length === 0 || statusFilter.includes(c.case_status)) &&
      (!fromDate || (caseDate && caseDate >= new Date(fromDate))) &&
      (!toDate || (caseDate && caseDate <= new Date(toDate)))
    );
  });

  const kpi = {
    total: filteredCases.length,
    entities: new Set(filteredCases.map(c => c["Entity Name"])).size,
    active: filteredCases.filter(c => c.case_status === "Pending").length,
    highRisk: filteredCases.filter(c => c.litigation_risk_score >= 7).length
  };

  const groupData = (key) => {
    const map = {};
    filteredCases.forEach(c => {
      const val = c[key] || "Unknown";
      map[val] = (map[val] || 0) + 1;
    });
    return Object.entries(map).map(([k, v]) => ({ name: k, value: v }));
  };

  const statusData = groupData("case_status");
  const stateData = groupData("state");
  const courtData = groupData("court");

  const timelineMap = {};
  filteredCases.forEach(c => {
    const m = (c.registration_date || "").slice(0, 7);
    if (!m) return;
    timelineMap[m] = (timelineMap[m] || 0) + 1;
  });
  const timelineData = Object.entries(timelineMap).map(([k, v]) => ({ month: k, cases: v }));

  return (
    <div className="dashboard">

      {/* HEADER (UNCHANGED) */}
      <div className="header1">
        <div className="header1-left">
          <h1>Legal Intelligence Dashboard</h1>
        </div>
        <div className="header1-right">
          <span>Welcome, Admin</span>
        </div>
      </div>

      {/* ✅ FILTERS UPDATED ONLY */}
      <div className="filters">

        <FilterDropdown
          label="Entities"
          options={[...new Set(data.cases.map(c => c["Entity Name"]))]}
          selected={entityFilter}
          setSelected={setEntityFilter}
        />

        <FilterDropdown
          label="States"
          options={[...new Set(data.cases.map(c => c.state))]}
          selected={stateFilter}
          setSelected={setStateFilter}
        />

        <FilterDropdown
          label="Status"
          options={["Pending","Dismissed","Allowed","Disposed"]}
          selected={statusFilter}
          setSelected={setStatusFilter}
        />

        {/* DATE FILTER */}
        <div className="filter-box">
          <label>From Date</label>
          <input type="date" value={fromDate} onChange={(e)=>setFromDate(e.target.value)} />
        </div>

        <div className="filter-box">
          <label>To Date</label>
          <input type="date" value={toDate} onChange={(e)=>setToDate(e.target.value)} />
        </div>

      </div>

      {/* EVERYTHING BELOW SAME */}

      <div className="kpi-grid">
        {[{ label: "Total Cases", value: kpi.total },
          { label: "Entities", value: kpi.entities },
          { label: "Active", value: kpi.active },
          { label: "High Risk", value: kpi.highRisk }
        ].map((item, i) => (
          <div className="card" key={i}>
            <p>{item.label}</p>
            <h2>{item.value}</h2>
          </div>
        ))}
      </div>

      <div className="charts">
        <div className="chart">
          <h3>Case Status</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={statusData} dataKey="value">
                {statusData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="chart">
          <h3>Cases by State</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={stateData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#018c91" radius={[6,6,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="charts">
        <div className="chart">
          <h3>Cases by Court</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={courtData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#186460" radius={[6,6,0,0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart">
          <h3>Timeline</h3>
          <ResponsiveContainer width="90%" height={300}>
            <LineChart data={timelineData}>
              <CartesianGrid strokeDasharray="1 1" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="cases" stroke="rgb(106, 117, 0)" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <h2 className="table-title">Case Details</h2>

      <div className="table-wrapper">
        <table className="cases-table">
          <thead>
            <tr>
              <th>Case</th>
              <th>Entity</th>
              <th>Court</th>
              <th>State</th>
              <th>Status</th>
              <th>Risk</th>
            </tr>
          </thead>
          <tbody>
            {filteredCases.map((c, i) => (
              <tr key={i}>
                <td>{c.case_number}</td>
                <td>{c["Entity Name"]}</td>
                <td>{c.court}</td>
                <td>{c.state}</td>
                <td>{c.case_status}</td>
                <td className={c.litigation_risk_score >= 7 ? "risk-high" : "risk-low"}>
                  {c.litigation_risk_score}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

    </div>
  );
}

export default Dashboard;