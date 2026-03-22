import { BrowserRouter, Routes, Route } from "react-router-dom";

import Header from "./components/Header";

import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import Entities from "./pages/Entities";
import Alerts from "./pages/Alerts";
import Reports from "./pages/Reports";
import Automation from "./pages/Automation";

import "./App.css";

function App() {

  return (

    <BrowserRouter>

      <Header />

      <div className="page">

        <Routes>

          <Route path="/" element={<Home />} />

          <Route path="/dashboard" element={<Dashboard />} />

          <Route path="/entities" element={<Entities />} />

          <Route path="/alerts" element={<Alerts />} />

          <Route path="/reports" element={<Reports />} />

          <Route path="/automation" element={<Automation />} />

        </Routes>

      </div>

    </BrowserRouter>

  );

}

export default App;