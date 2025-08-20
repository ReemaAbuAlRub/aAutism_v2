import React, { useState } from "react";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import "../styles/SignupPage.css"; // reuse existing styles

export default function LeftPanel({ title }) {
  const { t } = useTranslation();
  const [showBreathing, setShowBreathing] = useState(false);

  return (
    <div className="left-section">
      <motion.img
        src="/robot.png"
        alt="Robot"
        className="robot-animated-big"
        animate={{ rotate: [0, 5, -5, 0] }}
        transition={{ repeat: Infinity, duration: 3 }}
      />
      <h1 className="app-name">{t("appName")}</h1>
      <h3 className="page-title">{title}</h3>

      <button className="breathing-btn" onClick={() => setShowBreathing(true)}>
        {t("signupPage.breathingExerciseBtn")}
      </button>

      {showBreathing && (
        <div className="breathing-modal">
          <div className="modal-content">
            <h2>{t("signupPage.breathingExerciseTitle")}</h2>
            <p>{t("signupPage.breathingExerciseText")}</p>
            <motion.div
              className="breathing-circle"
              animate={{ scale: [1, 1.4, 1] }}
              transition={{ repeat: Infinity, duration: 4 }}
            />
            <button className="close-btn" onClick={() => setShowBreathing(false)}>
              {t("signupPage.popupClose")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}