// // import {useEffect,useState} from "react";
// // import api from "../api";

// // function Alerts(){

// // const [alerts,setAlerts]=useState([]);
// // const [logs,setLogs]=useState([]);
// // const [selected,setSelected]=useState(null);

// // const [name,setName]=useState("");
// // const [time,setTime]=useState("");
// // const [frequency,setFrequency]=useState("daily");


// // useEffect(()=>{

// // loadAlerts();

// // },[]);


// // const loadAlerts=async()=>{

// // const res=await api.get("/alerts");

// // setAlerts(res.data);

// // };


// // const createAlert=async()=>{

// // await api.post("/alerts",{

// // name,
// // time,
// // frequency,
// // status:"active"

// // });

// // loadAlerts();

// // };


// // const toggleAlert=async(id)=>{

// // await api.post(`/alerts/${id}/toggle`);

// // loadAlerts();

// // };


// // const viewHistory=async(id)=>{

// // const res=await api.get(`/alerts/${id}/logs`);

// // setLogs(res.data);

// // setSelected(id);

// // };


// // return(

// // <div>

// // <h1>Alerts</h1>

// // <div>

// // <input
// // placeholder="Alert Name"
// // onChange={(e)=>setName(e.target.value)}
// // />

// // <select
// // onChange={(e)=>setFrequency(e.target.value)}
// // >

// // <option value="daily">Daily</option>
// // <option value="weekly">Weekly</option>
// // <option value="monthly">Monthly</option>

// // </select>

// // <input
// // type="time"
// // onChange={(e)=>setTime(e.target.value)}
// // />

// // <button onClick={createAlert}>
// // Create Alert
// // </button>

// // </div>


// // <table>

// // <thead>

// // <tr>
// // <th>Name</th>
// // <th>Frequency</th>
// // <th>Time</th>
// // <th>Status</th>
// // <th>Actions</th>
// // </tr>

// // </thead>


// // <tbody>

// // {alerts.map(a=>(

// // <tr key={a.id}>

// // <td>{a.name}</td>
// // <td>{a.frequency}</td>
// // <td>{a.time}</td>
// // <td>{a.status}</td>

// // <td>

// // <button onClick={()=>toggleAlert(a.id)}>
// // Toggle
// // </button>

// // <button onClick={()=>viewHistory(a.id)}>
// // History
// // </button>

// // </td>

// // </tr>

// // ))}

// // </tbody>

// // </table>


// // {selected && (

// // <div>

// // <h3>Alert Logs</h3>

// // <table>

// // <thead>

// // <tr>
// // <th>Time</th>
// // <th>Status</th>
// // <th>Emails</th>
// // <th>Cases</th>
// // </tr>

// // </thead>

// // <tbody>

// // {logs.map((l,i)=>(

// // <tr key={i}>

// // <td>{l.run_time}</td>
// // <td>{l.status}</td>
// // <td>{l.emails_sent}</td>
// // <td>{l.cases_found}</td>

// // </tr>

// // ))}

// // </tbody>

// // </table>

// // </div>

// // )}

// // </div>

// // );

// // }

// // export default Alerts;








// import { useEffect, useState } from "react";
// import api from "../api";
// import { FaCog } from "react-icons/fa";
// import "./Alerts.css";

// function Alerts() {

// const [alerts,setAlerts] = useState([]);
// const [logs,setLogs] = useState([]);
// const [selected,setSelected] = useState(null);
// const editAlert = async (id)=>{

// const name = prompt("New alert name")
// const time = prompt("New time")

// await api.put(`/alerts/${id}`,{
// name:name,
// time:time
// })

// loadAlerts()

// }

// useEffect(()=>{
//     loadAlerts();
// },[]);

// const loadAlerts = async ()=>{
//     const res = await api.get("/alerts");
//     setAlerts(res.data);
// };

// const toggleAlert = async(id)=>{
//     await api.post(`/alerts/${id}/toggle`);
//     loadAlerts();
// };

// const deleteAlert = async(id)=>{
//     await api.delete(`/alerts/${id}`);
//     loadAlerts();
// };

// const viewHistory = async(id)=>{

// const res = await api.get(`/alerts/${id}/logs`)

// setLogs(res.data)

// setSelected(id)

// }
// <div
// className="alert-card"
// onClick={()=>viewHistory(alert.id)}
// ></div>

// return(

// <div className="alerts-container">

// <h2>Alerts</h2>

// <div className="alerts-grid">

// {alerts.map(alert=>(

// <div
// key={alert.id}
// className={`alert-card ${alert.status}`}
// onClick={()=>viewHistory(alert.id)}
// >

