// import React, { useState, useEffect, useRef } from "react";
// import { useTranslation } from "react-i18next";
// import "./../styles/Chat.css";

// const API = "http://localhost:8000/api/v1/chat";

// export default function Chat({ username, darkMode }) {
//     const { t, i18n } = useTranslation();


//     const [messages, setMessages] = useState([
//         {
//             id: 1,
//             text: t("chat.botWelcome", { name: username || t("friend") }),
//             sender: "bot",
//         },
//     ]);
//     const [input, setInput] = useState("");
//     const [listening, setListening] = useState(false);

//     const messagesEndRef = useRef(null);
//     const chatBoxRef = useRef(null);
//     const recognitionRef = useRef(null);
//     const [assistantPosition, setAssistantPosition] = useState({ top: "80%" });

//     useEffect(() => {
//         if (chatBoxRef.current) {
//             chatBoxRef.current.scrollTop = 0;
//         }
//     }, []);

//     useEffect(() => {
//         if (messages.length > 1) {
//             messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//         }
//     }, [messages]);

//     const handleScroll = () => {
//         if (!chatBoxRef.current) return;
//         const chatBox = chatBoxRef.current;
//         const msgElements = Array.from(chatBox.querySelectorAll(".chat-message"));
//         let closestMsg = null;
//         let closestDist = Infinity;

//         msgElements.forEach((el) => {
//             const rect = el.getBoundingClientRect();
//             const dist = Math.abs(rect.top - window.innerHeight / 2);
//             if (dist < closestDist) {
//                 closestDist = dist;
//                 closestMsg = el;
//             }
//         });

//         if (closestMsg) {
//             const rect = closestMsg.getBoundingClientRect();
//             setAssistantPosition({ top: rect.top + window.scrollY + rect.height / 2 });
//         }
//     };

//     useEffect(() => {
//         const chatBox = chatBoxRef.current;
//         if (chatBox) {
//             chatBox.addEventListener("scroll", handleScroll);
//             handleScroll();
//         }
//         return () => chatBox?.removeEventListener("scroll", handleScroll);
//     }, [messages]);

//     const handleSend = () => {
//         if (input.trim() === "") return;
//         const newMsg = { id: Date.now(), text: input, sender: "user" };
//         setMessages([...messages, newMsg]);

//         setTimeout(() => {
//             const botReply = {
//                 id: Date.now(),
//                 text: t("chat.botReply"),
//                 sender: "bot",
//             };
//             setMessages((prev) => [...prev, botReply]);
//         }, 1000);

//         setInput("");
//     };

//     const startListening = () => {
//         if (!("webkitSpeechRecognition" in window)) {
//             alert("⚠️ المتصفح لا يدعم التعرف على الصوت");
//             return;
//         }

//         const recognition = new window.webkitSpeechRecognition();
//         recognition.lang = i18n.language === "en" ? "en-US" : "ar-SA";
//         recognition.continuous = false;
//         recognition.interimResults = false;

//         recognition.onstart = () => setListening(true);
//         recognition.onend = () => setListening(false);

//         recognition.onresult = (event) => {
//             const transcript = event.results[0][0].transcript;
//             setInput(transcript);
//         };

//         recognition.start();
//         recognitionRef.current = recognition;
//     };

//     return (
//         <div className={`chat-container ${darkMode ? "dark" : ""}`}>
//             <div className="chat-box" ref={chatBoxRef}>
//                 {messages.map((msg) => (
//                     <div
//                         key={msg.id}
//                         data-id={msg.id}
//                         className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
//                     >
//                         <div className="message-bubble">{msg.text}</div>
//                     </div>
//                 ))}
//                 <div ref={messagesEndRef} />
//             </div>

//             <div
//                 className="chat-assistant"
//                 style={{ top: assistantPosition.top }}
//             >
//                 <img src="/robot.png" alt="robot assistant" />
//             </div>

