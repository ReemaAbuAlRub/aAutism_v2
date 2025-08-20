import React, { createContext, useState } from "react";

export const LanguageContext = createContext();

const translations = {
    ar: {
        appName: "روبوت المساعدة",
        signin: "تسجيل الدخول",
        signup: "إنشاء حساب",
        welcomeMsg: "مرحباً بك 🌼",
        chat: "الشات",
        profile: "الملف الشخصي",
    },
    en: {
        appName: "Assistant Bot",
        signin: "Sign In",
        signup: "Sign Up",
        welcomeMsg: "Welcome 🌼",
        chat: "Chat",
        profile: "Profile",
    },
};

export const LanguageProvider = ({ children }) => {
    const [language, setLanguage] = useState("ar");

    return (
        <LanguageContext.Provider value={{ language, setLanguage, texts: translations }}>
            {children}
        </LanguageContext.Provider>
    );
};
