import { createContext, useContext, useEffect, useState } from "react";

import {
    loginUser,
    registerUser,
    getCurrentUser,
} from "../services/authService";

const AuthContext = createContext();
const isAuthSuccess = (response) =>
    response?.success ?? !!response?.access_token;
const getUserFromResponse = (response) =>
    response?.user ??
    (response?.id && response?.email ? response : null);

export const AuthProvider = ({ children }) => {

    const [user, setUser] = useState(null);

    const [token, setToken] = useState(
        localStorage.getItem("token")
    );

    const [loading, setLoading] = useState(true);

    const syncUser = async () => {

        try {

            const response = await getCurrentUser();
            console.log("Current user:", response);
            const currentUser = getUserFromResponse(response);

            if (currentUser) {

                setUser(currentUser);
                return currentUser;

            }

            logout();
            return null;

        } catch (error) {

            console.error(error);

            logout();
            return null;

        }

    };


    // ==========================
    // Load User
    // ==========================

    useEffect(() => {

        const loadUser = async () => {

            if (!token) {

                setLoading(false);
                return;

            }

            try {
                await syncUser();

            } finally {
            setLoading(false);
            }

        };

        loadUser();

    }, [token]);


    // ==========================
    // Register
    // ==========================

    const register = async (userData) => {

        setLoading(true);

        const response = await registerUser(userData);

        if (isAuthSuccess(response)) {

            localStorage.setItem(
                "token",
                response.access_token
            );

            setToken(response.access_token);
            setUser(getUserFromResponse(response));

            if (!getUserFromResponse(response)) {

                await syncUser();

            }

        }

        setLoading(false);

        return response;

    };


    // ==========================
    // Login
    // ==========================

    const login = async (userData) => {

        setLoading(true);

        const response = await loginUser(userData);

        if (isAuthSuccess(response)) {

            localStorage.setItem(
                "token",
                response.access_token
            );

            setToken(response.access_token);
            setUser(getUserFromResponse(response));

            if (!getUserFromResponse(response)) {

                await syncUser();

            }

        }

        setLoading(false);

        return response;

    };


    // ==========================
    // Logout
    // ==========================

    const logout = () => {

        localStorage.removeItem("token");

        setUser(null);

        setToken(null);

    };


    return (

        <AuthContext.Provider

            value={{

                user,

                token,

                loading,

                login,

                register,

                logout,

                isAuthenticated: !!token,

            }}

        >

            {children}

        </AuthContext.Provider>

    );

};


export const useAuth = () => {

    return useContext(AuthContext);

};
