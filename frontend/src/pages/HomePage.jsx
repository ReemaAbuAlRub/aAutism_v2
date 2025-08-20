// File: src/pages/HomePage.jsx
import React from "react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";
import LeftPanel from "../components/LeftPanel";
import "../styles/SignupPage.css";

export default function HomePage({ darkMode }) {
  const { t } = useTranslation();
  const navigate = useNavigate();

  // IMPORTANT: removed the auto-redirect useEffect.
  // We only navigate after the user clicks a button.

  const handleYes = () => {
    localStorage.setItem("answeredQuestion", "true");
    navigate("/login");
  };

  const handleNo = () => {
    localStorage.setItem("answeredQuestion", "true");
    navigate("/signup");
  };

  return (
    <div className={`signup-page ${darkMode ? "dark" : ""}`}>
      <div className="page-layout">
        <LeftPanel title={t("signupPage.questionTitle")} />

        <div className="right-section">
          <motion.div
            className="form-box modern-form no-bg"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h2 className="form-title">{t("signupPage.questionTitle")}</h2>
            <div className="question-buttons">
              <button onClick={handleYes} className="modern-btn yes-btn">
                {t("signupPage.yes")}
              </button>
              <button onClick={handleNo} className="modern-btn no-btn">
                {t("signupPage.no")}
              </button>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

// Also ensure logout clears the flag so first visit shows HomePage next time.
// In src/components/Header.jsx, inside logout():
// localStorage.removeItem("answeredQuestion"); // (or localStorage.clear())
