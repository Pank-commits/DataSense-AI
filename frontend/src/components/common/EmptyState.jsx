import { FaDatabase } from "react-icons/fa";

function EmptyState() {

  return (

    <div className="text-center py-24">

      <FaDatabase className="text-7xl text-slate-600 mx-auto mb-8" />

      <h2 className="text-4xl text-white font-bold">

        No Datasets Found

      </h2>

      <p className="text-slate-400 mt-4 text-lg">

        Try changing your search or filters.

      </p>

    </div>

  );

}

export default EmptyState;