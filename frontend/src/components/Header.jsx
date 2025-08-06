import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import "./Header.css";

export default function Header({ setFormStep, username, avatar, darkMode, setDarkMode }) {
    const [menuOpen, setMenuOpen] = useState(false);
    const [profileOpen, setProfileOpen] = useState(false);
    const [langOpen, setLangOpen] = useState(false);

    const langRef = useRef(null);
    const profileRef = useRef(null);
    const navigate = useNavigate();
    const location = useLocation();
    const { t, i18n } = useTranslation();

    // إغلاق أي dropdown عند الضغط خارجها
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (
                (!langRef.current || !langRef.current.contains(event.target)) &&
                (!profileRef.current || !profileRef.current.contains(event.target))
            ) {
                setLangOpen(false);
                setProfileOpen(false);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    // زر الرجوع
    const handleBack = () => {
        navigate(-1);
    };

    const showBackOnHome =
        location.pathname === "/" && localStorage.getItem("answeredQuestion");

    const handleLogoClick = () => {
        if (location.pathname === "/") {
            navigate("/");
        } else if (location.pathname === "/welcome") {
            navigate("/welcome");
        } else if (location.pathname === "/chat") {
            navigate("/welcome");
        } else if (location.pathname === "/profile") {
            navigate("/chat");
        }
    };

    return (
        <header className={`modern-header ${darkMode ? "dark" : ""}`}>
            <div className="header-left">
                <div className="menu-icon" onClick={() => setMenuOpen(true)}>
                    ☰
                </div>

                {(location.pathname !== "/" || showBackOnHome) && (
                    <button className={`back-btn ${darkMode ? "dark" : ""}`} onClick={handleBack}>
                        🔙
                    </button>
                )}
            </div>

            <div
                className="logo-center"
                onClick={handleLogoClick}
                style={{ cursor: "pointer" }}
            >
                <img src="/robot.png" alt="Logo" className="logo-img" />
                <span className="logo-text">{t("appName")}</span>
            </div>

            <div className="actions-section">
                {/* زر الوضع الليلي */}
                <button className={`mode-btn ${darkMode ? "dark" : ""}`} onClick={() => setDarkMode(!darkMode)}>
                    {darkMode ? "☀️" : "🌙"}
                </button>

                {/* Dropdown للغات */}
                <div className="lang-dropdown" ref={langRef}>
                    <button
                        className={`auth-btn lang-btn ${darkMode ? "dark" : ""}`}
                        onClick={() => setLangOpen(!langOpen)}
                    >
                        🌐 {i18n.language === "ar" ? "العربية" : "English"}
                    </button>
                    <AnimatePresence>
                        {langOpen && (
                            <motion.div
                                className={`dropdown-menu ${darkMode ? "dark" : ""}`}
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.3 }}
                            >
                                <button
                                    className={`dropdown-item ${darkMode ? "dark" : ""}`}
                                    onClick={() => {
                                        i18n.changeLanguage("ar");
                                        setLangOpen(false);
                                    }}
                                >
                                    🇸🇦 العربية
                                </button>
                                <button
                                    className={`dropdown-item ${darkMode ? "dark" : ""}`}
                                    onClick={() => {
                                        i18n.changeLanguage("en");
                                        setLangOpen(false);
                                    }}
                                >
                                    🇬🇧 English
                                </button>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>

                {/* Dropdown للبروفايل */}
                {username && (
                    <div className="lang-dropdown" ref={profileRef}>
                        <button
                            className={`auth-btn lang-btn ${darkMode ? "dark" : ""}`}
                            onClick={() => setProfileOpen(!profileOpen)}
                        >
                            {avatar ? (
                                <img src={avatar} alt="Avatar" className="avatar-small" />
                            ) : (
                                "👤"
                            )}{" "}
                            {username}
                        </button>
                        <AnimatePresence>
                            {profileOpen && (
                                <motion.div
                                    className={`dropdown-menu ${darkMode ? "dark" : ""}`}
                                    initial={{ opacity: 0, y: -10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    transition={{ duration: 0.3 }}
                                >
                                    <button
                                        className={`dropdown-item ${darkMode ? "dark" : ""}`}
                                        onClick={() => {
                                            navigate("/profile");
                                            setProfileOpen(false);
                                        }}
                                    >
                                        ✏️ {t("editProfile")}
                                    </button>
                                    <button
                                        className={`dropdown-item logout ${darkMode ? "dark" : ""}`}
                                        onClick={() => {
                                            localStorage.clear();
                                            window.location.href = "/";
                                        }}
                                    >
                                        🚪 {t("logout")}
                                    </button>
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>
                )}

                {!username && (
                    <>
                        <button
                            className={`auth-btn signin ${darkMode ? "dark" : ""}`}
                            onClick={() => setFormStep("signin")}
                        >
                            {t("signin")}
                        </button>
                        <button
                            className={`auth-btn signup ${darkMode ? "dark" : ""}`}
                            onClick={() => setFormStep("signup")}
                        >
                            {t("signup")}
                        </button>
                    </>
                )}
            </div>

            {/* القائمة الجانبية */}
            <AnimatePresence>
                {menuOpen && (
                    <>
                        <motion.div
                            className="menu-overlay"
                            onClick={() => setMenuOpen(false)}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 0.6 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.3 }}
                        />

                        <motion.div
                            className={`side-menu ${darkMode ? "dark" : ""}`}
                            initial={{ x: -300, opacity: 0 }}
                            animate={{ x: 0, opacity: 1 }}
                            exit={{ x: -300, opacity: 0 }}
                            transition={{ duration: 0.4, ease: "easeInOut" }}
                        >
                            <div className="side-menu-links">
                                {location.pathname === "/" && (
                                    <button
                                        onClick={() => navigate("/")}
                                        className={`auth-btn ${darkMode ? "dark" : ""}`}
                                    >
                                        🏠 {t("menu.home")}
                                    </button>
                                )}
                                <button
                                    onClick={() => navigate("/welcome")}
                                    className={`auth-btn ${darkMode ? "dark" : ""}`}
                                >
                                    🌼 {t("menu.welcome")}
                                </button>
                                <button
                                    onClick={() => navigate("/chat")}
                                    className={`auth-btn ${darkMode ? "dark" : ""}`}
                                >
                                    💬 {t("menu.chat")}
                                </button>
                                <button
                                    onClick={() => navigate("/profile")}
                                    className={`auth-btn ${darkMode ? "dark" : ""}`}
                                >
                                    ⚙️ {t("menu.profile")}
                                </button>

                                <a
                                    href="https://ga4dh.org/about-us"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className={`auth-btn about-btn ${darkMode ? "dark" : ""}`}
                                >
                                    ℹ️ {t("menu.about")}
                                </a>
                                <div className="logout-containar">
                                    <button
                                        onClick={() => setMenuOpen(false)}
                                        className={`close-side ${darkMode ? "dark" : ""}`}
                                    >
                                        ✖️ {t("menu.close")}
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    </>
                )}
            </AnimatePresence>
        </header>
    );
}
