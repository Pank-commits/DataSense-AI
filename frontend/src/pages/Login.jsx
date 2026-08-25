import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const REDIRECT_DELAY_MS = 900;

const Login = () => {

    const navigate = useNavigate();

    const {
        login,
        isAuthenticated,
    } = useAuth();

    const [formData, setFormData] = useState({
        email: "",
        password: "",
    });

    const [loading, setLoading] = useState(false);

    const [feedback, setFeedback] = useState({
        type: "",
        message: "",
    });

    useEffect(() => {

        if (isAuthenticated) {

            const redirectTimer = window.setTimeout(() => {

                navigate("/", { replace: true });

            }, REDIRECT_DELAY_MS);

            return () => window.clearTimeout(redirectTimer);

        }

    }, [isAuthenticated, navigate]);

    const handleChange = (e) => {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        setLoading(true);

        setFeedback({
            type: "",
            message: "",
        });

        const response = await login(formData);
        const isSuccess = response.success ?? !!response.access_token;

        if (isSuccess) {

            setFeedback({
                type: "success",
                message: "Login successful. Redirecting to home...",
            });

        } else {

            setFeedback({
                type: "error",
                message: response.message || "Invalid email or password.",
            });

        }

        setLoading(false);

    };

    return (

        <div className="min-h-screen flex items-center justify-center bg-gray-100">

            <div className="w-full max-w-md bg-white shadow-lg rounded-xl p-8">

                <h1 className="text-3xl font-bold text-center mb-6">

                    Login

                </h1>

                {feedback.message && (

                    <div
                        className={`mb-4 rounded-lg border px-4 py-3 text-sm font-medium ${
                            feedback.type === "success"
                                ? "border-emerald-200 bg-emerald-50 text-emerald-700"
                                : "border-red-200 bg-red-50 text-red-700"
                        }`}
                    >

                        {feedback.message}

                    </div>

                )}

                <form
                    onSubmit={handleSubmit}
                    className="space-y-5"
                >

                    <div>

                        <label className="block mb-2 font-medium">

                            Email

                        </label>

                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter your email"
                            required
                        />

                    </div>

                    <div>

                        <label className="block mb-2 font-medium">

                            Password

                        </label>

                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Enter your password"
                            required
                        />

                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-lg bg-blue-600 py-2 text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
                    >

                        {loading ? "Logging in..." : "Login"}

                    </button>

                </form>

                <p className="text-center mt-6">

                    Don't have an account?

                    <Link
                        to="/register"
                        className="text-blue-600 font-semibold ml-2"
                    >

                        Register

                    </Link>

                </p>

            </div>

        </div>

    );

};

export default Login;
