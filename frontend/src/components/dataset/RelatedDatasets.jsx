import { useEffect, useState } from "react";
import { getDatasets } from "../../Services/datasetService";
import DatasetCard from "./DatasetCard";

function RelatedDatasets({ currentDataset }) {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadRelatedDatasets();
  }, [currentDataset]);

  const loadRelatedDatasets = async () => {
    try {
      setLoading(true);

      const response = await getDatasets({
        category: currentDataset.category,
        limit: 4,
      });

      const related = response.items.filter(
        (dataset) => dataset.slug !== currentDataset.slug
      );

      setDatasets(related.slice(0, 3));
    } catch (error) {
      console.error("Error loading related datasets:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <section className="rounded-3xl border border-slate-800 bg-slate-900 p-8">
        <h2 className="text-3xl font-bold text-white">
          Related Datasets
        </h2>

        <p className="mt-6 text-slate-400">
          Loading related datasets...
        </p>
      </section>
    );
  }

  if (datasets.length === 0) {
    return null;
  }

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900 p-8">

      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white">
          Related Datasets
        </h2>

        <p className="mt-2 text-slate-400">
          Explore similar datasets in the same category.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
        {datasets.map((dataset) => (
          <DatasetCard
            key={dataset.slug}
            dataset={dataset}
          />
        ))}
      </div>

    </section>
  );
}

export default RelatedDatasets;
