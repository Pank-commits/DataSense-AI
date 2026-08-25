import api from "./api";

/**
 * Get complete dashboard statistics
 */
export const getDashboardStats = async () => {
  try {
    const response = await api.get("/dashboard/stats");
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard statistics:", error);
    throw error;
  }
};