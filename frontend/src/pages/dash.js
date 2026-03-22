// // // import {useEffect,useState} from "react";
// // // import api from "../api";

// // // import {
// // // BarChart,Bar,
// // // PieChart,Pie,Cell,
// // // XAxis,YAxis,Tooltip,
// // // ResponsiveContainer,
// // // LineChart,Line
// // // } from "recharts";

// // // function Dashboard(){

// // // const [data,setData] = useState(null);

// // // const loadData = async()=>{

// // // const res = await api.get("/dashboard");

// // // setData(res.data);

// // // };

// // // useEffect(()=>{

// // // loadData();

// // // },[]);

// // // if(!data) return <p>Loading dashboard...</p>;

// // // /* KPI */

// // // const kpi = data.kpi;

// // // /* Charts */
// // // const [entityFilter,setEntityFilter] = useState("");
// // // const [stateFilter,setStateFilter] = useState("");
// // // const [statusFilter,setStatusFilter] = useState("");

// // // const statusData = Object.entries(data.case_status).map(([k,v])=>({
// // // name:k,
// // // value:v
// // // }));

// // // const stateData = Object.entries(data.state).map(([k,v])=>({
// // // name:k,
// // // cases:v
// // // }));

// // // const courtData = Object.entries(data.court).map(([k,v])=>({
// // // name:k,
// // // cases:v
// // // }));

// // // const timelineData = Object.entries(data.timeline).map(([k,v])=>({
// // // month:k,
// // // cases:v
// // // }));

// // // const filteredCases = data.cases.filter(c =>

// // // (!entityFilter || c["Entity Name"]===entityFilter) &&
// // // (!stateFilter || c.state===stateFilter) &&
// // // (!statusFilter || c.case_status===statusFilter)

// // // );

// // // return(

// // // <div>

// // // <h1>Legal Intelligence Dashboard</h1>

// // // {/* KPI CARDS */}

// // // <div className="kpi-grid">

// // // <div className="card">

// // // <h3>Total Cases</h3>
// // // <h2>{kpi.total_cases}</h2>

// // // </div>

// // // <div className="card">

// // // <h3>Entities Monitored</h3>
// // // <h2>{kpi.entities}</h2>

// // // </div>

// // // <div className="card">

// // // <h3>Active Cases</h3>
// // // <h2>{kpi.active_cases}</h2>

// // // </div>

// // // <div className="card">

// // // <h3>High Risk Cases</h3>
// // // <h2>{kpi.high_risk}</h2>

// // // </div>

// // // </div>

// // // {/* CHARTS */}

// // // <div className="charts">

// // // <div className="chart">

// // // <h3>Case Status</h3>

// // // <ResponsiveContainer width="100%" height={300}>

// // // <PieChart>

// // // <Pie data={statusData} dataKey="value" nameKey="name" />

// // // <Tooltip/>

// // // </PieChart>

// // // </ResponsiveContainer>

// // // </div>

// // // <div className="chart">

// // // <h3>Cases by State</h3>

// // // <ResponsiveContainer width="100%" height={300}>

// // // <BarChart data={stateData}>

// // // <XAxis dataKey="name"/>
// // // <YAxis/>
// // // <Tooltip/>

// // // <Bar dataKey="cases"/>

// // // </BarChart>

// // // </ResponsiveContainer>

// // // </div>

// // // </div>

// // // <div className="charts">

// // // <div className="chart">

// // // <h3>Cases by Court</h3>

// // // <ResponsiveContainer width="100%" height={300}>

// // // <BarChart data={courtData}>

// // // <XAxis dataKey="name"/>
// // // <YAxis/>
// // // <Tooltip/>

// // // <Bar dataKey="cases"/>

// // // </BarChart>

// // // </ResponsiveContainer>

// // // </div>

// // // <div className="chart">

// // // <h3>Litigation Timeline</h3>

// // // <ResponsiveContainer width="100%" height={300}>

// // // <LineChart data={timelineData}>

// // // <XAxis dataKey="month"/>
// // // <YAxis/>
// // // <Tooltip/>

// // // <Line type="monotone" dataKey="cases"/>

// // // </LineChart>

// // // </ResponsiveContainer>

