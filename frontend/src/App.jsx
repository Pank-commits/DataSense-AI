import Footer from "./components/layout/Footer";
import Navbar from "./components/layout/Navbar";

import AppRoutes from "./routes/AppRoutes";
import { ToastProvider } from "./context/ToastContext";

function App() {
    return (
        <ToastProvider><div className="min-h-screen flex flex-col">

            <Navbar />

            <main className="flex-1">
                <AppRoutes />
            </main>

            <Footer />

        </div></ToastProvider>
    );
}

export default App;
