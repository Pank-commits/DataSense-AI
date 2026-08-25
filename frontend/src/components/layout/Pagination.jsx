import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

function Pagination({
  page,
  totalPages,
  onPageChange,
}) {
  if (totalPages <= 1) return null;

  const pages = Array.from(
    { length: totalPages },
    (_, index) => index + 1
  );

  return (
    <div className="mt-10 flex flex-wrap items-center justify-center gap-3">

      <button
        onClick={() => onPageChange(page - 1)}
        disabled={page === 1}
        className="flex items-center gap-2 rounded-xl border border-slate-700 px-4 py-2 text-white transition hover:border-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
      >
        <FaChevronLeft />
        Previous
      </button>

      {pages.map((pageNumber) => (
        <button
          key={pageNumber}
          onClick={() => onPageChange(pageNumber)}
          className={`h-10 w-10 rounded-lg font-semibold transition ${
            page === pageNumber
              ? "bg-cyan-500 text-white"
              : "border border-slate-700 text-white hover:border-cyan-400"
          }`}
        >
          {pageNumber}
        </button>
      ))}

      <button
        onClick={() => onPageChange(page + 1)}
        disabled={page === totalPages}
        className="flex items-center gap-2 rounded-xl border border-slate-700 px-4 py-2 text-white transition hover:border-cyan-400 disabled:cursor-not-allowed disabled:opacity-40"
      >
        Next
        <FaChevronRight />
      </button>

    </div>
  );
}

export default Pagination;