import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import Navbar from "../components/layout/Navbar";

import DatasetHero from "../components/dataset/DatasetHero";
import DatasetDescription from "../components/dataset/DatasetDescription";
import DatasetStats from "../components/dataset/DatasetStats";
import DatasetTags from "../components/dataset/DatasetTags";
import DatasetActions from "../components/dataset/DatasetActions";
import RelatedDatasets from "../components/dataset/RelatedDatasets";

import { getDatasetBySlug } from "../Services/datasetService";

function DatasetDetails() {
  const { slug } = useParams();

  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadDataset();
  }, [slug]);

  const loadDataset = async () => {
    try {
      setLoading(true);
      setError("");

      const data = await getDatasetBySlug(slug);

      setDataset(data);
    } catch (err) {
      console.error(err);
      setError("Failed to load dataset.");
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-slate-950 flex items-center justify-center">
          <h2 className="text-2xl font-semibold text-white">
            Loading dataset...
          </h2>
        </div>
      </>
    );
  }

  if (error || !dataset) {
    return (
      <>
        <Navbar />
        <div className="min-h-screen bg-slate-950 flex items-center justify-center">
          <h2 className="text-2xl font-semibold text-red-400">
            {error || "Dataset not found"}
          </h2>
        </div>
      </>
    );
  }

  return (
    <>
      <Navbar />

      <main className="min-h-screen bg-slate-950">

        <DatasetHero dataset={dataset} />

        <div className="mx-auto max-w-7xl space-y-10 px-6 py-12">

          <DatasetDescription dataset={dataset} />

          <DatasetStats dataset={dataset} />

          <DatasetTags dataset={dataset} />

          <DatasetActions dataset={dataset} />

          <RelatedDatasets currentDataset={dataset} />

        </div>

      </main>

    </>
  );
}

export default DatasetDetails;