// // // </div>

// // // </div>

// // // </div>

// // // );

// // // }

// // // export default Dashboard;

































// // import {useEffect,useState} from "react";
// // import api from "../api";

// // import {
// // BarChart,Bar,
// // PieChart,Pie,
// // LineChart,Line,
// // XAxis,YAxis,
// // Tooltip,
// // ResponsiveContainer
// // } from "recharts";

// // function Dashboard(){

// // const [data,setData] = useState(null);

// // const [entityFilter,setEntityFilter] = useState("");
// // const [stateFilter,setStateFilter] = useState("");
// // const [statusFilter,setStatusFilter] = useState("");

// // const loadData = async()=>{

// // const res = await api.get("/dashboard");

// // setData(res.data);

// // };

// // useEffect(()=>{

// // loadData();

// // },[]);

// // if(!data) return <p>Loading dashboard...</p>;

// // const kpi = data.kpi;

// // /* Convert objects to chart arrays */

// // const statusData = Object.entries(data.case_status).map(([k,v])=>({
// // name:k,
// // value:v
// // }));

// // const stateData = Object.entries(data.state).map(([k,v])=>({
// // name:k,
// // cases:v
// // }));

// // const courtData = Object.entries(data.court).map(([k,v])=>({
// // name:k,
// // cases:v
// // }));

// // const timelineData = Object.entries(data.timeline).map(([k,v])=>({
// // month:k,
// // cases:v
// // }));

// // /* Filters */

// // const filteredCases = data.cases.filter(c =>

// // (!entityFilter || c["Entity Name"]===entityFilter) &&
// // (!stateFilter || c.state===stateFilter) &&
// // (!statusFilter || c.case_status===statusFilter)

// // );

// // return(

// // <div>

// // <h1>Legal Intelligence Dashboard</h1>

// // {/* FILTERS */}

// // <div className="filters">

// // <select onChange={(e)=>setEntityFilter(e.target.value)}>

// // <option value="">All Entities</option>

// // {[...new Set(data.cases.map(c=>c["Entity Name"]))].map(e=>(

// // <option key={e}>{e}</option>

// // ))}

// // </select>

// // <select onChange={(e)=>setStateFilter(e.target.value)}>

// // <option value="">All States</option>

// // {[...new Set(data.cases.map(c=>c.state))].map(s=>(

// // <option key={s}>{s}</option>

// // ))}

// // </select>

// // <select onChange={(e)=>setStatusFilter(e.target.value)}>

// // <option value="">All Status</option>

// // <option>Pending</option>
// // <option>Dismissed</option>
// // <option>Allowed</option>
// // <option>Disposed</option>

// // </select>

// // </div>

// // {/* KPI CARDS */}

// // <div className="kpi-grid">

// // <div className="card">

// // <h3>Total Cases</h3>
// // <h2>{kpi.total_cases}</h2>

// // </div>

// // <div className="card">

// // <h3>Entities</h3>
// // <h2>{kpi.entities}</h2>

// // </div>

// // <div className="card">

// // <h3>Active Cases</h3>
// // <h2>{kpi.active_cases}</h2>

// // </div>

// // <div className="card">

// // <h3>High Risk</h3>
// // <h2>{kpi.high_risk}</h2>

// // </div>

// // </div>

// // {/* CHART ROW 1 */}

// // <div className="charts">

// // <div className="chart">

// // <h3>Case Status</h3>

// // <ResponsiveContainer width="100%" height={300}>

// // <PieChart>

// // <Pie data={statusData} dataKey="value" nameKey="name"/>

// // <Tooltip/>

// // </PieChart>

// // </ResponsiveContainer>

// // </div>

// // <div className="chart">

// // <h3>Cases by State</h3>

// // <ResponsiveContainer width="100%" height={300}>

// // <BarChart data={stateData}>

// // <XAxis dataKey="name"/>
// // <YAxis/>
// // <Tooltip/>

// // <Bar dataKey="cases"/>

// // </BarChart>

// // </ResponsiveContainer>

// // </div>

// // </div>

// // {/* CHART ROW 2 */}

// // <div className="charts">

// // <div className="chart">

// // <h3>Cases by Court</h3>

