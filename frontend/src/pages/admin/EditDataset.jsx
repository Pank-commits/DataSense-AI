import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import AdminLayout from "../../components/admin/AdminLayout";
import DatasetForm from "../../components/admin/DatasetForm";

import { getDatasetBySlug } from "../../Services/datasetService";
import { updateDataset } from "../../Services/adminService";
import { useToast } from "../../context/ToastContext";

function EditDataset() {
  const { slug } = useParams();
  const navigate = useNavigate();

  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const showToast = useToast();

  useEffect(() => {
    loadDataset();
  }, [slug]);

  const loadDataset = async () => {
    try {
      const data = await getDatasetBySlug(slug);
      setDataset(data);
    } catch (error) {
      console.error(error);
      showToast("Failed to load dataset.", "error");
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (formData) => {
    try {
      setSaving(true);

      await updateDataset(slug, formData);

      showToast("Dataset updated successfully!");

      navigate("/admin/datasets");
    } catch (error) {
      console.error(error);
      showToast("Failed to update dataset.", "error");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <AdminLayout>
        <div className="animate-pulse space-y-6 rounded-2xl border border-slate-800 bg-slate-900 p-8" aria-label="Loading dataset"><div className="h-8 w-1/3 rounded bg-slate-800" /><div className="h-12 rounded bg-slate-800" /><div className="h-32 rounded bg-slate-800" /></div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>

      <div className="mb-8">

        <h1 className="text-4xl font-bold text-white">
          Edit Dataset
        </h1>

        <p className="mt-2 text-slate-400">
          Update dataset information.
        </p>

      </div>

      <DatasetForm
        initialData={dataset}
        onSubmit={handleSubmit}
        loading={saving}
      />

    </AdminLayout>
  );
}

export default EditDataset;
