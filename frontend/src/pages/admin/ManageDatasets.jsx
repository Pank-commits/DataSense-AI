import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { FaPlus } from "react-icons/fa";

import AdminLayout from "../../components/admin/AdminLayout";
import DatasetTable from "../../components/admin/DatasetTable";
import { getDatasets } from "../../Services/datasetService";

function ManageDatasets() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      setLoading(true);

      const response = await getDatasets({
        limit: 1000,
      });

      setDatasets(response.items || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AdminLayout>

      <div className="mb-8 flex items-center justify-between">

        <div>
          <h1 className="text-4xl font-bold text-white">
            Manage Datasets
          </h1>

          <p className="mt-2 text-slate-400">
            Add, edit and delete datasets.
          </p>
        </div>

        <Link
          to="/admin/add-dataset"
          className="flex items-center gap-2 rounded-xl bg-cyan-500 px-6 py-3 font-semibold text-white hover:bg-cyan-400"
        >
          <FaPlus />
          Add Dataset
        </Link>

      </div>

      <DatasetTable
        datasets={datasets}
        loading={loading}
        refresh={loadDatasets}
      />

    </AdminLayout>
  );
}

export default ManageDatasets;