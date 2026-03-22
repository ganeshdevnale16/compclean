// import { Link } from "react-router-dom";

// function Header() {

//   return (

//     <header className="header">

//       <div className="logo">
//         Legal Monitor
//       </div>

//       <nav>

//         <Link to="/">Home</Link>

//         <Link to="/dashboard">Dashboard</Link>

//         <Link to="/entities">Entities</Link>

//         <Link to="/alerts">Alerts</Link>

//         <Link to="/reports">Reports</Link>

//         <Link to="/automation">Automation</Link>

//       </nav>

//     </header>

//   );

// }

// export default Header;







import { Link } from "react-router-dom";
import { FaHome, FaChartBar, FaBuilding, FaBell, FaFileAlt, FaCogs } from "react-icons/fa";
import "./header.css";

function Header() {

  return (
    <header className="main-header">

      <div className="logo">
        Legal Monitor
      </div>

      <nav className="nav-menu">

        <Link to="/">
          <FaHome />
          <span>Home</span>
        </Link>

        <Link to="/dashboard">
          <FaChartBar />
          <span>Dashboard</span>
        </Link>

        <Link to="/entities">
          <FaBuilding />
          <span>Entities</span>
        </Link>

        <Link to="/alerts">
          <FaBell />
          <span>Alerts</span>
        </Link>

        <Link to="/reports">
          <FaFileAlt />
          <span>Reports</span>
        </Link>

        <Link to="/automation">
          <FaCogs />
          <span>Automation</span>
        </Link>

        

      </nav>

    </header>
  );
}

export default Header;