import { FaSearch, FaTimes } from "react-icons/fa";

function SearchBar({
  value,
  onChange,
  onSearch,
  onClear,
  placeholder = "Search datasets...",
  disabled = false,
}) {
  const handleSubmit = (e) => {
    e.preventDefault();

    if (!disabled && onSearch) {
      onSearch();
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Escape" && value && onClear) {
      onClear();
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="flex overflow-hidden rounded-2xl border border-slate-800 bg-slate-900 shadow-xl">

        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          aria-label="Search datasets"
          className="flex-1 bg-transparent px-6 py-4 text-white outline-none placeholder:text-slate-500 disabled:cursor-not-allowed disabled:opacity-60"
        />

        {value && (
          <button
            type="button"
            onClick={onClear}
            disabled={disabled}
            aria-label="Clear search"
            className="px-4 text-slate-400 transition hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            <FaTimes />
          </button>
        )}

        <button
          type="submit"
          disabled={disabled}
          aria-label="Search"
          className="bg-cyan-500 px-6 text-white transition hover:bg-cyan-400 disabled:cursor-not-allowed disabled:opacity-50"
        >
          <FaSearch />
        </button>

      </div>
    </form>
  );
}

export default SearchBar;