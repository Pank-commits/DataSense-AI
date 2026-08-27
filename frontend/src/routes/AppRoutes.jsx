import { Routes, Route } from "react-router-dom";
import AIChat from "../components/AIChat/AIChat";
// Public Pages
import Home from "../pages/Home";
import Datasets from "../pages/Datasets";
import DatasetDetails from "../pages/DatasetDetails";
import Login from "../pages/Login";
import Register from "../pages/Register";
import About from "../pages/About";
import NotFound from "../pages/NotFound";
// Protected Route
import ProtectedRoute from "../components/common/ProtectedRoute";

// Admin Route
import AdminRoute from "./AdminRoute";

// Admin Pages
import Dashboard from "../pages/admin/Dashboard";
import ManageDatasets from "../pages/admin/ManageDatasets";
import AddDataset from "../pages/admin/AddDataset";
import EditDataset from "../pages/admin/EditDataset";

const AppRoutes = () => {
  return (
    <Routes>

      {/* ================= PUBLIC ROUTES ================= */}

      <Route
        path="/"
        element={<Home />}
      />
      <Route
        path="/datasets"
        element={<Datasets />}
      />

      <Route
        path="/datasets/:slug"
        element={<DatasetDetails />}
      />

      <Route
        path="/about"
        element={<About />}
      />

      <Route
        path="/login"
        element={<Login />}
      />

      <Route
        path="/register"
        element={<Register />}
      />

      {/* ================= USER PROTECTED ROUTES ================= */}

      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <div className="p-10 text-2xl">
              User Profile (Coming Soon)
            </div>
          </ProtectedRoute>
        }
      />

      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <div className="p-10 text-2xl">
              Dashboard (Coming Soon)
            </div>
          </ProtectedRoute>
        }
      />

      {/* ================= ADMIN ROUTES ================= */}

      <Route
        path="/admin/dashboard"
        element={
          <AdminRoute>
            <Dashboard />
          </AdminRoute>
        }
      />

      <Route
        path="/ai"
        element={
          <ProtectedRoute>
            <AIChat />
          </ProtectedRoute>
       }
      />

      <Route
        path="/admin/datasets"
        element={
          <AdminRoute>
            <ManageDatasets />
          </AdminRoute>
        }
      />

      <Route
        path="/admin/add-dataset"
        element={
          <AdminRoute>
            <AddDataset />
          </AdminRoute>
        }
      />

      <Route
        path="/admin/edit/:slug"
        element={
          <AdminRoute>
            <EditDataset />
          </AdminRoute>
        }
      />

      {/* ================= 404 ================= */}

      <Route
        path="*"
        element={<NotFound />}
      />

    </Routes>
  );
};

export default AppRoutes;
