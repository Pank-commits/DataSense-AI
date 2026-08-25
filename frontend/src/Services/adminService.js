import api from "./api";

export const createDataset = async (dataset) => {
  const response = await api.post("/datasets", dataset);
  return response.data;
};

export const updateDataset = async (slug, dataset) => {
  const response = await api.put(`/datasets/${slug}`, dataset);
  return response.data;
};

export const deleteDataset = async (slug) => {
  const response = await api.delete(`/datasets/${slug}`);
  return response.data;
};