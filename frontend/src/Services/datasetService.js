import api from "./api";

// ==========================
// GET ALL DATASETS
// ==========================
export const getDatasets = async (params = {}) => {
  try {
    const response = await api.get("/datasets", { params });
    return response.data;
  } catch (error) {
    console.error("Error fetching datasets:", error);
    throw error;
  }
};

// ==========================
// GET DATASET BY SLUG
// ==========================
export const getDatasetBySlug = async (slug) => {
  try {
    const response = await api.get(`/datasets/${slug}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching dataset:", error);
    throw error;
  }
};

// ==========================
// CREATE DATASET
// ==========================
export const createDataset = async (dataset) => {
  try {
    const response = await api.post("/datasets", dataset);
    return response.data;
  } catch (error) {
    console.error("Error creating dataset:", error);
    throw error;
  }
};

// ==========================
// UPDATE DATASET
// ==========================
export const updateDataset = async (slug, dataset) => {
  try {
    const response = await api.put(`/datasets/${slug}`, dataset);
    return response.data;
  } catch (error) {
    console.error("Error updating dataset:", error);
    throw error;
  }
};

// ==========================
// DELETE DATASET
// ==========================
export const deleteDataset = async (slug) => {
  try {
    const response = await api.delete(`/datasets/${slug}`);
    return response.data;
  } catch (error) {
    console.error("Error deleting dataset:", error);
    throw error;
  }
};