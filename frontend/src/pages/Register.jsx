import { useEffect, useRef, useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const REDIRECT_DELAY_MS = 1200;

const Register = () => {

    const navigate = useNavigate();

    const { register } = useAuth();

    const [formData, setFormData] = useState({
        full_name: "",
        email: "",
        password: "",
        confirmPassword: "",
    });

    const [loading, setLoading] = useState(false);

    const [feedback, setFeedback] = useState({
        type: "",
        message: "",
    });

    const redirectTimerRef = useRef(null);

    useEffect(() => {

        return () => {

            window.clearTimeout(window.__registerRedirectTimer__);
            window.clearTimeout(redirectTimerRef.current);

        };

    }, []);

    const handleChange = (e) => {

        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });

    };

    const handleSubmit = async (e) => {

        e.preventDefault();

        setFeedback({
            type: "",
            message: "",
        });

        if (formData.password !== formData.confirmPassword) {

            setFeedback({
                type: "error",
                message: "Passwords do not match.",
            });

            return;

        }

        setLoading(true);

        const response = await register({
            full_name: formData.full_name,
            email: formData.email,
            password: formData.password,
        });
        const isSuccess = response.success ?? !!response.access_token;

        if (isSuccess) {

            setFeedback({
                type: "success",
                message: "Registration successful. Redirecting to home...",
            });

            redirectTimerRef.current = window.setTimeout(() => {

                navigate("/", { replace: true });

            }, REDIRECT_DELAY_MS);

        } else {

            setFeedback({
                type: "error",
                message: response.message || "Unable to register. Please try again.",
            });

        }

        setLoading(false);

    };

    return (

        <div className="min-h-screen flex items-center justify-center bg-gray-100">

            <div className="w-full max-w-md bg-white rounded-xl shadow-lg p-8">

                <h1 className="text-3xl font-bold text-center mb-6">

                    Create Account

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

                        <label className="block mb-2">

                            Full Name

                        </label>

                        <input
                            type="text"
                            name="full_name"
                            value={formData.full_name}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-4 py-2"
                            required
                        />

                    </div>

                    <div>

                        <label className="block mb-2">

                            Email

                        </label>

                        <input
                            type="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-4 py-2"
                            required
                        />

                    </div>

                    <div>

                        <label className="block mb-2">

                            Password

                        </label>

                        <input
                            type="password"
                            name="password"
                            value={formData.password}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-4 py-2"
                            required
                        />

                    </div>

                    <div>

                        <label className="block mb-2">

                            Confirm Password

                        </label>

                        <input
                            type="password"
                            name="confirmPassword"
                            value={formData.confirmPassword}
                            onChange={handleChange}
                            className="w-full border rounded-lg px-4 py-2"
                            required
                        />

                    </div>

                    <button
                        type="submit"
                        disabled={loading}
                        className="w-full rounded-lg bg-green-600 py-2 text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:bg-green-400"
                    >

                        {loading ? "Creating Account..." : "Register"}

                    </button>

                </form>

                <p className="text-center mt-6">

                    Already have an account?

                    <Link
                        to="/login"
                        className="ml-2 text-blue-600 font-semibold"
                    >

                        Login

                    </Link>

                </p>

            </div>

        </div>

    );

};

export default Register;
