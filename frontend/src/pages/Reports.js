import { useEffect, useState } from "react";
import Select from "react-select";
import api from "../api";
import "./report.css";
function Reports(){

const [data,setData] = useState([]);

const [report,setReport] = useState("cases");

const [entities,setEntities] = useState([]);
const [states,setStates] = useState([]);
const [courts,setCourts] = useState([]);
const [judges,setJudges] = useState([]);
const [statuses,setStatuses] = useState([]);
const [caseTypes,setCaseTypes] = useState([]);

const [regFrom,setRegFrom] = useState("");
const [regTo,setRegTo] = useState("");
const [decFrom,setDecFrom] = useState("");
const [decTo,setDecTo] = useState("");

useEffect(()=>{

loadData();

},[]);


const loadData = async()=>{

const res = await api.get("/cases");

setData(res.data);

};


const uniqueOptions = (field)=>{

return [...new Set(data.map(x=>x[field]).filter(v=>v && v!==""))]

.sort()

.map(v=>({label:v,value:v}));

};


const downloadReport = async(type="excel")=>{

const payload = {

report_type:report,

entity: entities.length ? entities.map(x=>x.value) : null,
state: states.length ? states.map(x=>x.value) : null,
court: courts.length ? courts.map(x=>x.value) : null,
judge: judges.length ? judges.map(x=>x.value) : null,
case_status: statuses.length ? statuses.map(x=>x.value) : null,
case_type: caseTypes.length ? caseTypes.map(x=>x.value) : null,

reg_from: regFrom || null,
reg_to: regTo || null,
dec_from: decFrom || null,
dec_to: decTo || null

};


const res = await api.post("/download-report",payload,{responseType:"blob"});

const url = window.URL.createObjectURL(new Blob([res.data]));

const link = document.createElement("a");

link.href = url;

link.download = "report.xlsx";

link.click();

};


const resetFilters = ()=>{

setEntities([]);
setStates([]);
setCourts([]);
setJudges([]);
setStatuses([]);
setCaseTypes([]);

setRegFrom("");
setRegTo("");
setDecFrom("");
setDecTo("");

};


return(

<div className="reports-page">

  <div className="header1">
    <h1>Reports Center</h1>
  </div>

  <div className="content">

<div className="report-type">

<label>Report Type</label>

<select value={report} onChange={(e)=>setReport(e.target.value)}>

<option value="cases">Case Details</option>
<option value="entity">Entity Risk Report</option>
<option value="court">Court Intelligence</option>
<option value="state">State Litigation</option>
<option value="judge">Judge Workload</option>
<option value="case_type">Case Type Analysis</option>
<option value="timeline">Litigation Timeline</option>
<option value="risk">Risk Statistics</option>
<option value="age">Case Age Distribution</option>

</select>

</div>


<div className="filters-grid">

<div>

<label>Entities</label>

<Select
isMulti
options={uniqueOptions("Entity Name")}
value={entities}
onChange={setEntities}
/>

</div>


<div>

<label>States</label>

<Select
isMulti
options={uniqueOptions("state")}
value={states}
onChange={setStates}
/>

</div>


<div>

<label>Courts</label>

<Select
isMulti
options={uniqueOptions("court")}
value={courts}
onChange={setCourts}
/>

</div>


<div>

<label>Judges</label>

<Select
isMulti
options={uniqueOptions("judge")}
value={judges}
onChange={setJudges}
/>

</div>


<div>

<label>Status</label>

<Select
isMulti
options={uniqueOptions("case_status")}
value={statuses}
onChange={setStatuses}
/>

</div>


<div>

<label>Case Type</label>

<Select
isMulti
options={uniqueOptions("case_type")}
value={caseTypes}
onChange={setCaseTypes}
/>

</div>

</div>


<div className="date-grid">

<div>

<label>Registration From</label>

<input type="date" value={regFrom} onChange={(e)=>setRegFrom(e.target.value)}/>

</div>

<div>

<label>Registration To</label>

<input type="date" value={regTo} onChange={(e)=>setRegTo(e.target.value)}/>

</div>

<div>

<label>Decision From</label>

<input type="date" value={decFrom} onChange={(e)=>setDecFrom(e.target.value)}/>

</div>

<div>

<label>Decision To</label>

<input type="date" value={decTo} onChange={(e)=>setDecTo(e.target.value)}/>

</div>

</div>


<div className="report-actions">

<button onClick={()=>downloadReport("excel")}>Download Excel</button>

<button onClick={resetFilters}>Reset Filters</button>

</div>

 </div>
</div>

);

}

export default Reports;