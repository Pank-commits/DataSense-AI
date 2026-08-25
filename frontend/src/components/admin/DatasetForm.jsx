import { useState, useEffect } from "react";

function DatasetForm({ initialData = {}, onSubmit, loading }) {
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    category: "",
    ml_task: "",
    data_type: "",
    difficulty: "",
    source: "",
    download_url: "",
    license: "",
    rows: "",
    columns: "",
    file_size: "",
    target_column: "",
    language: "",
    tags: "",
    thumbnail: "",
  });

  useEffect(() => {
    if (Object.keys(initialData).length > 0) {
      setFormData({
        name: initialData.name || "",
        description: initialData.description || "",
        category: initialData.category || "",
        ml_task: initialData.ml_task || "",
        data_type: initialData.data_type || "",
        difficulty: initialData.difficulty || "",
        source: initialData.source || "",
        download_url: initialData.download_url || "",
        license: initialData.license || "",
        rows: initialData.rows || "",
        columns: initialData.columns || "",
        file_size: initialData.file_size || "",
        target_column: initialData.target_column || "",
        language: initialData.language || "",
        tags: initialData.tags || "",
        thumbnail: initialData.thumbnail || "",
      });
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  const inputClass =
    "w-full rounded-lg border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-400";

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-6 rounded-2xl border border-slate-800 bg-slate-900 p-8"
    >
      <div className="grid gap-6 md:grid-cols-2">
        <div>
          <label className="mb-2 block text-slate-300">Dataset Name</label>
          <input
            name="name"
            value={formData.name}
            onChange={handleChange}
            className={inputClass}
            required
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Category</label>
          <input
            name="category"
            value={formData.category}
            onChange={handleChange}
            className={inputClass}
            required
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">ML Task</label>
          <input
            name="ml_task"
            value={formData.ml_task}
            onChange={handleChange}
            className={inputClass}
            required
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Data Type</label>
          <input
            name="data_type"
            value={formData.data_type}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Difficulty</label>
          <input
            name="difficulty"
            value={formData.difficulty}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Source</label>
          <input
            name="source"
            value={formData.source}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Download URL</label>
          <input
            name="download_url"
            value={formData.download_url}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">License</label>
          <input
            name="license"
            value={formData.license}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Rows</label>
          <input
            type="number"
            name="rows"
            value={formData.rows}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Columns</label>
          <input
            type="number"
            name="columns"
            value={formData.columns}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">File Size</label>
          <input
            name="file_size"
            value={formData.file_size}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Target Column</label>
          <input
            name="target_column"
            value={formData.target_column}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Language</label>
          <input
            name="language"
            value={formData.language}
            onChange={handleChange}
            className={inputClass}
          />
        </div>

        <div>
          <label className="mb-2 block text-slate-300">Thumbnail URL</label>
          <input
            name="thumbnail"
            value={formData.thumbnail}
            onChange={handleChange}
            className={inputClass}
          />
        </div>
      </div>

      <div>
        <label className="mb-2 block text-slate-300">Tags</label>
        <input
          name="tags"
          value={formData.tags}
          onChange={handleChange}
          placeholder="ai,healthcare,classification"
          className={inputClass}
        />
      </div>

      <div>
        <label className="mb-2 block text-slate-300">Description</label>
        <textarea
          rows={6}
          name="description"
          value={formData.description}
          onChange={handleChange}
          className={inputClass}
          required
        />
      </div>

      <button
        type="submit"
        disabled={loading}
        className="rounded-lg bg-cyan-500 px-8 py-3 font-semibold text-white transition hover:bg-cyan-400 disabled:opacity-50"
      >
        {loading ? "Saving..." : "Save Dataset"}
      </button>
    </form>
  );
}

export default DatasetForm;