// <div className="alert-header">

// <h3>{alert.name}</h3>

// <div className="settings">

// <FaCog />

// <div className="menu">

// <button onClick={()=>toggleAlert(alert.id)}>
// {alert.status === "active" ? "Pause" : "Activate"}
// </button>

// <button onClick={()=>editAlert(alert.id)}>
// Edit
// </button>

// <button onClick={()=>deleteAlert(alert.id)}>
// Delete
// </button>

// </div>

// </div>

// </div>

// <p><b>Frequency:</b> {alert.frequency}</p>
// <p><b>Time:</b> {alert.time}</p>
// <p><b>Status:</b> {alert.status}</p>

// </div>

// ))}

// </div>

// {selected && (

// <div className="history-panel">

// <h3>Alert History</h3>

// <table>

// <thead>
// <tr>
// <th>Time</th>
// <th>Status</th>
// <th>Emails</th>
// <th>Cases</th>
// </tr>
// </thead>

// <tbody>

// {logs.length === 0 ?

// <tr>
// <td colSpan="4">No history yet</td>
// </tr>

// :

// logs.map((l,i)=>(

// <tr key={i}>
// <td>{l.run_time}</td>
// <td>{l.status}</td>
// <td>{l.emails_sent}</td>
// <td>{l.cases_found}</td>
// </tr>

// ))

// }

// </tbody>

// </table>

// </div>

// )}

// </div>

// );

// }

// export default Alerts;











































// import { useEffect, useState } from "react";
// import api from "../api";
// import { FaCog } from "react-icons/fa";
// import "./Alerts.css";

// function Alerts() {

// const [alerts, setAlerts] = useState([]);
// const [logs, setLogs] = useState([]);
// const [selected, setSelected] = useState(null);

// // 🔹 Edit Modal State
// const [showEditModal, setShowEditModal] = useState(false);
// const [editData, setEditData] = useState({});

// // 🔹 History Modal State
// const [showHistoryModal, setShowHistoryModal] = useState(false);

// useEffect(() => {
// loadAlerts();
// }, []);

// const loadAlerts = async () => {
// const res = await api.get("/alerts");
// setAlerts(res.data);
// };

// // --------------------
// // ACTIONS
// // --------------------

// const toggleAlert = async (id) => {
// await api.post(`/alerts/${id}/toggle`);
// loadAlerts();
// };

// const deleteAlert = async (id) => {
// await api.delete(`/alerts/${id}`);
// loadAlerts();
// };

// const openEditModal = (alert, e) => {
// e.stopPropagation();
// setEditData(alert);
// setShowEditModal(true);
// };

// const updateAlert = async () => {
// await api.put(`/alerts/${editData.id}`, editData);
// setShowEditModal(false);
// loadAlerts();
// };

// const viewHistory = async (id) => {
// const res = await api.get(`/alerts/${id}/logs`);
// setLogs(res.data);
// setSelected(id);
// setShowHistoryModal(true);
// };

// // --------------------
// // UI
// // --------------------

// return (

// <div className="alerts-container">

// <h2>Alerts</h2>

// <div className="alerts-grid">

// {alerts.map(alert => (

// <div
// key={alert.id}
// className={`alert-card ${alert.status}`}
// onClick={() => viewHistory(alert.id)}
// >

// <div className="alert-header">

// <h3>{alert.name}</h3>

// <div className="settings">
// <FaCog />

// <div className="menu">

// <button onClick={(e)=>{
// e.stopPropagation();
// toggleAlert(alert.id);
// }}>
// {alert.status === "active" ? "Pause" : "Activate"} </button>

// <button onClick={(e)=> openEditModal(alert, e)}>
// Edit </button>

// <button onClick={(e)=>{
// e.stopPropagation();
// deleteAlert(alert.id);
// }}>
// Delete </button>

// </div>

// </div>

// </div>

// <p><b>Frequency:</b> {alert.frequency}</p>
// <p><b>Time:</b> {alert.time}</p>
// <p><b>Status:</b> {alert.status}</p>

// </div>

// ))}

// </div>

// {/* ===================== */}
// {/* EDIT MODAL */}
// {/* ===================== */}

// {showEditModal && (

// <div className="modal-overlay">
//     <div className="modal">

// ```
//     <h3>Edit Alert</h3>

//     <input
//         value={editData.name}
//         onChange={(e)=>setEditData({...editData, name: e.target.value})}
//         placeholder="Alert Name"
//     />

