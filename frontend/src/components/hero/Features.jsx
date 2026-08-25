import {
  FaBrain,
  FaDatabase,
  FaDownload,
  FaFilter,
  FaRobot,
  FaSearch,
} from "react-icons/fa";

const features = [
  {
    icon: <FaDatabase />,
    title: "Massive Dataset Library",
    description:
      "Explore datasets from Healthcare, Finance, NLP, Computer Vision, Agriculture, IoT and many more.",
  },
  {
    icon: <FaRobot />,
    title: "AI Recommendation",
    description:
      "Get intelligent dataset recommendations based on your project and machine learning task.",
  },
  {
    icon: <FaSearch />,
    title: "Advanced Search",
    description:
      "Instantly search datasets using names, categories, tags, difficulty and ML tasks.",
  },
  {
    icon: <FaFilter />,
    title: "Smart Filters",
    description:
      "Filter datasets by category, source, language, difficulty and dataset type.",
  },
  {
    icon: <FaDownload />,
    title: "One Click Download",
    description:
      "Download datasets directly from trusted sources like Kaggle and UCI Repository.",
  },
  {
    icon: <FaBrain />,
    title: "Built For AI",
    description:
      "Designed especially for AI Engineers, Data Scientists, Researchers and Students.",
  },
];

function Features() {
  return (
    <section className="bg-slate-950 py-24">

      <div className="max-w-7xl mx-auto px-6">

        <div className="text-center">

          <h2 className="text-5xl font-bold text-white">

            Why Choose

            <span className="text-cyan-400">
              {" "}DataSense AI?
            </span>

          </h2>

          <p className="text-slate-400 mt-6 max-w-3xl mx-auto text-lg">

            Everything you need to discover the perfect dataset
            for Machine Learning and Artificial Intelligence.

          </p>

        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mt-20">

          {features.map((feature, index) => (

            <div
              key={index}
              className="group bg-slate-900 border border-slate-800 rounded-3xl p-8 hover:border-cyan-400 hover:-translate-y-2 transition-all duration-300"
            >

              <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 text-cyan-400 flex items-center justify-center text-3xl group-hover:bg-cyan-500 group-hover:text-white transition">

                {feature.icon}

              </div>

              <h3 className="text-white text-2xl font-semibold mt-8">

                {feature.title}

              </h3>

              <p className="text-slate-400 leading-7 mt-4">

                {feature.description}

              </p>

            </div>

          ))}

        </div>

      </div>

    </section>
  );
}

export default Features;