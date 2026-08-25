import DatasetCard from "../dataset/DatasetCard";

function SearchResults({
  datasets,
  loading,
  error,
  total = 0,
}) {
  if (loading) {
    return (
      <section className="py-12">
        <div className="text-center text-slate-400">
          Loading datasets...
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="py-12">
        <div className="rounded-2xl border border-red-500/30 bg-red-500/10 p-6 text-center text-red-300">
          {error}
        </div>
      </section>
    );
  }

  if (!datasets || datasets.length === 0) {
    return (
      <section className="py-12">
        <div className="rounded-2xl border border-slate-800 bg-slate-900 p-10 text-center">
          <h3 className="text-2xl font-bold text-white">
            No datasets found
          </h3>

          <p className="mt-3 text-slate-400">
            Try changing your search keywords or filters.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="space-y-8">

      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-white">
          Search Results
        </h2>

        <span className="rounded-full bg-cyan-500/10 px-4 py-2 text-cyan-300">
          {total} Dataset{total !== 1 ? "s" : ""}
        </span>
      </div>

      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {datasets.map((dataset) => (
          <DatasetCard
            key={dataset.id}
            dataset={dataset}
          />
        ))}
      </div>

    </section>
  );
}

export default SearchResults;