import {
  FaFileAlt,
  FaGlobe,
  FaBalanceScale,
  FaBullseye,
  FaFileArchive,
} from "react-icons/fa";

function DatasetDescription({ dataset }) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900 p-8">

      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white">
          About this Dataset
        </h2>

        <p className="mt-4 text-lg leading-8 text-slate-400">
          {dataset.description}
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">

        <div className="flex items-start gap-4 rounded-2xl border border-slate-800 bg-slate-950 p-5">
          <FaBalanceScale className="mt-1 text-2xl text-cyan-400" />

          <div>
            <p className="text-sm text-slate-400">
              License
            </p>

            <h3 className="mt-1 text-lg font-semibold text-white">
              {dataset.license}
            </h3>
          </div>
        </div>

        <div className="flex items-start gap-4 rounded-2xl border border-slate-800 bg-slate-950 p-5">
          <FaGlobe className="mt-1 text-2xl text-cyan-400" />

          <div>
            <p className="text-sm text-slate-400">
              Language
            </p>

            <h3 className="mt-1 text-lg font-semibold text-white">
              {dataset.language}
            </h3>
          </div>
        </div>

        <div className="flex items-start gap-4 rounded-2xl border border-slate-800 bg-slate-950 p-5">
          <FaBullseye className="mt-1 text-2xl text-cyan-400" />

          <div>
            <p className="text-sm text-slate-400">
              Target Column
            </p>

            <h3 className="mt-1 text-lg font-semibold text-white">
              {dataset.target_column}
            </h3>
          </div>
        </div>

        <div className="flex items-start gap-4 rounded-2xl border border-slate-800 bg-slate-950 p-5">
          <FaFileArchive className="mt-1 text-2xl text-cyan-400" />

          <div>
            <p className="text-sm text-slate-400">
              File Size
            </p>

            <h3 className="mt-1 text-lg font-semibold text-white">
              {dataset.file_size}
            </h3>
          </div>
        </div>

        <div className="flex items-start gap-4 rounded-2xl border border-slate-800 bg-slate-950 p-5 md:col-span-2">
          <FaFileAlt className="mt-1 text-2xl text-cyan-400" />

          <div>
            <p className="text-sm text-slate-400">
              Dataset Slug
            </p>

            <h3 className="mt-1 break-all text-lg font-semibold text-white">
              {dataset.slug}
            </h3>
          </div>
        </div>

      </div>

    </section>
  );
}

export default DatasetDescription;