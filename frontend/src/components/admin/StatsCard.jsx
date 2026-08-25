function StatsCard({ title, value, icon }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">

      <div className="mb-5 text-4xl text-cyan-400">
        {icon}
      </div>

      <p className="text-slate-400">
        {title}
      </p>

      <h2 className="mt-2 text-4xl font-bold text-white">
        {value}
      </h2>

    </div>
  );
}

export default StatsCard;