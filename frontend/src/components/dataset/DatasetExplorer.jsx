import { useEffect, useState, useCallback } from "react";

import { getDatasets } from "../../Services/datasetService";

import SearchBar from "../search/SearchBar";
import SearchFilter from "../search/SearchFilter";
import SortBar from "../search/SortBar";
import SearchResults from "../search/SearchResults";
import Pagination from "../layout/Pagination";

function DatasetExplorer() {
  const [datasets, setDatasets] = useState([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState("");

  const [search, setSearch] = useState("");

  const [category, setCategory] = useState("");

  const [mlTask, setMlTask] = useState("");

  const [difficulty, setDifficulty] = useState("");

  const [dataType, setDataType] = useState("");

  const [sort, setSort] = useState("name");

  const [order, setOrder] = useState("asc");

  const [page, setPage] = useState(1);

  const [limit] = useState(6);

  const [total, setTotal] = useState(0);

  const [totalPages, setTotalPages] = useState(1);

  const loadDatasets = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const response = await getDatasets({
        search,
        category,
        ml_task: mlTask,
        difficulty,
        data_type: dataType,
        page,
        limit,
        sort,
        order,
      });

      setDatasets(response.items);

      setTotal(response.total);

      setTotalPages(response.total_pages);
    } catch (err) {
      console.error(err);

      setError("Failed to load datasets.");
    } finally {
      setLoading(false);
    }
  }, [
    search,
    category,
    mlTask,
    difficulty,
    dataType,
    page,
    limit,
    sort,
    order,
  ]);

  useEffect(() => {
    loadDatasets();
  }, [loadDatasets]);

  const handleSearch = () => {
    setPage(1);
    loadDatasets();
  };

  const handleClearSearch = () => {
    setSearch("");
    setPage(1);
  };

  const handleApplyFilters = () => {
    setPage(1);
    loadDatasets();
  };

  const handleResetFilters = () => {
    setCategory("");
    setMlTask("");
    setDifficulty("");
    setDataType("");
    setSearch("");
    setSort("name");
    setOrder("asc");
    setPage(1);
  };

  return (
    <section className="bg-slate-950 py-20">
      <div className="mx-auto max-w-7xl px-6">

        <div className="mb-10">

          <h2 className="text-4xl font-bold text-white">

            Explore Datasets

          </h2>

          <p className="mt-3 text-slate-400">

            Search thousands of AI, ML and Data Science datasets.

          </p>

        </div>

        <div className="space-y-8">

          <SearchBar
            value={search}
            onChange={setSearch}
            onSearch={handleSearch}
            onClear={handleClearSearch}
          />

          <SearchFilter
            category={category}
            setCategory={setCategory}
            mlTask={mlTask}
            setMlTask={setMlTask}
            difficulty={difficulty}
            setDifficulty={setDifficulty}
            dataType={dataType}
            setDataType={setDataType}
            onApply={handleApplyFilters}
            onReset={handleResetFilters}
          />

          <SortBar
            sort={sort}
            setSort={setSort}
            order={order}
            setOrder={setOrder}
          />

          <SearchResults
            datasets={datasets}
            loading={loading}
            error={error}
            total={total}
          />

          <Pagination
            page={page}
            totalPages={totalPages}
            onPageChange={setPage}
          />

        </div>
      </div>
    </section>
  );
}

export default DatasetExplorer;
