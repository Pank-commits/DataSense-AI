function LoadingSkeleton() {
  return (
    <div className="grid md:grid-cols-2 xl:grid-cols-3 gap-8">

      {Array.from({ length: 6 }).map((_, index) => (

        <div
          key={index}
          className="bg-slate-900 rounded-3xl overflow-hidden border border-slate-800 animate-pulse"
        >

          <div className="h-48 bg-slate-800/80"></div>

          <div className="p-6">

            <div className="h-7 bg-slate-800 rounded mb-5 w-4/5"></div>

            <div className="h-4 bg-slate-800 rounded mb-3"></div>

            <div className="h-4 bg-slate-800 rounded mb-3"></div>

            <div className="h-4 bg-slate-800 rounded w-2/3"></div>

            <div className="grid grid-cols-2 gap-3 mt-8">

              <div className="h-10 bg-slate-800 rounded"></div>

              <div className="h-10 bg-slate-800 rounded"></div>

              <div className="h-10 bg-slate-800 rounded"></div>

              <div className="h-10 bg-slate-800 rounded"></div>

            </div>

            <div className="flex gap-2 mt-6">

              <div className="h-8 w-16 bg-slate-800 rounded-full"></div>

              <div className="h-8 w-16 bg-slate-800 rounded-full"></div>

              <div className="h-8 w-16 bg-slate-800 rounded-full"></div>

            </div>

            <div className="flex justify-between mt-8">

              <div className="h-10 w-24 bg-slate-800 rounded"></div>

              <div className="h-10 w-24 bg-slate-800 rounded"></div>

            </div>

          </div>

        </div>

      ))}

    </div>
  );
}

export default LoadingSkeleton;