// // <ResponsiveContainer width="100%" height={300}>

// // <BarChart data={courtData}>

// // <XAxis dataKey="name"/>
// // <YAxis/>
// // <Tooltip/>

// // <Bar dataKey="cases"/>

// // </BarChart>

// // </ResponsiveContainer>

// // </div>

// // <div className="chart">

// // <h3>Litigation Timeline</h3>

// // <ResponsiveContainer width="100%" height={300}>

// // <LineChart data={timelineData}>

// // <XAxis dataKey="month"/>
// // <YAxis/>
// // <Tooltip/>

// // <Line type="monotone" dataKey="cases"/>

// // </LineChart>

// // </ResponsiveContainer>

// // </div>

// // </div>

// // {/* CASE TABLE */}

// // <h2>Case Details</h2>

// // <table className="cases-table">

// // <thead>

// // <tr>

// // <th>Entity</th>
// // <th>Case Number</th>
// // <th>Court</th>
// // <th>Judge</th>
// // <th>State</th>
// // <th>Status</th>
// // <th>Risk</th>
// // <th>Registration Date</th>

// // </tr>

// // </thead>

// // <tbody>

// // {filteredCases.map((c,i)=>(

// // <tr key={i}>

// // <td>{c["Entity Name"]}</td>
// // <td>{c.case_number}</td>
// // <td>{c.court}</td>
// // <td>{c.judge}</td>
// // <td>{c.state}</td>
// // <td>{c.case_status}</td>
// // <td>{c.litigation_risk_score}</td>
// // <td>{c.registration_date}</td>

// // </tr>

// // ))}

// // </tbody>

// // </table>

// // </div>

// // );

// // }

// // export default Dashboard;












// import {useEffect,useState} from "react";
// import api from "../api";

// import {
// BarChart,Bar,
// PieChart,Pie,
// LineChart,Line,
// XAxis,YAxis,
// Tooltip,
// ResponsiveContainer
// } from "recharts";

// function Dashboard(){

// const [data,setData] = useState(null);

// const [entityFilter,setEntityFilter] = useState("");
// const [stateFilter,setStateFilter] = useState("");
// const [statusFilter,setStatusFilter] = useState("");

// const loadData = async()=>{

// const res = await api.get("/dashboard");

// setData(res.data);

// };

// useEffect(()=>{

// loadData();

// },[]);

// if(!data) return <p>Loading dashboard...</p>;



// /* ===========================
// FILTER DATASET
// =========================== */

// const filteredCases = data.cases.filter(c =>

// (!entityFilter || c["Entity Name"]===entityFilter) &&
// (!stateFilter || c.state===stateFilter) &&
// (!statusFilter || c.case_status===statusFilter)

// );



// /* ===========================
// KPI CALCULATION
// =========================== */

// const kpi = {

// total_cases: filteredCases.length,

// entities: new Set(filteredCases.map(c=>c["Entity Name"])).size,

// active_cases: filteredCases.filter(c=>c.case_status==="Pending").length,

// high_risk: filteredCases.filter(c=>c.litigation_risk_score>=7).length

// };



// /* ===========================
// CASE STATUS CHART
// =========================== */

// const statusCount = {};

// filteredCases.forEach(c=>{

// const s = c.case_status || "Unknown";

// statusCount[s] = (statusCount[s] || 0) + 1;

// });

// const statusData = Object.entries(statusCount).map(([k,v])=>({
// name:k,
// value:v
// }));



// /* ===========================
// STATE CHART
// =========================== */

// const stateCount = {};

// filteredCases.forEach(c=>{

// const s = c.state || "Unknown";

// stateCount[s] = (stateCount[s] || 0) + 1;

// });

// const stateData = Object.entries(stateCount).map(([k,v])=>({
// name:k,
// cases:v
// }));



// /* ===========================
// COURT CHART
// =========================== */

// const courtCount = {};

// filteredCases.forEach(c=>{

// const s = c.court || "Unknown";

// courtCount[s] = (courtCount[s] || 0) + 1;

// });

// const courtData = Object.entries(courtCount).map(([k,v])=>({
// name:k,
// cases:v
// }));



// /* ===========================
// TIMELINE CHART
// =========================== */

