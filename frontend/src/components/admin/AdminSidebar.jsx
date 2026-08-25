import { NavLink } from "react-router-dom";
import {
  FaDatabase,
  FaPlusCircle,
  FaChartBar,
} from "react-icons/fa";

function AdminSidebar() {
  const linkClass = ({ isActive }) =>
    `flex items-center gap-3 rounded-xl px-4 py-3 transition ${
      isActive
        ? "bg-cyan-500 text-white"
        : "text-slate-300 hover:bg-slate-800"
    }`;

  return (
    <aside className="w-72 border-r border-slate-800 bg-slate-900 p-6">

      <h1 className="mb-10 text-3xl font-bold text-cyan-400">
        DataSense
      </h1>

      <nav className="space-y-3">

        <NavLink to="/admin" end className={linkClass}>
          <FaChartBar />
          Dashboard
        </NavLink>

        <NavLink to="/admin/datasets" className={linkClass}>
          <FaDatabase />
          Manage Datasets
        </NavLink>

        <NavLink to="/admin/add-dataset" className={linkClass}>
          <FaPlusCircle />
          Add Dataset
        </NavLink>

      </nav>

    </aside>
  );
}

export default AdminSidebar;