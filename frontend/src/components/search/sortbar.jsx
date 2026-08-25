import { FaSortAmountDown, FaSortAmountUp } from "react-icons/fa";

function SortBar({
  sort,
  setSort,
  order,
  setOrder,
}) {
  return (
    <div className="flex flex-col gap-4 rounded-2xl border border-slate-800 bg-slate-900 p-6 md:flex-row md:items-center md:justify-between">

      <div className="flex items-center gap-3">
        <label className="font-semibold text-white">
          Sort By
        </label>

        <select
          value={sort}
          onChange={(e) => setSort(e.target.value)}
          className="rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-white outline-none focus:border-cyan-400"
        >
          <option value="name">Name</option>
          <option value="rating">Rating</option>
          <option value="downloads">Downloads</option>
          <option value="created_at">Recently Added</option>
        </select>
      </div>

      <button
        onClick={() =>
          setOrder(order === "asc" ? "desc" : "asc")
        }
        className="flex items-center justify-center gap-2 rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-white transition hover:bg-cyan-400"
      >
        {order === "asc" ? (
          <>
            <FaSortAmountUp />
            Ascending
          </>
        ) : (
          <>
            <FaSortAmountDown />
            Descending
          </>
        )}
      </button>

    </div>
  );
}

export default SortBar;