// const timelineCount = {};

// filteredCases.forEach(c=>{

// const month = (c.registration_date || "").substring(0,7);

// if(!month) return;

// timelineCount[month] = (timelineCount[month] || 0) + 1;

// });

// const timelineData = Object.entries(timelineCount).map(([k,v])=>({
// month:k,
// cases:v
// }));



// return(

// <div>

// <h1>Legal Intelligence Dashboard</h1>



// {/* ===========================
// FILTERS
// =========================== */}

// <div className="filters">

// <select onChange={(e)=>setEntityFilter(e.target.value)}>

// <option value="">All Entities</option>

// {[...new Set(data.cases.map(c=>c["Entity Name"]))].map(e=>(

// <option key={e}>{e}</option>

// ))}

// </select>

// <select onChange={(e)=>setStateFilter(e.target.value)}>

// <option value="">All States</option>

// {[...new Set(data.cases.map(c=>c.state))].map(s=>(

// <option key={s}>{s}</option>

// ))}

// </select>

// <select onChange={(e)=>setStatusFilter(e.target.value)}>

// <option value="">All Status</option>

// <option>Pending</option>
// <option>Dismissed</option>
// <option>Allowed</option>
// <option>Disposed</option>

// </select>

// </div>



// {/* ===========================
// KPI CARDS
// =========================== */}

// <div className="kpi-grid">

// <div className="card">

// <h3>Total Cases</h3>
// <h2>{kpi.total_cases}</h2>

// </div>

// <div className="card">

// <h3>Entities</h3>
// <h2>{kpi.entities}</h2>

// </div>

// <div className="card">

// <h3>Active Cases</h3>
// <h2>{kpi.active_cases}</h2>

// </div>

// <div className="card">

// <h3>High Risk</h3>
// <h2>{kpi.high_risk}</h2>

// </div>

// </div>



// {/* ===========================
// CHART ROW 1
// =========================== */}

// <div className="charts">

// <div className="chart">

// <h3>Case Status</h3>

// <ResponsiveContainer width="100%" height={300}>

// <PieChart>

// <Pie data={statusData} dataKey="value" nameKey="name"/>

// <Tooltip/>

// </PieChart>

// </ResponsiveContainer>

// </div>

// <div className="chart">

// <h3>Cases by State</h3>

// <ResponsiveContainer width="100%" height={300}>

// <BarChart data={stateData}>

// <XAxis dataKey="name"/>
// <YAxis/>
// <Tooltip/>

// <Bar dataKey="cases"/>

// </BarChart>

// </ResponsiveContainer>

// </div>

// </div>



// {/* ===========================
// CHART ROW 2
// =========================== */}

// <div className="charts">

// <div className="chart">

// <h3>Cases by Court</h3>

// <ResponsiveContainer width="100%" height={300}>

// <BarChart data={courtData}>

// <XAxis dataKey="name"/>
// <YAxis/>
// <Tooltip/>

// <Bar dataKey="cases"/>

// </BarChart>

// </ResponsiveContainer>

// </div>

// <div className="chart">

// <h3>Litigation Timeline</h3>

// <ResponsiveContainer width="100%" height={300}>

// <LineChart data={timelineData}>

// <XAxis dataKey="month"/>
// <YAxis/>
// <Tooltip/>

// <Line type="monotone" dataKey="cases"/>

// </LineChart>

// </ResponsiveContainer>

// </div>

// </div>



// {/* ===========================
// CASE TABLE
// =========================== */}

// <h2>Case Details</h2>

// <table className="cases-table">

// <thead>

// <tr>

// <th>Entity</th>
// <th>Case Number</th>
// <th>Court</th>
// <th>Judge</th>
// <th>State</th>
// <th>Status</th>
// <th>Risk</th>
// <th>Registration Date</th>

// </tr>

// </thead>

// <tbody>

// {filteredCases.map((c,i)=>(

// <tr key={i}>

// <td>{c["Entity Name"]}</td>
// <td>{c.case_number}</td>
// <td>{c.court}</td>
// <td>{c.judge}</td>
// <td>{c.state}</td>
// <td>{c.case_status}</td>
// <td>{c.litigation_risk_score}</td>
// <td>{c.registration_date}</td>

