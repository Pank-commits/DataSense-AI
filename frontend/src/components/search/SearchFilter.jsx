import { FaFilter, FaUndo } from "react-icons/fa";

function SearchFilter({
  category,
  setCategory,
  mlTask,
  setMlTask,
  difficulty,
  setDifficulty,
  dataType,
  setDataType,
  onApply,
  onReset,
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

      <div className="mb-6 flex items-center gap-3">
        <FaFilter className="text-cyan-400 text-xl" />
        <h2 className="text-xl font-semibold text-white">
          Filter Datasets
        </h2>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">

        {/* Category */}
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="">All Categories</option>
          <option value="Healthcare">Healthcare</option>
          <option value="Finance">Finance</option>
          <option value="Education">Education</option>
          <option value="Agriculture">Agriculture</option>
          <option value="Retail">Retail</option>
          <option value="Transportation">Transportation</option>
        </select>

        {/* ML Task */}
        <select
          value={mlTask}
          onChange={(e) => setMlTask(e.target.value)}
          className="rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="">All ML Tasks</option>
          <option value="Classification">Classification</option>
          <option value="Regression">Regression</option>
          <option value="Clustering">Clustering</option>
          <option value="Detection">Detection</option>
          <option value="Segmentation">Segmentation</option>
          <option value="Recommendation">Recommendation</option>
        </select>

        {/* Difficulty */}
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="">All Difficulty</option>
          <option value="Beginner">Beginner</option>
          <option value="Intermediate">Intermediate</option>
          <option value="Advanced">Advanced</option>
        </select>

        {/* Data Type */}
        <select
          value={dataType}
          onChange={(e) => setDataType(e.target.value)}
          className="rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="">All Data Types</option>
          <option value="CSV">CSV</option>
          <option value="JSON">JSON</option>
          <option value="Excel">Excel</option>
          <option value="Image">Image</option>
          <option value="Text">Text</option>
          <option value="Audio">Audio</option>
        </select>

      </div>

      <div className="mt-6 flex flex-wrap gap-4">

        <button
          onClick={onApply}
          className="rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-white transition hover:bg-cyan-400"
        >
          Apply Filters
        </button>

        <button
          onClick={onReset}
          className="flex items-center gap-2 rounded-xl border border-slate-700 px-6 py-3 font-semibold text-white transition hover:border-cyan-400"
        >
          <FaUndo />
          Reset
        </button>

      </div>

    </div>
  );
}

export default SearchFilter;