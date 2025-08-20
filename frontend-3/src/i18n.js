import i18n from "i18next";
import { initReactI18next } from "react-i18next";
import ar from "./translations/ar.json";
import en from "./translations/en.json";

i18n
    .use(initReactI18next)
    .init({
        resources: {
            ar: {
                translation: ar,
            },
            en: {
                translation: en,
            },
        },
        lng: "ar", // اللغة الافتراضية
        fallbackLng: "en", // إذا ما لقى النص يرجع للإنجليزية
        interpolation: {
            escapeValue: false,
        },
    });

export default i18n;
