import { Link } from "react-router-dom";
import {
  FaDatabase,
  FaDownload,
  FaStar,
  FaExternalLinkAlt,
} from "react-icons/fa";

function DatasetCard({ dataset }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 hover:border-cyan-400 transition duration-300">

      <div className="flex justify-between items-start">

        <h3 className="text-2xl font-bold text-white">
          {dataset.name}
        </h3>

        <span className="bg-cyan-500/10 text-cyan-300 px-3 py-1 rounded-full text-sm">
          {dataset.difficulty}
        </span>

      </div>

      <p className="text-slate-400 mt-4 line-clamp-3">
        {dataset.description}
      </p>

      <div className="flex flex-wrap gap-2 mt-5">

        <span className="bg-slate-800 px-3 py-1 rounded-full text-sm text-cyan-300">
          {dataset.category}
        </span>

        <span className="bg-slate-800 px-3 py-1 rounded-full text-sm text-white">
          {dataset.ml_task}
        </span>

        <span className="bg-slate-800 px-3 py-1 rounded-full text-sm text-white">
          {dataset.data_type}
        </span>

      </div>

      <div className="flex justify-between items-center mt-8">

        <div className="flex gap-4 text-slate-400 text-sm">

          <span className="flex items-center gap-2">
            <FaDownload />
            {dataset.downloads}
          </span>

          <span className="flex items-center gap-2">
            <FaStar />
            {dataset.rating}
          </span>

        </div>

        <Link
          to={`/datasets/${dataset.slug}`}
          className="flex items-center gap-2 text-cyan-400 hover:text-cyan-300"
        >
          View
          <FaExternalLinkAlt />
        </Link>

      </div>

    </div>
  );
}

export default DatasetCard;