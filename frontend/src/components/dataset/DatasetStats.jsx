import {
  FaTable,
  FaColumns,
  FaDownload,
  FaStar,
  FaDatabase,
  FaRobot,
} from "react-icons/fa";

function DatasetStats({ dataset }) {
  const stats = [
    {
      title: "Rows",
      value: dataset.rows?.toLocaleString(),
      icon: <FaTable />,
    },
    {
      title: "Columns",
      value: dataset.columns,
      icon: <FaColumns />,
    },
    {
      title: "Downloads",
      value: dataset.downloads?.toLocaleString(),
      icon: <FaDownload />,
    },
    {
      title: "Rating",
      value: dataset.rating,
      icon: <FaStar />,
    },
    {
      title: "Data Type",
      value: dataset.data_type,
      icon: <FaDatabase />,
    },
    {
      title: "ML Task",
      value: dataset.ml_task,
      icon: <FaRobot />,
    },
  ];

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900 p-8">

      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white">
          Dataset Statistics
        </h2>

        <p className="mt-2 text-slate-400">
          Quick overview of the dataset.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">

        {stats.map((stat) => (
          <div
            key={stat.title}
            className="rounded-2xl border border-slate-800 bg-slate-950 p-6 transition hover:border-cyan-400"
          >
            <div className="mb-4 text-3xl text-cyan-400">
              {stat.icon}
            </div>

            <p className="text-sm text-slate-400">
              {stat.title}
            </p>

            <h3 className="mt-2 text-2xl font-bold text-white">
              {stat.value}
            </h3>
          </div>
        ))}

      </div>

    </section>
  );
}

export default DatasetStats;