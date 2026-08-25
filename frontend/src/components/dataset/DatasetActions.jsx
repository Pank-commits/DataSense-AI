import { FaDownload, FaExternalLinkAlt, FaCopy, FaShareAlt } from "react-icons/fa";

function DatasetActions({ dataset }) {
  const copyLink = async () => {
    try {
      await navigator.clipboard.writeText(window.location.href);
      alert("Dataset link copied to clipboard!");
    } catch (error) {
      console.error(error);
      alert("Failed to copy link.");
    }
  };

  const shareDataset = async () => {
    if (navigator.share) {
      try {
        await navigator.share({
          title: dataset.name,
          text: dataset.description,
          url: window.location.href,
        });
      } catch (error) {
        console.error(error);
      }
    } else {
      copyLink();
    }
  };

  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900 p-8">

      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white">
          Quick Actions
        </h2>

        <p className="mt-2 text-slate-400">
          Download, share, or explore this dataset.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

        <a
          href={dataset.download_url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center gap-3 rounded-xl bg-cyan-500 px-6 py-4 font-semibold text-white transition hover:bg-cyan-400"
        >
          <FaDownload />
          Download
        </a>

        <a
          href={dataset.download_url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center justify-center gap-3 rounded-xl border border-slate-700 px-6 py-4 font-semibold text-white transition hover:border-cyan-400"
        >
          <FaExternalLinkAlt />
          Visit Source
        </a>

        <button
          onClick={copyLink}
          className="flex items-center justify-center gap-3 rounded-xl border border-slate-700 px-6 py-4 font-semibold text-white transition hover:border-cyan-400"
        >
          <FaCopy />
          Copy Link
        </button>

        <button
          onClick={shareDataset}
          className="flex items-center justify-center gap-3 rounded-xl border border-slate-700 px-6 py-4 font-semibold text-white transition hover:border-cyan-400"
        >
          <FaShareAlt />
          Share
        </button>

      </div>

    </section>
  );
}

export default DatasetActions;