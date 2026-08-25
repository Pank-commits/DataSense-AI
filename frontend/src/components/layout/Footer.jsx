import {
  FaBrain,
  FaGithub,
  FaLinkedin,
  FaEnvelope,
} from "react-icons/fa";

function Footer() {
  return (
    <footer className="bg-slate-900 border-t border-slate-800">

      <div className="max-w-7xl mx-auto px-6 py-16">

        <div className="grid md:grid-cols-3 gap-10">

          {/* Logo */}

          <div>

            <div className="flex items-center gap-3">

              <div className="bg-cyan-500 p-3 rounded-xl">

                <FaBrain className="text-white text-xl" />

              </div>

              <h2 className="text-2xl font-bold text-white">

                Data<span className="text-cyan-400">Sense AI</span>

              </h2>

            </div>

            <p className="text-slate-400 mt-5 leading-7">

              AI Powered Dataset Discovery Platform built for
              Machine Learning, Deep Learning,
              Data Science and Artificial Intelligence.

            </p>

          </div>

          {/* Links */}

          <div>

            <h3 className="text-white text-xl font-bold mb-5">

              Quick Links

            </h3>

            <ul className="space-y-3">

              <li>
                <a
                  href="/"
                  className="text-slate-400 hover:text-cyan-400 transition"
                >
                  Home
                </a>
              </li>

              <li>
                <a
                  href="/datasets"
                  className="text-slate-400 hover:text-cyan-400 transition"
                >
                  Datasets
                </a>
              </li>

              <li>
                <a
                  href="/about"
                  className="text-slate-400 hover:text-cyan-400 transition"
                >
                  About
                </a>
              </li>

            </ul>

          </div>

          {/* Social */}

          <div>

            <h3 className="text-white text-xl font-bold mb-5">

              Connect

            </h3>

            <div className="flex gap-5 text-2xl">

              <FaGithub className="text-cyan-400 hover:text-white cursor-pointer transition" />

              <FaLinkedin className="text-cyan-400 hover:text-white cursor-pointer transition" />

              <FaEnvelope className="text-cyan-400 hover:text-white cursor-pointer transition" />

            </div>

          </div>

        </div>

        <div className="border-t border-slate-800 mt-12 pt-8 text-center text-slate-500">

          © 2026 DataSense AI | Built with React • FastAPI • PostgreSQL

        </div>

      </div>

    </footer>
  );
}

export default Footer;