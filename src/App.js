import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { useState, useEffect } from "react";
import { I18nextProvider } from "react-i18next";
import i18n from "./i18n";

import SignupPage from "./pages/SignupPage";
import Welcome from "./pages/Welcome";
import Chat from "./pages/Chat";
import Profile from "./pages/Profile";
import Header from "./components/Header";

function App() {
    const [formStep, setFormStep] = useState("question");
    const [username, setUsername] = useState("");
    const [avatar, setAvatar] = useState(null);
    const [darkMode, setDarkMode] = useState(false);

    // استرجاع البيانات من localStorage عند التحميل
    useEffect(() => {
        const storedName = localStorage.getItem("username");
        const storedAvatar = localStorage.getItem("avatar");
        const savedMode = localStorage.getItem("dark-mode") === "true";

        if (storedName) setUsername(storedName);
        if (storedAvatar) setAvatar(storedAvatar);
        setDarkMode(savedMode);

        // ضبط كلاس الوضع الليلي عند أول تحميل
        document.body.classList.toggle("dark-mode", savedMode);
    }, []);

    // تحديث body عند تغيير الوضع الليلي
    useEffect(() => {
        if (darkMode) {
            document.body.classList.add("dark-mode");
        } else {
            document.body.classList.remove("dark-mode");
        }
        localStorage.setItem("dark-mode", darkMode);
    }, [darkMode]);

    const isLoggedIn = !!username;

    return (
        <I18nextProvider i18n={i18n}>
            <Router>
                <Header
                    setFormStep={setFormStep}
                    username={username}
                    avatar={avatar}
                    darkMode={darkMode}
                    setDarkMode={setDarkMode}
                />
                <div>
                    <Routes>
                        {/* صفحة التسجيل */}
                        <Route
                            path="/"
                            element={
                                isLoggedIn ? (
                                    <Navigate to="/welcome" replace />
                                ) : (
                                    <SignupPage
                                        externalStep={formStep}
                                        setUsername={setUsername}
                                        setAvatar={setAvatar}
                                        darkMode={darkMode}
                                    />
                                )
                            }
                        />

                        {/* صفحة الترحيب */}
                        <Route
                            path="/welcome"
                            element={
                                isLoggedIn ? (
                                    <Welcome
                                        username={username}
                                        avatar={avatar}
                                        darkMode={darkMode}
                                    />
                                ) : (
                                    <Navigate to="/" replace />
                                )
                            }
                        />

                        {/* صفحة الشات */}
                        <Route
                            path="/chat"
                            element={
                                isLoggedIn ? (
                                    <Chat
                                        username={username}
                                        avatar={avatar}
                                        darkMode={darkMode}
                                    />
                                ) : (
                                    <Navigate to="/" replace />
                                )
                            }
                        />

                        {/* صفحة البروفايل */}
                        <Route
                            path="/profile"
                            element={
                                isLoggedIn ? (
                                    <Profile
                                        setUsernameGlobal={setUsername}
                                        setAvatarGlobal={setAvatar}
                                        darkMode={darkMode}
                                    />
                                ) : (
                                    <Navigate to="/" replace />
                                )
                            }
                        />
                    </Routes>
                </div>
            </Router>
        </I18nextProvider>
    );
}

export default App;
