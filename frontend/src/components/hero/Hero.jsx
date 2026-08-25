import { Link } from "react-router-dom";
import {
  FaArrowRight,
  FaDatabase,
  FaIdBadge,
  FaRobot,
  FaSearch,
  FaStar,
} from "react-icons/fa";

import { useAuth } from "../../context/AuthContext";

function Hero() {
  const { isAuthenticated, user } = useAuth();

  const displayName =
    user?.full_name ||
    user?.name ||
    user?.username ||
    user?.email ||
    (user?.id ? `User #${user.id}` : "");

  return (
    <section className="relative min-h-screen bg-slate-950 overflow-hidden">

      {/* Background Glow */}
      <div className="absolute top-20 left-10 w-80 h-80 bg-cyan-500/20 blur-[140px] rounded-full"></div>
      <div className="absolute bottom-10 right-10 w-80 h-80 bg-blue-500/20 blur-[140px] rounded-full"></div>

      <div className="relative max-w-7xl mx-auto px-6 pt-40 pb-24">

        {isAuthenticated && displayName && (
          <div className="mb-10 flex justify-end">
            <div className="inline-flex items-center gap-3 rounded-2xl border border-emerald-400/30 bg-emerald-500/10 px-4 py-3 text-emerald-300 shadow-lg shadow-emerald-950/40 backdrop-blur">
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-400/15 text-emerald-200">
                <FaIdBadge className="text-lg" />
              </div>

              <div className="text-right">
                <p className="flex items-center justify-end gap-2 text-xs font-semibold uppercase tracking-[0.2em] text-emerald-200/80">
                  <FaStar className="text-[10px]" />
                  Signed In
                </p>
                <p className="max-w-[240px] truncate text-sm font-semibold text-white">
                  {displayName}
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Badge */}
        <div className="flex justify-center">

          <span className="px-5 py-2 rounded-full border border-cyan-500/30 bg-cyan-500/10 text-cyan-400 font-semibold">

            🚀 AI Powered Dataset Discovery Platform

          </span>

        </div>

        {/* Heading */}

        <h1 className="text-center mt-8 text-6xl md:text-7xl font-extrabold text-white leading-tight">

          Discover

          <span className="block bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent">

            Machine Learning Datasets

          </span>

        </h1>

        {/* Subtitle */}

        <p className="max-w-3xl mx-auto text-center text-slate-400 text-xl leading-9 mt-8">

          Search thousands of datasets for Artificial Intelligence,
          Machine Learning, Deep Learning, NLP,
          Computer Vision and Data Analytics.

        </p>

        {/* Search */}

        <div className="max-w-3xl mx-auto mt-12">

          <div className="flex bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden shadow-xl">

            <input
              type="text"
              placeholder="Search datasets..."
              className="flex-1 bg-transparent px-6 py-5 text-white outline-none"
            />

            <button className="bg-cyan-500 hover:bg-cyan-400 px-8 transition">

              <FaSearch className="text-white text-xl" />

            </button>

          </div>

        </div>

        {/* Buttons */}

        <div className="flex justify-center gap-5 mt-10 flex-wrap">

          <Link
            to="/datasets"
            className="bg-cyan-500 hover:bg-cyan-400 px-8 py-4 rounded-xl font-semibold text-white flex items-center gap-3 transition"
          >

            Browse Datasets

            <FaArrowRight />

          </Link>

          <Link
            to="/about"
            className="border border-slate-700 hover:border-cyan-400 px-8 py-4 rounded-xl font-semibold text-white transition"
          >

            Learn More

          </Link>

        </div>

        {/* Stats */}

        <div className="grid md:grid-cols-3 gap-8 mt-24">

          <div className="bg-slate-900 rounded-3xl border border-slate-800 p-8 hover:border-cyan-400 transition">

            <FaDatabase className="text-5xl text-cyan-400 mb-6" />

            <h2 className="text-4xl font-bold text-white">

              5000+

            </h2>

            <p className="text-slate-400 mt-3">

              Curated Datasets

            </p>

          </div>

          <div className="bg-slate-900 rounded-3xl border border-slate-800 p-8 hover:border-cyan-400 transition">

            <FaRobot className="text-5xl text-cyan-400 mb-6" />

            <h2 className="text-4xl font-bold text-white">

              AI Powered

            </h2>

            <p className="text-slate-400 mt-3">

              Smart Recommendation

            </p>

          </div>

          <div className="bg-slate-900 rounded-3xl border border-slate-800 p-8 hover:border-cyan-400 transition">

            <FaSearch className="text-5xl text-cyan-400 mb-6" />

            <h2 className="text-4xl font-bold text-white">

              Instant

            </h2>

            <p className="text-slate-400 mt-3">

              Search Experience

            </p>

          </div>

        </div>

      </div>

    </section>
  );
}

export default Hero;
