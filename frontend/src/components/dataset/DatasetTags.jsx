import { FaTags } from "react-icons/fa";

function DatasetTags({ dataset }) {
  const tags = dataset.tags
    ? dataset.tags
        .split(",")
        .map((tag) => tag.trim())
        .filter(Boolean)
    : [];

  if (tags.length === 0) {
    return null;
  }

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900 p-8">

      <div className="mb-8 flex items-center gap-3">

        <FaTags className="text-2xl text-cyan-400" />

        <h2 className="text-3xl font-bold text-white">
          Tags
        </h2>

      </div>

      <div className="flex flex-wrap gap-4">

        {tags.map((tag) => (
          <span
            key={tag}
            className="rounded-full border border-cyan-500/30 bg-cyan-500/10 px-5 py-2 text-sm font-medium text-cyan-300 transition hover:bg-cyan-500 hover:text-white"
          >
            #{tag}
          </span>
        ))}

      </div>

    </section>
  );
}

export default DatasetTags;