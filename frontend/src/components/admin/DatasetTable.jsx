import { Link } from "react-router-dom";
import { FaEdit, FaTrash } from "react-icons/fa";

import { deleteDataset } from "../../Services/datasetService";
import { useToast } from "../../context/ToastContext";

function DatasetTable({ datasets, loading, refresh }) {
  const showToast = useToast();
  const handleDelete = async (slug) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this dataset?"
    );

    if (!confirmed) return;

    try {
      await deleteDataset(slug);

      showToast("Dataset deleted successfully!");

      refresh();
    } catch (error) {
      console.error("Delete failed:", error);

      const message =
        error.response?.data?.detail || "Failed to delete dataset.";

      showToast(message, "error");
    }
  };

  if (loading) {
    return (
      <div className="animate-pulse overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 p-6" aria-label="Loading datasets">
        {Array.from({ length: 6 }).map((_, index) => <div key={index} className="mb-4 h-10 rounded bg-slate-800 last:mb-0" />)}
      </div>
    );
  }

  if (datasets.length === 0) {
    return (
      <div className="rounded-2xl border border-slate-800 bg-slate-900 p-8 text-center text-white">
        No datasets found.
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-slate-900">
      <table className="min-w-full">
        <thead className="border-b border-slate-800 bg-slate-950">
          <tr>
            <th className="px-6 py-4 text-left text-slate-300">Dataset</th>
            <th className="px-6 py-4 text-left text-slate-300">Category</th>
            <th className="px-6 py-4 text-left text-slate-300">ML Task</th>
            <th className="px-6 py-4 text-left text-slate-300">Downloads</th>
            <th className="px-6 py-4 text-left text-slate-300">Rating</th>
            <th className="px-6 py-4 text-center text-slate-300">Actions</th>
          </tr>
        </thead>

        <tbody>
          {datasets.map((dataset) => (
            <tr
              key={dataset.slug}
              className="border-b border-slate-800 hover:bg-slate-800/40"
            >
              <td className="px-6 py-5 font-medium text-white">
                {dataset.name}
              </td>

              <td className="px-6 py-5 text-slate-300">
                {dataset.category}
              </td>

              <td className="px-6 py-5 text-slate-300">
                {dataset.ml_task}
              </td>

              <td className="px-6 py-5 text-slate-300">
                {dataset.downloads}
              </td>

              <td className="px-6 py-5 text-yellow-400">
                ⭐ {dataset.rating}
              </td>

              <td className="px-6 py-5">
                <div className="flex justify-center gap-3">
                  <Link
                    to={`/admin/edit/${dataset.slug}`}
                    className="rounded-lg bg-blue-600 p-3 text-white transition hover:bg-blue-500"
                  >
                    <FaEdit />
                  </Link>

                  <button
                    onClick={() => handleDelete(dataset.slug)}
                    className="rounded-lg bg-red-600 p-3 text-white transition hover:bg-red-500"
                  >
                    <FaTrash />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DatasetTable;