// </tr>

// ))}

// </tbody>

// </table>

// </div>

// );

// }

// export default Dashboard;


















import { useEffect, useState } from "react";
import api from "../api";
import "./dashboard.css";

import {
  BarChart, Bar,
  PieChart, Pie, Cell,
  LineChart, Line,
  XAxis, YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts";
import "./dashboard.css";

const COLORS = ["#e5fa24", "#fcbf56", "#40c8e0", "#a64afc", "#4863b9"];

function Dashboard() {
  const [data, setData] = useState(null);
  const [entityFilter, setEntityFilter] = useState("");
  const [stateFilter, setStateFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  useEffect(() => {
    api.get("/dashboard").then(res => setData(res.data));
  }, []);

  if (!data) return <p className="loading">Loading dashboard...</p>;

  const filteredCases = data.cases.filter(c =>
    (!entityFilter || c["Entity Name"] === entityFilter) &&
    (!stateFilter || c.state === stateFilter) &&
    (!statusFilter || c.case_status === statusFilter)
  );

  const kpi = {
    total: filteredCases.length,
    entities: new Set(filteredCases.map(c => c["Entity Name"])) .size,
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
      <div className="header1">
  <div className="header1-left">
    <h1>Legal Intelligence Dashboard</h1>
  </div>

  <div className="header1-right">
    <span>Welcome, Admin</span>
  </div>
</div>

      <div className="filters">
        <select onChange={e => setEntityFilter(e.target.value)}>
          <option value="">All Entities</option>
          {[...new Set(data.cases.map(c => c["Entity Name"]))].map(e => <option key={e}>{e}</option>)}
        </select>

        <select onChange={e => setStateFilter(e.target.value)}>
          <option value="">All States</option>
          {[...new Set(data.cases.map(c => c.state))].map(s => <option key={s}>{s}</option>)}
        </select>

        <select onChange={e => setStatusFilter(e.target.value)}>
          <option value="">All Status</option>
          <option>Pending</option>
          <option>Dismissed</option>
          <option>Allowed</option>
          <option>Disposed</option>
        </select>
      </div>

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























































body {
  font-family: 'Inter', sans-serif;
  background: #ffffff;
}
.page-content {
  overflow:hidden ;   /* IE/Edge */
}
.dashboard {
  height: calc(100vh - 60px); /* adjust 60px = header height */
  overflow-y: auto;

  scrollbar-width: none;      /* Firefox */
}

.dashboard::-webkit-scrollbar {
  display: none;              /* Chrome */
}
.page-content::-webkit-scrollbar {
  display: none;              /* Chrome, Safari */
}
.dashboard {
  padding: 0px;
}

.title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 0px;
}

/* ===== HEADER ===== */

.header1 {
  background: linear-gradient(90deg, #2f3e46, #354f52);
  padding: 15px 25px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}

.header1 h1 {
  color: #ffffff;
  font-size: 22px;
  font-weight: 600;
  margin: 0;
  letter-spacing: 0.5px;
}
.header1 {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(90deg, #2f3e46, #354f52);
  padding: 15px 25px;
  border-radius: 8px;
}

.header1-right {
  color: #d1d5db;
  font-size: 14px;
}
.filters select {
  margin-right: 10px;
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #ddd;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin: 20px 0;
}

.card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: 0.3s;
}

.card:hover {
  transform: translateY(-5px);
}

.card h2 {
  font-size: 26px;
}

.charts {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
}

.chart {
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.table-wrapper {
  overflow-x: auto;
  background: white;
  border-radius: 12px;
  margin-top: 20px;
}

.cases-table {
  width: 100%;
  border-collapse: collapse;
}

.cases-table th, .cases-table td {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.cases-table tr:hover {
  background: #f9fafb;
}

.risk-high {
  color: #ef4444;
  /* font-weight: bold; */
}

.risk-low {
  color: #22c55e;
  /* font-weight: bold; */
}
.filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

body {
  margin: 0;
  overflow-y: hidden;
}

.dashboard {
  height: calc(100vh - 60px);
  overflow-y: auto;
  padding-bottom: 40px; /* 👈 adds white space below table */
}




























