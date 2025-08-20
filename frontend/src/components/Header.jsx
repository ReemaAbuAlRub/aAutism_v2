// import React, { useState, useEffect, useRef } from "react";
// import { motion, AnimatePresence } from "framer-motion";
// import { useNavigate, useLocation } from "react-router-dom";
// import { useTranslation } from "react-i18next";
// import "./Header.css";

// export default function Header({ setFormStep, username, avatar, darkMode, setDarkMode }) {
//     const [menuOpen, setMenuOpen] = useState(false);
//     const [profileOpen, setProfileOpen] = useState(false);
//     const [langOpen, setLangOpen] = useState(false);

//     const langRef = useRef(null);
//     const profileRef = useRef(null);
//     const navigate = useNavigate();
//     const location = useLocation();
//     const { t, i18n } = useTranslation();

//     // إغلاق أي dropdown عند الضغط خارجها
//     useEffect(() => {
//         const handleClickOutside = (event) => {
//             if (
//                 (!langRef.current || !langRef.current.contains(event.target)) &&
//                 (!profileRef.current || !profileRef.current.contains(event.target))
//             ) {
//                 setLangOpen(false);
//                 setProfileOpen(false);
//             }
//         };
//         document.addEventListener("mousedown", handleClickOutside);
//         return () => {
//             document.removeEventListener("mousedown", handleClickOutside);
//         };
//     }, []);

//     // زر الرجوع
//     const handleBack = () => {
//         navigate(-1);
//     };

//     const showBackOnHome =
//         location.pathname === "/" && localStorage.getItem("answeredQuestion");

//     const handleLogoClick = () => {
//         if (location.pathname === "/") {
//             navigate("/");
//         } else if (location.pathname === "/welcome") {
//             navigate("/welcome");
//         } else if (location.pathname === "/chat") {
//             navigate("/welcome");
//         } else if (location.pathname === "/profile") {
//             navigate("/chat");
//         }
//     };

//     return (
//         <header className={`modern-header ${darkMode ? "dark" : ""}`}>
//             <div className="header-left">
//                 <div className="menu-icon" onClick={() => setMenuOpen(true)}>
//                     ☰
//                 </div>

//                 {(location.pathname !== "/" || showBackOnHome) && (
//                     <button className={`back-btn ${darkMode ? "dark" : ""}`} onClick={handleBack}>
//                         🔙
//                     </button>
//                 )}
//             </div>

//             <div
//                 className="logo-center"
//                 onClick={handleLogoClick}
//                 style={{ cursor: "pointer" }}
//             >
//                 <img src="/robot.png" alt="Logo" className="logo-img" />
//                 <span className="logo-text">{t("appName")}</span>
//             </div>

//             <div className="actions-section">
//                 {/* زر الوضع الليلي */}
//                 <button className={`mode-btn ${darkMode ? "dark" : ""}`} onClick={() => setDarkMode(!darkMode)}>
//                     {darkMode ? "☀️" : "🌙"}
//                 </button>

//                 {/* Dropdown للغات */}
//                 <div className="lang-dropdown" ref={langRef}>
//                     <button
//                         className={`auth-btn lang-btn ${darkMode ? "dark" : ""}`}
//                         onClick={() => setLangOpen(!langOpen)}
//                     >
//                         🌐 {i18n.language === "ar" ? "العربية" : "English"}
//                     </button>
//                     <AnimatePresence>
//                         {langOpen && (
//                             <motion.div
//                                 className={`dropdown-menu ${darkMode ? "dark" : ""}`}
//                                 initial={{ opacity: 0, y: -10 }}
//                                 animate={{ opacity: 1, y: 0 }}
//                                 exit={{ opacity: 0, y: -10 }}
//                                 transition={{ duration: 0.3 }}
//                             >
//                                 <button
//                                     className={`dropdown-item ${darkMode ? "dark" : ""}`}
//                                     onClick={() => {
//                                         i18n.changeLanguage("ar");
//                                         setLangOpen(false);
//                                     }}
//                                 >
//                                     🇸🇦 العربية
//                                 </button>
//                                 <button
//                                     className={`dropdown-item ${darkMode ? "dark" : ""}`}
//                                     onClick={() => {
//                                         i18n.changeLanguage("en");
//                                         setLangOpen(false);
//                                     }}
//                                 >
//                                     🇬🇧 English
//                                 </button>
//                             </motion.div>
//                         )}
//                     </AnimatePresence>
//                 </div>

