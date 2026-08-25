import { useEffect, useState, useCallback, useRef } from "react";

import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import Sidebar from "../components/layout/Sidebar";
import SearchBar from "../components/search/SearchBar";
import SortBar from "../components/search/SortBar";
import DatasetGrid from "../components/dataset/DatasetGrid";
import Pagination from "../components/layout/Pagination";

import {
  getDatasets,
} from "../Services/datasetService";

const PAGE_SIZE = 6;
const DEFAULT_QUERY = {
  search: "",
  category: "",
  ml_task: "",
  difficulty: "",
  data_type: "",
  page: 1,
  sort: "",
  order: "asc",
};

function Datasets() {
  const [datasets, setDatasets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchInput, setSearchInput] = useState("");
  const [queryState, setQueryState] = useState(DEFAULT_QUERY);
  const [totalPages, setTotalPages] = useState(1);
  const [totalResults, setTotalResults] = useState(0);
  const [error, setError] = useState("");
  const latestRequestRef = useRef(0);

  useEffect(() => {
    const timer = setTimeout(() => {
      setQueryState((prev) => {
        if (prev.search === searchInput) {
          return prev;
        }

        return {
          ...prev,
          search: searchInput,
          page: 1,
        };
      });
    }, 400);

    return () => clearTimeout(timer);
  }, [searchInput]);

  const loadDatasets = useCallback(async () => {
    const requestId = latestRequestRef.current + 1;
    latestRequestRef.current = requestId;
    setLoading(true);
    setError("");

    try {
      const response = await getDatasets({
        ...queryState,
        limit: PAGE_SIZE,
      });

      if (requestId !== latestRequestRef.current) {
        return;
      }

      setDatasets(response.items || []);
      setTotalPages(response.total_pages || 1);
      setTotalResults(response.total || 0);

      if (response.page && response.page !== queryState.page) {
        setQueryState((prev) => ({
          ...prev,
          page: response.page,
        }));
      }
    } catch (error) {
      if (requestId !== latestRequestRef.current) {
        return;
      }

      console.error(error);
      setError(error.response?.data?.detail || "Unable to load datasets. Please try again.");
    } finally {
      if (requestId === latestRequestRef.current) {
        setLoading(false);
      }
    }
  }, [queryState]);

  useEffect(() => {
    loadDatasets();
  }, [loadDatasets]);

  const updateQueryState = useCallback((updates) => {
    setQueryState((prev) => ({
      ...prev,
      ...updates,
    }));
  }, []);

  const handleFilterChange = useCallback((key, value) => {
    updateQueryState({
      [key]: value,
      page: 1,
    });
  }, [updateQueryState]);

  const clearFilters = useCallback(() => {
    setSearchInput("");
    setQueryState(DEFAULT_QUERY);
  }, []);

  const changePage = useCallback((page) => {
    updateQueryState({ page });
  }, [updateQueryState]);

  const handleSortChange = useCallback((sort) => {
    const descendingSorts = ["downloads", "rating", "rows"];

    updateQueryState({
      sort,
      order: descendingSorts.includes(sort) ? "desc" : "asc",
      page: 1,
    });
  }, [updateQueryState]);

  return (
    <>
      <Navbar />

      <div className="bg-slate-950 min-h-screen pt-28">

        <SearchBar
          value={searchInput}
          onChange={setSearchInput}
        />

        <div className="max-w-7xl mx-auto px-6 py-10">

          <div className="grid md:grid-cols-4 gap-8 items-start">

            <div className="md:col-span-1">
              <Sidebar
                filters={queryState}
                onFilterChange={handleFilterChange}
                onClear={clearFilters}
              />
            </div>

            <div className="md:col-span-3">

              <div className="flex justify-between items-center flex-wrap gap-4 mb-8">

                <h2 className="text-4xl font-bold text-white">
                  Explore Datasets
                </h2>

                <SortBar
                  sort={queryState.sort}
                  setSort={handleSortChange}
                  order={queryState.order}
                  setOrder={(nextOrder) =>
                    updateQueryState({
                      order: nextOrder,
                      page: 1,
                    })
                  }
                />

                <span className="text-slate-400">
                  {totalResults} Results
                </span>

              </div>

              <DatasetGrid
                datasets={datasets}
                loading={loading}
              />
              {error && <div className="mt-6 rounded-xl border border-red-400/30 bg-red-950/40 p-4 text-red-200">{error}</div>}

              <Pagination
                page={queryState.page}
                totalPages={totalPages}
                onPageChange={changePage}
              />

            </div>

          </div>

        </div>

        <Footer />

      </div>

    </>
  );
}

export default Datasets;
