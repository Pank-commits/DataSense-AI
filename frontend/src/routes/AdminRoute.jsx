import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function AdminRoute({ children }) {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950">
        <h1 className="text-2xl text-white">
          Loading...
        </h1>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Change this check to match your backend's user model.
  // For example, if your API returns `role: "admin"`.
  if (user.role !== "admin") {
    return <Navigate to="/" replace />;
  }

  return children;
}

export default AdminRoute;