//             <div className="chat-input-container">
//                 <input
//                     type="text"
//                     className="chat-input"
//                     value={input}
//                     onChange={(e) => setInput(e.target.value)}
//                     placeholder={t("chat.placeholder")}
//                     onKeyDown={(e) => e.key === "Enter" && handleSend()}
//                 />
//                 <button
//                     className={`mic-btn ${listening ? "active" : ""}`}
//                     onClick={startListening}
//                 >
//                     {listening ? t("chat.listening") : t("chat.mic")}
//                 </button>
//                 <button className="send-btn" onClick={handleSend}>
//                     {t("chat.send")}
//                 </button>
//             </div>
//         </div>
//     );
// }

import React, { useState, useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import "./../styles/Chat.css";

const API = "http://localhost:8000/api/v1/chat";

export default function Chat({ username, darkMode }) {
  const { t, i18n } = useTranslation();

  // Chat messages
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: t("chat.botWelcome", { name: username || t("friend") }),
      sender: "bot",
    },
  ]);

  // Input & options
  const [input, setInput] = useState("");
  const [generateImage, setGenerateImage] = useState(false);

  // Speech-to-text
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef(null);

  // Refs for auto-scroll
  const messagesEndRef = useRef(null);
  const chatBoxRef     = useRef(null);

  // Scroll to bottom whenever messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // SEND handler: calls backend, plays TTS, displays image
  const handleSend = async () => {
    const text = input.trim();
    if (!text) return;

    console.log("🔥 handleSend()", { text, generateImage });

    // show user message
    setMessages(prev => [
      ...prev,
      { id: Date.now(), text, sender: "user" },
    ]);
    setInput("");

    const token = localStorage.getItem("token");
    console.log("🔑 token:", token);
    if (!token) {
      alert("⚠️ You must be logged in to chat.");
      return;
    }
    

    try {
      console.log("🌐 calling fetch to", API + "/");
      const resp = await fetch(API + "/", {
        method: "POST",
        headers: {
          "Content-Type":  "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({ text, generate_image: generateImage }),
      });
      console.log("🌐 response status:", resp.status);

      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        console.error("❌ backend error payload:", err);
        throw new Error(err.detail || resp.statusText);
      }

      const data = await resp.json();
      console.log("📨 ChatResponse JSON:", data);

      // play TTS audio
      if (data.audio_base64) {
        new Audio(`data:audio/mp3;base64,${data.audio_base64}`)
          .play()
          .catch(() => {});
      }

      // append bot reply (and optional image)
      setMessages(prev => [
        ...prev,
        {
          id:    Date.now() + 1,
          text:  data.text,
          sender:"bot",
          image: data.image_url,    // base64 or URL from backend
        },
      ]);
    } catch (e) {
      console.error("💥 handleSend caught:", e);
      setMessages(prev => [
        ...prev,
        { id: Date.now() + 2, text: "⚠️ " + e.message, sender: "bot" },
      ]);
    }
  };

  // Start browser speech recognition
  const startListening = () => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("⚠️ Your browser does not support speech recognition.");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = i18n.language === "en" ? "en-US" : "ar-SA";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => setListening(true);
    recognition.onend   = () => setListening(false);

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      setInput(transcript);
    };

    recognition.start();
    recognitionRef.current = recognition;
  };

  return (
    <div className={`chat-container ${darkMode ? "dark" : ""}`}>
      <div className="chat-box" ref={chatBoxRef}>
        {messages.map(msg => (
          <div key={msg.id} className={`chat-message ${msg.sender}`}>
            <div className="message-bubble">
              {msg.text}
              {msg.image && (
                <img
                  src={msg.image.startsWith("data:")
                    ? msg.image
                    : `data:image/png;base64,${msg.image}`}
                  alt="generated"
                  className="chat-image"
                />
              )}
            </div>
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          value={input}
          placeholder={t("chat.placeholder")}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleSend()}
        />

        <button
          className={`mic-btn ${listening ? "active" : ""}`}
          onClick={startListening}
        >
          {listening ? t("chat.listening") : t("chat.mic")}
        </button>

        <label className="image-toggle">
          <input
            type="checkbox"
            checked={generateImage}
            onChange={e => setGenerateImage(e.target.checked)}
          />{" "}
          {t("chat.generateImage")}
        </label>

        <button className="send-btn" onClick={handleSend}>
          {t("chat.send")}
        </button>
      </div>
    </div>
  );
}
