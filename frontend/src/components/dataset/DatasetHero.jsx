import {
  FaDatabase,
  FaDownload,
  FaStar,
  FaExternalLinkAlt,
  FaTag,
} from "react-icons/fa";

function DatasetHero({ dataset }) {
  return (
    <section className="relative overflow-hidden bg-slate-950 border-b border-slate-800">

      {/* Background Glow */}
      <div className="absolute -top-20 -left-20 h-72 w-72 rounded-full bg-cyan-500/10 blur-[120px]" />
      <div className="absolute bottom-0 right-0 h-72 w-72 rounded-full bg-blue-500/10 blur-[120px]" />

      <div className="relative mx-auto max-w-7xl px-6 py-16">

        <div className="grid gap-12 lg:grid-cols-3">

          {/* Thumbnail */}
          <div>

            <img
              src={dataset.thumbnail}
              alt={dataset.name}
              className="w-full rounded-3xl border border-slate-800 object-cover shadow-2xl"
            />

          </div>

          {/* Dataset Info */}
          <div className="lg:col-span-2">

            <div className="flex flex-wrap gap-3">

              <span className="rounded-full bg-cyan-500/10 px-4 py-2 text-cyan-300">
                {dataset.category}
              </span>

              <span className="rounded-full bg-slate-800 px-4 py-2 text-white">
                {dataset.ml_task}
              </span>

              <span className="rounded-full bg-emerald-500/10 px-4 py-2 text-emerald-300">
                {dataset.difficulty}
              </span>

            </div>

            <h1 className="mt-6 text-5xl font-bold text-white">
              {dataset.name}
            </h1>

            <p className="mt-6 text-lg leading-8 text-slate-400">
              {dataset.description}
            </p>

            {/* Stats */}

            <div className="mt-10 grid gap-5 md:grid-cols-4">

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

                <FaDatabase className="mb-3 text-2xl text-cyan-400" />

                <p className="text-sm text-slate-400">
                  Data Type
                </p>

                <h3 className="text-lg font-semibold text-white">
                  {dataset.data_type}
                </h3>

              </div>

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

                <FaDownload className="mb-3 text-2xl text-cyan-400" />

                <p className="text-sm text-slate-400">
                  Downloads
                </p>

                <h3 className="text-lg font-semibold text-white">
                  {dataset.downloads}
                </h3>

              </div>

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

                <FaStar className="mb-3 text-2xl text-yellow-400" />

                <p className="text-sm text-slate-400">
                  Rating
                </p>

                <h3 className="text-lg font-semibold text-white">
                  {dataset.rating}
                </h3>

              </div>

              <div className="rounded-2xl border border-slate-800 bg-slate-900 p-5">

                <FaTag className="mb-3 text-2xl text-cyan-400" />

                <p className="text-sm text-slate-400">
                  Source
                </p>

                <h3 className="text-lg font-semibold text-white">
                  {dataset.source}
                </h3>

              </div>

            </div>

            {/* Buttons */}

            <div className="mt-10 flex flex-wrap gap-5">

              <a
                href={dataset.download_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 rounded-xl bg-cyan-500 px-8 py-4 font-semibold text-white transition hover:bg-cyan-400"
              >
                <FaDownload />

                Download Dataset
              </a>

              <a
                href={dataset.download_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 rounded-xl border border-slate-700 px-8 py-4 font-semibold text-white transition hover:border-cyan-400"
              >
                <FaExternalLinkAlt />

                Visit Source
              </a>

            </div>

          </div>

        </div>

      </div>

    </section>
  );
}

export default DatasetHero;