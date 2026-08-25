import DatasetCard from "./DatasetCard";
import LoadingSkeleton from "../common/LoadingSkeleton";
import EmptyState from "../common/EmptyState";

function DatasetGrid({
  datasets,
  loading,
}) {

  if (loading) {

    return <LoadingSkeleton />;

  }

  if (datasets.length === 0) {

    return <EmptyState />;

  }

  return (

    <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-8">

      {datasets.map((dataset) => (

        <DatasetCard
          key={dataset.id}
          dataset={dataset}
        />

      ))}

    </div>

  );

}

export default DatasetGrid;