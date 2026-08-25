import { useEffect, useState } from "react";
import {
  FaDatabase,
  FaFolderOpen,
  FaDownload,
  FaStar,
} from "react-icons/fa";

import AdminLayout from "../../components/admin/AdminLayout";
import StatsCard from "../../components/admin/StatsCard";
import DashboardCharts from "../../components/admin/DashboardCharts";
import { getDashboardStats } from "../../Services/dashboardService";

function Dashboard() {
  const [loading, setLoading] = useState(true);

  const [stats, setStats] = useState({
    totalDatasets: 0,
    totalCategories: 0,
    totalDownloads: 0,
    averageRating: 0,
  });

  const [recentDatasets, setRecentDatasets] = useState([]);
  const [topRatedDatasets, setTopRatedDatasets] = useState([]);
  const [categoryData, setCategoryData] = useState([]);
  const [mlTaskData, setMlTaskData] = useState([]);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const data = await getDashboardStats();

      setStats({
        totalDatasets: data.total_datasets,
        totalCategories: data.total_categories,
        totalDownloads: data.total_downloads,
        averageRating: data.average_rating,
      });

      setRecentDatasets(data.recent_datasets || []);
      setTopRatedDatasets(data.top_rated_datasets || []);
      setCategoryData(data.category_stats || []);
      setMlTaskData(data.ml_task_stats || []);
    } catch (error) {
      console.error("Dashboard Error:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-96">
          <p className="text-xl text-white">Loading Dashboard...</p>
        </div>
      </AdminLayout>
    );
  }

  return (
    <AdminLayout>
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-white">Dashboard</h1>
        <p className="mt-2 text-slate-400">
          Overview of your dataset platform.
        </p>
      </div>

      {/* Stats */}
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <StatsCard
          title="Datasets"
          value={stats.totalDatasets}
          icon={<FaDatabase />}
        />

        <StatsCard
          title="Categories"
          value={stats.totalCategories}
          icon={<FaFolderOpen />}
        />

        <StatsCard
          title="Downloads"
          value={stats.totalDownloads.toLocaleString()}
          icon={<FaDownload />}
        />

        <StatsCard
          title="Average Rating"
          value={stats.averageRating}
          icon={<FaStar />}
        />
      </div>

      {/* Charts */}
      <DashboardCharts
        categoryData={categoryData}
        mlTaskData={mlTaskData}
      />

      {/* Recent Datasets */}
      <div className="mt-10 rounded-2xl border border-slate-700 bg-slate-900 shadow-lg p-6">

        <h2 className="mb-6 text-3xl font-bold text-white">
          Recent Datasets
        </h2>

        <div className="overflow-x-auto">
          <table className="min-w-full">

            <thead className="border-b border-slate-700">
              <tr>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Name
                </th>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Category
                </th>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Task
                </th>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Downloads
                </th>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Rating
                </th>

              </tr>
            </thead>

            <tbody>

              {recentDatasets.map((dataset) => (

                <tr
                  key={dataset.slug}
                  className="border-b border-slate-800 hover:bg-slate-800 transition-colors"
                >

                  <td className="px-4 py-4 text-white font-medium">
                    {dataset.name}
                  </td>

                  <td className="px-4 py-4 text-slate-300">
                    {dataset.category}
                  </td>

                  <td className="px-4 py-4 text-slate-300">
                    {dataset.ml_task}
                  </td>

                  <td className="px-4 py-4 text-cyan-400 font-semibold">
                    {dataset.downloads.toLocaleString()}
                  </td>

                  <td className="px-4 py-4 text-yellow-400 font-semibold">
                    ⭐ {dataset.rating}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>
        </div>
      </div>

      {/* Top Rated */}
      <div className="mt-10 rounded-2xl border border-slate-700 bg-slate-900 shadow-lg p-6">

        <h2 className="mb-6 text-3xl font-bold text-white">
          Top Rated Datasets
        </h2>

        <div className="overflow-x-auto">

          <table className="min-w-full">

            <thead className="border-b border-slate-700">
              <tr>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Name
                </th>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Category
                </th>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Downloads
                </th>

                <th className="px-4 py-3 text-left text-slate-300 font-semibold">
                  Rating
                </th>

              </tr>
            </thead>

            <tbody>

              {topRatedDatasets.map((dataset) => (

                <tr
                  key={dataset.slug}
                  className="border-b border-slate-800 hover:bg-slate-800 transition-colors"
                >

                  <td className="px-4 py-4 text-white font-medium">
                    {dataset.name}
                  </td>

                  <td className="px-4 py-4 text-slate-300">
                    {dataset.category}
                  </td>

                  <td className="px-4 py-4 text-cyan-400 font-semibold">
                    {dataset.downloads.toLocaleString()}
                  </td>

                  <td className="px-4 py-4 text-yellow-400 font-semibold">
                    ⭐ {dataset.rating}
                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>
      </div>

    </AdminLayout>
  );
}

export default Dashboard;