//                 {/* Dropdown للبروفايل */}
//                 {username && (
//                     <div className="lang-dropdown" ref={profileRef}>
//                         <button
//                             className={`auth-btn lang-btn ${darkMode ? "dark" : ""}`}
//                             onClick={() => setProfileOpen(!profileOpen)}
//                         >
//                             {avatar ? (
//                                 <img src={avatar} alt="Avatar" className="avatar-small" />
//                             ) : (
//                                 "👤"
//                             )}{" "}
//                             {username}
//                         </button>
//                         <AnimatePresence>
//                             {profileOpen && (
//                                 <motion.div
//                                     className={`dropdown-menu ${darkMode ? "dark" : ""}`}
//                                     initial={{ opacity: 0, y: -10 }}
//                                     animate={{ opacity: 1, y: 0 }}
//                                     exit={{ opacity: 0, y: -10 }}
//                                     transition={{ duration: 0.3 }}
//                                 >
//                                     <button
//                                         className={`dropdown-item ${darkMode ? "dark" : ""}`}
//                                         onClick={() => {
//                                             navigate("/profile");
//                                             setProfileOpen(false);
//                                         }}
//                                     >
//                                         ✏️ {t("editProfile")}
//                                     </button>
//                                     <button
//                                         className={`dropdown-item logout ${darkMode ? "dark" : ""}`}
//                                         onClick={() => {
//                                             localStorage.clear();
//                                             window.location.href = "/";
//                                         }}
//                                     >
//                                         🚪 {t("logout")}
//                                     </button>
//                                 </motion.div>
//                             )}
//                         </AnimatePresence>
//                     </div>
//                 )}

//                 {!username && (
//                     <>
//                         <button
//                             className={`auth-btn signin ${darkMode ? "dark" : ""}`}
//                             onClick={() => setFormStep("signin")}
//                         >
//                             {t("signin")}
//                         </button>
//                         <button
//                             className={`auth-btn signup ${darkMode ? "dark" : ""}`}
//                             onClick={() => setFormStep("signup")}
//                         >
//                             {t("signup")}
//                         </button>
//                     </>
//                 )}
//             </div>

//             {/* القائمة الجانبية */}
//             <AnimatePresence>
//                 {menuOpen && (
//                     <>
//                         <motion.div
//                             className="menu-overlay"
//                             onClick={() => setMenuOpen(false)}
//                             initial={{ opacity: 0 }}
//                             animate={{ opacity: 0.6 }}
//                             exit={{ opacity: 0 }}
//                             transition={{ duration: 0.3 }}
//                         />

//                         <motion.div
//                             className={`side-menu ${darkMode ? "dark" : ""}`}
//                             initial={{ x: -300, opacity: 0 }}
//                             animate={{ x: 0, opacity: 1 }}
//                             exit={{ x: -300, opacity: 0 }}
//                             transition={{ duration: 0.4, ease: "easeInOut" }}
//                         >
//                             <div className="side-menu-links">
//                                 {location.pathname === "/" && (
//                                     <button
//                                         onClick={() => navigate("/")}
//                                         className={`auth-btn ${darkMode ? "dark" : ""}`}
//                                     >
//                                         🏠 {t("menu.home")}
//                                     </button>
//                                 )}
//                                 <button
//                                     onClick={() => navigate("/welcome")}
//                                     className={`auth-btn ${darkMode ? "dark" : ""}`}
//                                 >
//                                     🌼 {t("menu.welcome")}
//                                 </button>
//                                 <button
//                                     onClick={() => navigate("/chat")}
//                                     className={`auth-btn ${darkMode ? "dark" : ""}`}
//                                 >
//                                     💬 {t("menu.chat")}
//                                 </button>
//                                 <button
//                                     onClick={() => navigate("/profile")}
//                                     className={`auth-btn ${darkMode ? "dark" : ""}`}
//                                 >
//                                     ⚙️ {t("menu.profile")}
//                                 </button>

//                                 <a
//                                     href="https://ga4dh.org/about-us"
//                                     target="_blank"
//                                     rel="noopener noreferrer"
//                                     className={`auth-btn about-btn ${darkMode ? "dark" : ""}`}
//                                 >
//                                     ℹ️ {t("menu.about")}
//                                 </a>
//                                 <div className="logout-containar">
//                                     <button
//                                         onClick={() => setMenuOpen(false)}
//                                         className={`close-side ${darkMode ? "dark" : ""}`}
//                                     >
//                                         ✖️ {t("menu.close")}
//                                     </button>
//                                 </div>
//                             </div>
//                         </motion.div>
//                     </>
//                 )}
//             </AnimatePresence>
//         </header>
//     );
// }

