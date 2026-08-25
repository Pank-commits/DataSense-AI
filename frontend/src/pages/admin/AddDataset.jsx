import { useState } from "react";
import { useNavigate } from "react-router-dom";

import AdminLayout from "../../components/admin/AdminLayout";
import DatasetForm from "../../components/admin/DatasetForm";
import { createDataset } from "../../Services/datasetService";
import { useToast } from "../../context/ToastContext";

function AddDataset() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const showToast = useToast();

  const handleSubmit = async (formData) => {
    try {
      setLoading(true);

      await createDataset(formData);

      showToast("Dataset added successfully!");

      navigate("/admin/datasets");
    } catch (error) {
      console.error("Error creating dataset:", error);

      const message =
        error.response?.data?.detail || "Failed to add dataset.";

      showToast(message, "error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AdminLayout>
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white">
          Add Dataset
        </h1>

        <p className="mt-2 text-slate-400">
          Create a new dataset in the platform.
        </p>
      </div>

      <DatasetForm
        onSubmit={handleSubmit}
        loading={loading}
      />
    </AdminLayout>
  );
}

export default AddDataset;