//     <input
//         type="time"
//         value={editData.time}
//         onChange={(e)=>setEditData({...editData, time: e.target.value})}
//     />

//     <select
//         value={editData.frequency}
//         onChange={(e)=>setEditData({...editData, frequency: e.target.value})}
//     >
//         <option value="daily">Daily</option>
//         <option value="weekly">Weekly</option>
//         <option value="monthly">Monthly</option>
//     </select>

//     <div className="modal-buttons">
//         <button onClick={updateAlert}>Save</button>
//         <button onClick={()=>setShowEditModal(false)}>Cancel</button>
//     </div>

// </div>
// ```

// </div>
// )}

// {/* ===================== */}
// {/* HISTORY MODAL */}
// {/* ===================== */}

// {showHistoryModal && (

// <div className="modal-overlay">
//     <div className="modal">

// ```
//     <h3>Alert History</h3>

//     <table>

//     <thead>
//     <tr>
//         <th>Time</th>
//         <th>Status</th>
//         <th>Emails</th>
//         <th>Cases</th>
//     </tr>
//     </thead>

//     <tbody>

//     {logs.length === 0 ? (
//         <tr>
//             <td colSpan="4">No history yet</td>
//         </tr>
//     ) : (
//         logs.map((l, i) => (
//             <tr key={i}>
//                 <td>{l.run_time}</td>
//                 <td>{l.status}</td>
//                 <td>{l.emails_sent}</td>
//                 <td>{l.cases_found}</td>
//             </tr>
//         ))
//     )}

//     </tbody>

//     </table>

//     <button onClick={()=>setShowHistoryModal(false)}>Close</button>

// </div>
// ```

// </div>
// )}

// </div>
// );

// }

// export default Alerts;

















import { useEffect, useState } from "react";
import api from "../api";
import { FaCog } from "react-icons/fa";
import "./Alerts.css";

