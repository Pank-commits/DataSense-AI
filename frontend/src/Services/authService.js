import api from "./api";

const getAuthErrorMessage = (error, fallbackMessage) => {

    const status = error.response?.status;

    const apiMessage =
        error.response?.data?.message ||
        error.response?.data?.detail;

    if (status === 409) {

        return "Email already registered.";

    }

    if (status === 401) {

        return "Invalid email or password.";

    }

    if (typeof apiMessage === "string" && apiMessage.trim()) {

        return apiMessage;

    }

    return fallbackMessage;

};


// ==========================
// Register
// ==========================

export const registerUser = async (userData) => {

    try {

        const response = await api.post(
            "/auth/register",
            userData
        );

        return response.data;

    } catch (error) {

        return {
            success: false,
            message: getAuthErrorMessage(
                error,
                "Unable to register. Please try again."
            ),
        };

    }

};


// ==========================
// Login
// ==========================

export const loginUser = async (userData) => {

    try {

        const response = await api.post(
            "/auth/login",
            userData
        );

        return response.data;

    } catch (error) {

        return {
            success: false,
            message: getAuthErrorMessage(
                error,
                "Unable to login. Please try again."
            ),
        };

    }

};


// ==========================
// Current User
// ==========================

export const getCurrentUser = async () => {

    const response = await api.get(
        "/auth/me"
    );

    return response.data;

};
