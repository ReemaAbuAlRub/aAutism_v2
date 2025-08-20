import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "../styles/Welcome.css";
import { useTranslation } from "react-i18next";

export default function Welcome({ username, avatar, darkMode }) {
    const [step, setStep] = useState("intro");
    const [selectedMood, setSelectedMood] = useState(null);
    // const [rockHits, setRockHits] = useState(0); // الغضب معطل حالياً
    const navigate = useNavigate();
    const { t } = useTranslation();

    const exercises = {
        calm: {
            title: t("exercise.calm.title"),
            text: t("exercise.calm.text"),
        },
        neutral: {
            title: t("exercise.neutral.title"),
            text: t("exercise.neutral.text"),
        },
        sad: {
            title: t("exercise.sad.title"),
            text: t("exercise.sad.text"),
        },
    };

    useEffect(() => {
        if (selectedMood === "happy") {
            setTimeout(() => {
                navigate("/chat");
            }, 3000);
        }
    }, [selectedMood, navigate]);

    return (
        <div className={`welcome-page ${darkMode ? "dark" : ""}`}>
            {step === "intro" && (
                <motion.div
                    className="intro-box"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 1 }}
                >
                    <img src="/robot.png" alt="Robot" className="robot-img" />
                    <h1>{t("welcomeTitle", { name: username ? ` ${username}` : "" })}</h1>
                    <button onClick={() => setStep("mood")} className="start-btn">
                        {t("startBtn")}
                    </button>
                </motion.div>
            )}

            {step === "mood" && (
                <motion.div
                    className="mood-box"
                    initial={{ y: 50, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ duration: 0.7 }}
                >
                    <h2>{t("howDoYouFeel")}</h2>
                    <div className="emoji-options">
                        <div className="emoji-card" onClick={() => setSelectedMood("happy")}>
                            <span className="emoji">😀</span>
                            <span className="emoji-label">{t("moods.happy")}</span>
                        </div>
                        <div className="emoji-card" onClick={() => setSelectedMood("calm")}>
                            <span className="emoji">🙂</span>
                            <span className="emoji-label">{t("moods.calm")}</span>
                        </div>
                        <div className="emoji-card" onClick={() => setSelectedMood("neutral")}>
                            <span className="emoji">😐</span>
                            <span className="emoji-label">{t("moods.neutral")}</span>
                        </div>
                        <div className="emoji-card" onClick={() => setSelectedMood("sad")}>
                            <span className="emoji">😞</span>
                            <span className="emoji-label">{t("moods.sad")}</span>
                        </div>
                        {/* الغضب معطل 
                        <div className="emoji-card" onClick={() => setSelectedMood("angry")}>
                            <span className="emoji">😡</span>
                            <span className="emoji-label">{t("moods.angry")}</span>
                        </div> */}
                    </div>
                </motion.div>
            )}

            {selectedMood && selectedMood !== "happy" && selectedMood !== "angry" && (
                <div className="exercise-modal">
                    <div className="modal-content">
                        <button
                            className="close-btn"
                            onClick={() => setSelectedMood(null)}
                        >
                            ❌
                        </button>
                        <h2>{exercises[selectedMood].title}</h2>
                        <p>{exercises[selectedMood].text}</p>
                        <motion.div
                            className="breathing-circle"
                            animate={{ scale: [1, 1.4, 1] }}
                            transition={{ repeat: Infinity, duration: 4 }}
                        />
                        <button
                            className="continue-btn"
                            onClick={() => navigate("/chat")}
                        >
                            {t("continueToChat")}
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
