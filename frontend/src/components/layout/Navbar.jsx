import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { FaBrain, FaBars, FaTimes } from "react-icons/fa";

import { useAuth } from "../../context/AuthContext";

function Navbar() {

    const [menuOpen, setMenuOpen] = useState(false);

    const {
        isAuthenticated,
        user,
        logout,
    } = useAuth();

    const navLinkClass = ({ isActive }) =>
        isActive
            ? "text-cyan-400 font-semibold"
            : "text-slate-300 hover:text-cyan-400 transition";

    return (

        <nav className="fixed top-0 left-0 w-full z-50 bg-slate-950/90 backdrop-blur-lg border-b border-slate-800">

            <div className="max-w-7xl mx-auto flex justify-between items-center px-6 py-4">

                {/* Logo */}

                <Link
                    to="/"
                    className="flex items-center gap-3"
                >

                    <div className="bg-cyan-500 p-2 rounded-xl shadow-lg shadow-cyan-500/40">

                        <FaBrain className="text-white text-xl" />

                    </div>

                    <h1 className="text-2xl font-bold text-white">

                        Data<span className="text-cyan-400">Sense AI</span>

                    </h1>

                </Link>

                {/* Desktop Navigation */}

                <div className="hidden md:flex items-center gap-10">

                    <NavLink
                        to="/"
                        className={navLinkClass}
                    >
                        Home
                    </NavLink>

                    <NavLink
                        to="/datasets"
                        className={navLinkClass}
                    >
                        Datasets
                    </NavLink>

                    <NavLink
                        to="/ai"
                        className={navLinkClass}
                    >
                        AI Assistant
                    </NavLink>

                    <NavLink
                        to="/about"
                        className={navLinkClass}
                    >
                        About
                    </NavLink>

                </div>

                {/* Desktop Authentication */}

                <div className="hidden md:flex items-center gap-4">

                    {isAuthenticated ? (

                        <>
                            <span className="text-cyan-400 font-medium">

                                Hello, {user?.full_name}

                            </span>

                            <button
                                onClick={logout}
                                className="bg-red-500 hover:bg-red-600 px-5 py-2 rounded-xl text-white font-semibold transition"
                            >
                                Logout
                            </button>
                        </>

                    ) : (

                        <>
                            <Link
                                to="/login"
                                className="text-slate-300 hover:text-cyan-400 transition"
                            >
                                Login
                            </Link>

                            <Link
                                to="/register"
                                className="bg-cyan-500 hover:bg-cyan-400 px-5 py-2 rounded-xl font-semibold transition"
                            >
                                Register
                            </Link>
                        </>

                    )}

                </div>

                {/* Mobile Menu Button */}

                <button
                    className="md:hidden text-white text-2xl"
                    onClick={() => setMenuOpen(!menuOpen)}
                >

                    {menuOpen ? <FaTimes /> : <FaBars />}

                </button>

            </div>

            {/* Mobile Menu */}

            {menuOpen && (

                <div className="md:hidden bg-slate-900 border-t border-slate-800">

                    <div className="flex flex-col px-6 py-6 gap-5">

                        <NavLink
                            to="/"
                            className={navLinkClass}
                            onClick={() => setMenuOpen(false)}
                        >
                            Home
                        </NavLink>

                        <NavLink
                            to="/datasets"
                            className={navLinkClass}
                            onClick={() => setMenuOpen(false)}
                        >
                            Datasets
                        </NavLink>

                        <NavLink
                            to="/ai"
                            className={navLinkClass}
                            onClick={() => setMenuOpen(false)}
                        >
                            AI Assistant
                        </NavLink>

                        <NavLink
                            to="/about"
                            className={navLinkClass}
                            onClick={() => setMenuOpen(false)}
                        >
                            About
                        </NavLink>

                        {isAuthenticated ? (

                            <>
                                <div className="text-cyan-400">

                                    {user?.full_name}

                                </div>

                                <button
                                    onClick={() => {

                                        logout();

                                        setMenuOpen(false);

                                    }}
                                    className="bg-red-500 rounded-xl py-3 text-white font-semibold"
                                >
                                    Logout
                                </button>
                            </>

                        ) : (

                            <>
                                <Link
                                    to="/login"
                                    onClick={() => setMenuOpen(false)}
                                    className="bg-cyan-500 text-center rounded-xl py-3 font-semibold"
                                >
                                    Login
                                </Link>

                                <Link
                                    to="/register"
                                    onClick={() => setMenuOpen(false)}
                                    className="bg-green-500 text-center rounded-xl py-3 font-semibold"
                                >
                                    Register
                                </Link>
                            </>

                        )}

                    </div>

                </div>

            )}

        </nav>

    );

}

export default Navbar;
