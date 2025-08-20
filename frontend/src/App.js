// import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
// import { useState, useEffect } from "react";
// import { I18nextProvider } from "react-i18next";
// import i18n from "./i18n";

// import SignupPage from "./pages/SignupPage";
// import Welcome from "./pages/Welcome";
// import Chat from "./pages/Chat";
// import Profile from "./pages/Profile";
// import Header from "./components/Header";

// function App() {
//     const [formStep, setFormStep] = useState("question");
//     const [username, setUsername] = useState("");
//     const [avatar, setAvatar] = useState(null);
//     const [darkMode, setDarkMode] = useState(false);

//     // استرجاع البيانات من localStorage عند التحميل
//     useEffect(() => {
//         const storedName = localStorage.getItem("username");
//         const storedAvatar = localStorage.getItem("avatar");
//         const savedMode = localStorage.getItem("dark-mode") === "true";

//         if (storedName) setUsername(storedName);
//         if (storedAvatar) setAvatar(storedAvatar);
//         setDarkMode(savedMode);

//         // ضبط كلاس الوضع الليلي عند أول تحميل
//         document.body.classList.toggle("dark-mode", savedMode);
//     }, []);

//     // تحديث body عند تغيير الوضع الليلي
//     useEffect(() => {
//         if (darkMode) {
//             document.body.classList.add("dark-mode");
//         } else {
//             document.body.classList.remove("dark-mode");
//         }
//         localStorage.setItem("dark-mode", darkMode);
//     }, [darkMode]);

//     const isLoggedIn = !!username;

//     return (
//         <I18nextProvider i18n={i18n}>
//             <Router>
//                 <Header
//                     setFormStep={setFormStep}
//                     username={username}
//                     avatar={avatar}
//                     darkMode={darkMode}
//                     setDarkMode={setDarkMode}
//                 />
//                 <div>
//                     <Routes>
//                         {/* صفحة التسجيل */}
//                         <Route
//                             path="/"
//                             element={
//                                 isLoggedIn ? (
//                                     <Navigate to="/welcome" replace />
//                                 ) : (
//                                     <SignupPage
//                                         externalStep={formStep}
//                                         setUsername={setUsername}
//                                         setAvatar={setAvatar}
//                                         darkMode={darkMode}
//                                     />
//                                 )
//                             }
//                         />

//                         {/* صفحة الترحيب */}
//                         <Route
//                             path="/welcome"
//                             element={
//                                 isLoggedIn ? (
//                                     <Welcome
//                                         username={username}
//                                         avatar={avatar}
//                                         darkMode={darkMode}
//                                     />
//                                 ) : (
//                                     <Navigate to="/" replace />
//                                 )
//                             }
//                         />

//                         {/* صفحة الشات */}
//                         <Route
//                             path="/chat"
//                             element={
//                                 isLoggedIn ? (
//                                     <Chat
//                                         username={username}
//                                         avatar={avatar}
//                                         darkMode={darkMode}
//                                     />
//                                 ) : (
//                                     <Navigate to="/" replace />
//                                 )
//                             }
//                         />

//                         {/* صفحة البروفايل */}
//                         <Route
//                             path="/profile"
//                             element={
//                                 isLoggedIn ? (
//                                     <Profile
//                                         setUsernameGlobal={setUsername}
//                                         setAvatarGlobal={setAvatar}
//                                         darkMode={darkMode}
//                                     />
//                                 ) : (
//                                     <Navigate to="/" replace />
//                                 )
//                             }
//                         />
//                     </Routes>
//                 </div>
//             </Router>
//         </I18nextProvider>
//     );
// }

// export default App;




import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import { I18nextProvider } from "react-i18next";
import i18n from "./i18n";

import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import Welcome from "./pages/Welcome";
import Chat from "./pages/Chat";
import Profile from "./pages/Profile";
import Header from "./components/Header";

export default function App() {
  const [darkMode, setDarkMode] = useState(localStorage.getItem("dark-mode") === "true");
  const [username, setUsername] = useState(localStorage.getItem("username") || "");
  const [avatar, setAvatar] = useState(localStorage.getItem("avatar") || null);

  // ✅ single source of truth for auth
  const [isLoggedIn, setIsLoggedIn] = useState(!!localStorage.getItem("token"));

  useEffect(() => {
    document.body.classList.toggle("dark-mode", darkMode);
    localStorage.setItem("dark-mode", String(darkMode));
  }, [darkMode]);

  // sync across tabs
  useEffect(() => {
    const onStorage = (e) => {
      if (e.key === "token") setIsLoggedIn(!!e.newValue);
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  const handleLogin = (displayName) => {
    // why: make Header reactive immediately
    setIsLoggedIn(true);
    if (displayName) {
      setUsername(displayName);
      localStorage.setItem("username", displayName);
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUsername("");
    setAvatar(null);
  };

  return (
    <I18nextProvider i18n={i18n}>
      <Router>
        <Header
          isLoggedIn={isLoggedIn}
          username={username}
          avatar={avatar}
          darkMode={darkMode}
          setDarkMode={setDarkMode}
          onLogout={handleLogout}
        />
        <Routes>
          <Route path="/" element={isLoggedIn ? <Navigate to="/welcome" replace /> : <HomePage darkMode={darkMode} />} />
          <Route
            path="/login"
            element={
              isLoggedIn ? (
                <Navigate to="/welcome" replace />
              ) : (
                <LoginPage setUsername={setUsername} darkMode={darkMode} onLogin={handleLogin} />
              )
            }
          />
          <Route
            path="/signup"
            element={
              isLoggedIn ? (
                <Navigate to="/welcome" replace />
              ) : (
                <SignupPage setUsername={setUsername} darkMode={darkMode} onLogin={handleLogin} />
              )
            }
          />
          <Route path="/welcome" element={isLoggedIn ? <Welcome username={username} /> : <Navigate to="/" replace />} />
          <Route path="/chat" element={isLoggedIn ? <Chat username={username} avatar={avatar} darkMode={darkMode} /> : <Navigate to="/" replace />} />
          <Route
            path="/profile"
            element={
              isLoggedIn ? (
                <Profile setUsernameGlobal={setUsername} setAvatarGlobal={setAvatar} darkMode={darkMode} />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </I18nextProvider>
  );
}