import React, { useEffect, useState } from "react";
import { NavLink, useLocation, useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import "../styles/Header.css";

export default function Header({ isLoggedIn, username, avatar, darkMode, setDarkMode, onLogout }) {
  const { t, i18n } = useTranslation();
  const navigate = useNavigate();
  const location = useLocation();
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute("dir", "ltr");
  }, []);

  const toggleLang = () => {
    const next = i18n.language?.startsWith("ar") ? "en" : "ar";
    i18n.changeLanguage(next);
    document.documentElement.setAttribute("dir", "ltr")
    // document.documentElement.setAttribute("dir", next.startsWith("ar") ? "rtl" : "ltr");
  };

  const handleLogout = () => {
    const savedLang = i18n.language;
    const savedDark = localStorage.getItem("dark-mode");
    setMenuOpen(false);

    sessionStorage.clear();
    localStorage.clear(); // removes token etc.

    if (savedLang) {
      i18n.changeLanguage(savedLang);
      document.documentElement.setAttribute("dir", savedLang.startsWith("ar") ? "rtl" : "ltr");
    }
    if (savedDark !== null) localStorage.setItem("dark-mode", savedDark);

    onLogout?.();                  // flip App state → Header re-renders w/ Signin/Signup
    navigate("/", { replace: true });
  };

  return (
    <>
      <header className="modern-header">
        <div className="header-left">
          <button className={`menu-icon ${darkMode ? "dark" : ""}`} onClick={() => setMenuOpen(true)}>☰</button>
          {location.pathname !== "/" && (
            <button className={`back-btn ${darkMode ? "dark" : ""}`} onClick={() => navigate(-1)}>←</button>
          )}
        </div>

        <div className="logo-center">
          <img src="/robot.png" alt="logo" className="logo-img" />
          <div className="logo-text">{t("appName")}</div>
        </div>

        <div className="actions-section">
          <button className={`mode-btn ${darkMode ? "dark" : ""}`} onClick={() => setDarkMode(v => !v)}>
            {darkMode ? "☀️" : "🌙"}
          </button>
          <button className={`lang-btn ${darkMode ? "dark" : ""}`} onClick={toggleLang}>
            🌐 {i18n.language?.startsWith("ar") ? "العربية" : "EN"}
          </button>

          {isLoggedIn ? (
            <>
              <div className="user-chip">
                <div className="avatar" />
                <span>{username || "User"}</span>
              </div>
              <button className={`auth-btn signin ${darkMode ? "dark" : ""}`} onClick={handleLogout}>
                {t("logout")}
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className={`auth-btn signin ${darkMode ? "dark" : ""}`}>{t("signin")}</NavLink>
              <NavLink to="/signup" className={`auth-btn signup ${darkMode ? "dark" : ""}`}>{t("signup")}</NavLink>
            </>
          )}
        </div>
      </header>

      {/* {isLoggedIn && (
        <nav className="subnav">
          <NavLink to="/" end className={({ isActive }) => `subnav-link ${isActive ? "active" : ""}`}>{t("menu.home")}</NavLink>
          <NavLink to="/chat" className={({ isActive }) => `subnav-link ${isActive ? "active" : ""}`}>{t("menu.chat")}</NavLink>
          <NavLink to="/profile" className={({ isActive }) => `subnav-link ${isActive ? "active" : ""}`}>{t("menu.profile")}</NavLink>
        </nav>
      )} */}

      {menuOpen && <div className="menu-overlay" onClick={() => setMenuOpen(false)} />}
      <aside className={`side-menu ${darkMode ? "dark" : ""}`} style={{ transform: `translateX(${menuOpen ? "0" : "-100%"})` }}>
        <div className="side-menu-links">
          <NavLink to="/" onClick={() => setMenuOpen(false)}>{t("menu.home")}</NavLink>
          <NavLink to="/chat" onClick={() => setMenuOpen(false)}>{t("menu.chat")}</NavLink>
          <NavLink to="/profile" onClick={() => setMenuOpen(false)}>{t("menu.profile")}</NavLink>
 
          <button className="about-btn" onClick={() => { setMenuOpen(false); navigate("/about"); }}>{t("menu.about")}</button>
        </div>
        <div className="logout-container">
          {isLoggedIn ? (
            <button className={`close-side ${darkMode ? "dark" : ""}`} onClick={handleLogout}>{t("logout")}</button>
          ) : (
            <button className={`close-side ${darkMode ? "dark" : ""}`} onClick={() => setMenuOpen(false)}>{t("menu.close")}</button>
          )}
        </div>
      </aside>
    </>
  );
}
