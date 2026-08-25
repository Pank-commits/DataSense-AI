import { FaUserCircle } from "react-icons/fa";

function AdminNavbar() {
  return (
    <header className="flex items-center justify-between border-b border-slate-800 bg-slate-900 px-8 py-5">

      <h2 className="text-2xl font-bold text-white">
        Admin Dashboard
      </h2>

      <div className="flex items-center gap-3">

        <FaUserCircle className="text-3xl text-cyan-400" />

        <span className="text-white">
          Admin
        </span>

      </div>

    </header>
  );
}

export default AdminNavbar;