function Alerts() {

const [alerts, setAlerts] = useState([]);
const [logs, setLogs] = useState([]);

const [showEditModal, setShowEditModal] = useState(false);
const [showCreateModal, setShowCreateModal] = useState(false);
const [showHistoryModal, setShowHistoryModal] = useState(false);

const runAlertNow = async (id) => {
  const confirmRun = window.confirm("Run this alert manually now?");
  if (!confirmRun) return;

  try {
    await api.post(`/alerts/${id}/run`);
    alert("Alert triggered successfully!");
    loadAlerts();
  } catch (err) {
    alert("Failed to run alert");
  }
};

const [editData, setEditData] = useState({});
const [newAlert, setNewAlert] = useState({
name: "",
time: "",
frequency: "daily"
});

const [activeMenu, setActiveMenu] = useState(null);

// --------------------
// LOAD
// --------------------

useEffect(() => {
loadAlerts();
}, []);

const loadAlerts = async () => {
const res = await api.get("/alerts");
setAlerts(res.data);
};

// Close dropdown on outside click
useEffect(() => {
const handleClick = () => setActiveMenu(null);
window.addEventListener("click", handleClick);
return () => window.removeEventListener("click", handleClick);
}, []);

// --------------------
// ACTIONS
// --------------------
// const [menuPosition, setMenuPosition] = useState({ x: 0, y: 0 });
const toggleAlert = async (id) => {
await api.post(`/alerts/${id}/toggle`);
loadAlerts();
};

const deleteAlert = async (id) => {
const confirmDelete = window.confirm("Are you sure you want to delete this alert?");
if (!confirmDelete) return;

await api.delete(`/alerts/${id}`);
loadAlerts();
};

const openEditModal = (alert, e) => {
  if (e) e.stopPropagation();
  setEditData(alert);
  setShowEditModal(true);
};

const updateAlert = async () => {
if (!editData.name || !editData.time) {
alert("Name and Time required");
return;
}

await api.put(`/alerts/${editData.id}`, editData);
setShowEditModal(false);
loadAlerts();
};

const createAlert = async () => {
if (!newAlert.name || !newAlert.time) {
alert("Please fill all fields");
return;
}

await api.post("/alerts", {
...newAlert,
status: "active"
});

setShowCreateModal(false);
setNewAlert({ name: "", time: "", frequency: "daily" });
loadAlerts();
};

const viewHistory = async (id) => {
const res = await api.get(`/alerts/${id}/logs`);
setLogs(res.data);
setShowHistoryModal(true);
};

// --------------------
// UI
// --------------------

return (

<div className="alerts-container">

{/* HEADER */}

<div className="header1">
  <div className="header-left">
    <h1>Alerts</h1>
  </div>

  <div className="header-right">
    <button className="create-btn" onClick={()=>setShowCreateModal(true)}>
      + New Alert
    </button>
  </div>
</div>

{/* LIST UI */}

<div className="alerts-list">

{alerts.map(alert => (

<div
key={alert.id}
className="alert-row"
onClick={() => viewHistory(alert.id)}
>

<div className="left">⏱</div>

<div className="middle">
  <div className="alert-name">{alert.name}</div>

  <div className="alert-meta">
    <span>{alert.frequency}</span>
    <span> | </span>
    <span>{alert.time}</span>
    <span> | </span>
    <span className={alert.status === "active" ? "status-active" : "status-paused"}>
      {alert.status}
    </span>
  </div>
</div>

<div className="right">

  <div className="gear-container" onClick={(e)=>e.stopPropagation()}>


<FaCog onClick={()=>{
  setActiveMenu(alert.id === activeMenu ? null : alert.id);
}}/>

{activeMenu === alert.id && (
  <div className="dropdown">

    <button onClick={()=>toggleAlert(alert.id)}>
      {alert.status === "active" ? "Pause" : "Activate"}
    </button>

    <button onClick={() => runAlertNow(alert.id)}>
    Run Now   {/* 🔥 NEW */}
  </button>

    <button onClick={(e)=>openEditModal(alert, e)}>
      Edit
    </button>

    <button onClick={()=>deleteAlert(alert.id)}>
      Delete
    </button>

  </div>
)}


  </div>

</div>

</div>

))}

</div>

{/* ===================== */}
{/* CREATE MODAL */}
{/* ===================== */}

{showCreateModal && (

<div className="modal-overlay">
  <div className="modal">


<h3>Create Alert</h3>

<input
  placeholder="Alert Name"
  value={newAlert.name}
  onChange={(e)=>setNewAlert({...newAlert, name:e.target.value})}
/>

<input
  type="time"
  value={newAlert.time}
  onChange={(e)=>setNewAlert({...newAlert, time:e.target.value})}
/>

<select
  value={newAlert.frequency}
  onChange={(e)=>setNewAlert({...newAlert, frequency:e.target.value})}
>
  <option value="daily">Daily</option>
  <option value="weekly">Weekly</option>
  <option value="monthly">Monthly</option>
</select>

<div className="modal-buttons">
  <button onClick={createAlert}>Create</button>
  <button onClick={()=>setShowCreateModal(false)}>Cancel</button>
</div>


  </div>
</div>
)}

{/* ===================== */}
{/* EDIT MODAL */}
{/* ===================== */}

{showEditModal && (

<div className="modal-overlay">
  <div className="modal">


<h3>Edit Alert</h3>

<input
  value={editData.name}
  onChange={(e)=>setEditData({...editData, name:e.target.value})}
/>

<input
  type="time"
  value={editData.time}
  onChange={(e)=>setEditData({...editData, time:e.target.value})}
/>

<select
  value={editData.frequency}
  onChange={(e)=>setEditData({...editData, frequency:e.target.value})}
>
  <option value="daily">Daily</option>
  <option value="weekly">Weekly</option>
  <option value="monthly">Monthly</option>
</select>

<div className="modal-buttons">
  <button onClick={updateAlert}>Save</button>
  <button onClick={()=>setShowEditModal(false)}>Cancel</button>
</div>


  </div>
</div>
)}

{/* ===================== */}
{/* HISTORY MODAL */}
{/* ===================== */}
{/* ===================== */}
{/* HISTORY MODAL */}
{/* ===================== */}
{showHistoryModal && (

<div 
  className="modal-overlay"
  onClick={() => setShowHistoryModal(false)}
>
  <div 
    className="modal history-modal"
    onClick={(e) => e.stopPropagation()}
  >

    <div className="modal-header">
      <h3 className="history-title">History</h3>
      <span className="close-icon" onClick={()=>setShowHistoryModal(false)}>×</span>
    </div>

    <table className="history-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Run Time</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>
        {logs.length === 0 ? (
          <tr>
            <td colSpan="3" className="no-data">No history yet</td>
          </tr>
        ) : (
          logs.map((l, i) => (
            <tr key={i}>
              <td style={{fontWeight: 500}}>{l.alert_name}</td>
              <td>{new Date(l.run_time).toLocaleString()}</td>
              <td className={
                l.status?.toLowerCase() === "success"
                  ? "status-success"
                  : "status-failed"
              }>
                {l.status}
              </td>
            </tr>
          ))
        )}
      </tbody>
    </table>

  </div>
</div>

)}

</div>
);

}

export default Alerts;
