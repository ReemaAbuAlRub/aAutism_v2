import React, { useState, useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import "./../styles/Chat.css";

export default function Chat({ username, darkMode }) {
    const { t, i18n } = useTranslation();

    const [messages, setMessages] = useState([
        {
            id: 1,
            text: t("chat.botWelcome", { name: username || t("friend") }),
            sender: "bot",
        },
    ]);
    const [input, setInput] = useState("");
    const [listening, setListening] = useState(false);

    const messagesEndRef = useRef(null);
    const chatBoxRef = useRef(null);
    const recognitionRef = useRef(null);
    const [assistantPosition, setAssistantPosition] = useState({ top: "80%" });

    useEffect(() => {
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = 0;
        }
    }, []);

    useEffect(() => {
        if (messages.length > 1) {
            messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    const handleScroll = () => {
        if (!chatBoxRef.current) return;
        const chatBox = chatBoxRef.current;
        const msgElements = Array.from(chatBox.querySelectorAll(".chat-message"));
        let closestMsg = null;
        let closestDist = Infinity;

        msgElements.forEach((el) => {
            const rect = el.getBoundingClientRect();
            const dist = Math.abs(rect.top - window.innerHeight / 2);
            if (dist < closestDist) {
                closestDist = dist;
                closestMsg = el;
            }
        });

        if (closestMsg) {
            const rect = closestMsg.getBoundingClientRect();
            setAssistantPosition({ top: rect.top + window.scrollY + rect.height / 2 });
        }
    };

    useEffect(() => {
        const chatBox = chatBoxRef.current;
        if (chatBox) {
            chatBox.addEventListener("scroll", handleScroll);
            handleScroll();
        }
        return () => chatBox?.removeEventListener("scroll", handleScroll);
    }, [messages]);

    const handleSend = () => {
        if (input.trim() === "") return;
        const newMsg = { id: Date.now(), text: input, sender: "user" };
        setMessages([...messages, newMsg]);

        setTimeout(() => {
            const botReply = {
                id: Date.now(),
                text: t("chat.botReply"),
                sender: "bot",
            };
            setMessages((prev) => [...prev, botReply]);
        }, 1000);

        setInput("");
    };

    const startListening = () => {
        if (!("webkitSpeechRecognition" in window)) {
            alert("⚠️ المتصفح لا يدعم التعرف على الصوت");
            return;
        }

        const recognition = new window.webkitSpeechRecognition();
        recognition.lang = i18n.language === "en" ? "en-US" : "ar-SA";
        recognition.continuous = false;
        recognition.interimResults = false;

        recognition.onstart = () => setListening(true);
        recognition.onend = () => setListening(false);

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            setInput(transcript);
        };

        recognition.start();
        recognitionRef.current = recognition;
    };

    return (
        <div className={`chat-container ${darkMode ? "dark" : ""}`}>
            <div className="chat-box" ref={chatBoxRef}>
                {messages.map((msg) => (
                    <div
                        key={msg.id}
                        data-id={msg.id}
                        className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
                    >
                        <div className="message-bubble">{msg.text}</div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
            </div>

            <div
                className="chat-assistant"
                style={{ top: assistantPosition.top }}
            >
                <img src="/robot.png" alt="robot assistant" />
            </div>

            <div className="chat-input-container">
                <input
                    type="text"
                    className="chat-input"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder={t("chat.placeholder")}
                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                />
                <button
                    className={`mic-btn ${listening ? "active" : ""}`}
                    onClick={startListening}
                >
                    {listening ? t("chat.listening") : t("chat.mic")}
                </button>
                <button className="send-btn" onClick={handleSend}>
                    {t("chat.send")}
                </button>
            </div>
        </div>
    );
}
