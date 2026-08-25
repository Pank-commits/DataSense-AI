import {
  FaFilter,
  FaDatabase,
  FaRobot,
  FaLayerGroup,
  FaSignal,
  FaRedo,
} from "react-icons/fa";

function Sidebar({
  filters = {},
  onFilterChange = () => {},
  onClear = () => {},
}) {
  return (
    <aside className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sticky top-24">

      <div className="flex items-center gap-3 mb-8">

        <FaFilter className="text-cyan-400 text-2xl" />

        <h2 className="text-2xl font-bold text-white">
          Filters
        </h2>

      </div>

      {/* Category */}

      <div className="mb-6">

        <label className="flex items-center gap-2 text-slate-300 font-semibold mb-3">

          <FaDatabase className="text-cyan-400" />

          Category

        </label>

        <select
          value={filters.category || ""}
          onChange={(e) =>
            onFilterChange("category", e.target.value)
          }
          className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="">All Categories</option>
          <option value="Healthcare">Healthcare</option>
          <option value="Finance">Finance</option>
          <option value="Business">Business</option>
          <option value="Education">Education</option>
          <option value="Agriculture">Agriculture</option>
          <option value="NLP">NLP</option>
          <option value="Computer Vision">Computer Vision</option>
        </select>

      </div>

      {/* ML Task */}

      <div className="mb-6">

        <label className="flex items-center gap-2 text-slate-300 font-semibold mb-3">

          <FaRobot className="text-cyan-400" />

          ML Task

        </label>

        <select
          value={filters.ml_task || ""}
          onChange={(e) =>
            onFilterChange("ml_task", e.target.value)
          }
          className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="">All Tasks</option>
          <option value="Classification">Classification</option>
          <option value="Regression">Regression</option>
          <option value="Clustering">Clustering</option>
          <option value="Recommendation">Recommendation</option>
          <option value="NLP">NLP</option>
        </select>

      </div>

      {/* Data Type */}

      <div className="mb-6">

        <label className="flex items-center gap-2 text-slate-300 font-semibold mb-3">

          <FaLayerGroup className="text-cyan-400" />

          Data Type

        </label>

        <select
          value={filters.data_type || ""}
          onChange={(e) =>
            onFilterChange("data_type", e.target.value)
          }
          className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="">All Types</option>
          <option value="CSV">CSV</option>
          <option value="Excel">Excel</option>
          <option value="JSON">JSON</option>
          <option value="Images">Images</option>
          <option value="Text">Text</option>
        </select>

      </div>

      {/* Difficulty */}

      <div className="mb-8">

        <label className="flex items-center gap-2 text-slate-300 font-semibold mb-3">

          <FaSignal className="text-cyan-400" />

          Difficulty

        </label>

        <select
          value={filters.difficulty || ""}
          onChange={(e) =>
            onFilterChange("difficulty", e.target.value)
          }
          className="w-full bg-slate-800 border border-slate-700 rounded-xl px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="">All Levels</option>
          <option value="Beginner">Beginner</option>
          <option value="Intermediate">Intermediate</option>
          <option value="Advanced">Advanced</option>
        </select>

      </div>

      <p className="text-sm text-slate-400">
        Filters update automatically.
      </p>

      <button
        onClick={onClear}
        className="w-full mt-4 border border-slate-700 hover:border-red-500 hover:text-red-400 transition rounded-xl py-3 text-slate-300 font-semibold flex items-center justify-center gap-2"
      >
        <FaRedo />

        Clear Filters

      </button>

    </aside>
  );
}

export default Sidebar;
