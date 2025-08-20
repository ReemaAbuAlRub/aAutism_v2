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


// import React, { useState, useEffect, useRef } from "react";
// import { useTranslation } from "react-i18next";
// import "./../styles/Chat.css";

// const API = "http://localhost:8000/api/v1/chat";

// export default function Chat({ username, darkMode }) {
//   const { t, i18n } = useTranslation();

//   const [messages, setMessages] = useState([
//     {
//       id: 1,
//       text: t("chat.botWelcome", { name: username || t("friend") }),
//       sender: "bot",
//     },
//   ]);
//   const [input, setInput] = useState("");
//   const generateImage = true; // always on, hidden
//   const [listening, setListening] = useState(false);
//   const recognitionRef = useRef(null);
//   const messagesEndRef = useRef(null);

//   useEffect(() => {
//     messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
//   }, [messages]);

//   const playTTS = (audioBase64) => {
//     if (!audioBase64) return;
//     const audio = new Audio(`data:audio/mp3;base64,${audioBase64}`);
//     audio.play().catch(() => {});
//   };

//   const handleSend = async () => {
//     const text = input.trim();
//     if (!text) return;

//     // Add user message
//     setMessages((prev) => [...prev, { id: Date.now(), text, sender: "user" }]);
//     setInput("");

//     const token = localStorage.getItem("token");
//     if (!token) {
//       alert("⚠️ You must be logged in to chat.");
//       return;
//     }

//     // Add typing indicator
//     const typingId = Date.now() + 0.5;
//     setMessages((prev) => [
//       ...prev,
//       { id: typingId, text: "typing", sender: "bot-typing" },
//     ]);

//     try {
//       const resp = await fetch(API + "/", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/json",
//           Authorization: `Bearer ${token}`,
//         },
//         body: JSON.stringify({ text, generate_image: generateImage }),
//       });

//       if (!resp.ok) {
//         const err = await resp.json().catch(() => ({}));
//         throw new Error(err.detail || resp.statusText);
//       }

//       const data = await resp.json();

//       // Replace typing indicator with actual message
//       setMessages((prev) =>
//         prev.map((m) =>
//           m.id === typingId
//             ? {
//                 id: Date.now() + 1,
//                 text: data.text,
//                 sender: "bot",
//                 image: data.image_url || null,
//                 audioBase64: data.audio_base64 || null,
//               }
//             : m
//         )
//       );
//     } catch (e) {
//       setMessages((prev) =>
//         prev.map((m) =>
//           m.id === typingId
//             ? { id: Date.now() + 2, text: "⚠️ " + e.message, sender: "bot" }
//             : m
//         )
//       );
//     }
//   };

//   const startListening = () => {
//     if (!("webkitSpeechRecognition" in window)) {
//       alert("⚠️ Your browser does not support speech recognition.");
//       return;
//     }
//     const recognition = new window.webkitSpeechRecognition();
//     recognition.lang = i18n.language === "en" ? "en-US" : "ar-SA";
//     recognition.continuous = false;
//     recognition.interimResults = false;
//     recognition.onstart = () => setListening(true);
//     recognition.onend = () => setListening(false);
//     recognition.onresult = (e) => {
//       const transcript = e.results[0][0].transcript;
//       setInput(transcript);
//     };
//     recognition.start();
//     recognitionRef.current = recognition;
//   };

//   const resolveImageSrc = (val) => {
//     if (!val) return null;
//     if (val.startsWith("data:")) return val;
//     if (/^https?:\/\//i.test(val)) return val;
//     return `data:image/png;base64,${val}`;
//   };

//   return (
//     <div className={`chat-container ${darkMode ? "dark" : ""}`}>
//       <div className="chat-box">
//         {messages.map((msg) => {
//           if (msg.sender === "bot-typing") {
//             return (
//               <div key={msg.id} className="chat-row bot">
//                 <div className="message-bubble bot typing">
//                   <span className="typing-dots">
//                     <span></span>
//                     <span></span>
//                     <span></span>
//                   </span>
//                 </div>
//               </div>
//             );
//           }

//           const isBot = msg.sender === "bot";
//           const imgSrc = resolveImageSrc(msg.image);

//           return (
//             <div key={msg.id} className={`chat-row ${msg.sender}`}>
//               {isBot && <img src="/robot.png" alt="bot" className="chat-avatar" />}

//               <div className="chat-content">
//                 <div className={`message-bubble ${msg.sender}`}>
//                   <div className="bubble-row">
//                     <span>{msg.text}</span>
//                     {isBot && msg.audioBase64 && (
//                       <button
//                         className="tts-btn"
//                         title={t("chat.playAudio") || "Play audio"}
//                         onClick={() => playTTS(msg.audioBase64)}
//                       >
//                         🔊
//                       </button>
//                     )}
//                   </div>
//                 </div>

//                 {isBot && imgSrc && (
//                   <img src={imgSrc} alt="generated" className="chat-generated-image" />
//                 )}
//               </div>
//             </div>
//           );
//         })}
//         <div ref={messagesEndRef} />
//       </div>

//       <div className="chat-input-container">
//         <input
//           type="text"
//           className="chat-input"
//           value={input}
//           placeholder={t("chat.placeholder")}
//           onChange={(e) => setInput(e.target.value)}
//           onKeyDown={(e) => e.key === "Enter" && handleSend()}
//         />
//         <button className={`mic-btn ${listening ? "active" : ""}`} onClick={startListening}>
//           {listening ? t("chat.listening") : t("chat.mic")}
//         </button>
//         <button className="send-btn" onClick={handleSend}>
//           {t("chat.send")}
//         </button>
//       </div>
//     </div>
//   );
// }


import React, { useState, useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";
import "./../styles/Chat.css";

const API = "http://localhost:8000/api/v1/chat";

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
  const generateImage = true;
  const [listening, setListening] = useState(false);

  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const logoutAndRedirect = (msg = "Session expired. Please log in again.") => {
    try {
      localStorage.removeItem("token");
    } catch (_) {}
    alert(msg);
    setMessages((prev) => prev.filter((m) => m.sender !== "bot-typing"));
    window.location.href = "/";
  };

  const playTTS = (audioBase64) => {
    if (!audioBase64) return;
    const audio = new Audio(`data:audio/mp3;base64,${audioBase64}`);
    audio.play().catch(() => {});
  };

  const extractErrorDetail = async (resp) => {
    try {
      const data = await resp.clone().json();
      if (typeof data === "string") return data;
      if (data?.detail) {
        if (typeof data.detail === "string") return data.detail;
        if (Array.isArray(data.detail)) {
          return data.detail.map((d) => d?.msg || d).join("; ");
        }
        if (typeof data.detail === "object") {
          return JSON.stringify(data.detail);
        }
      }
      return JSON.stringify(data);
    } catch (_) {
      try {
        return await resp.text();
      } catch (__) {
        return resp.statusText || "Unknown error";
      }
    }
  };

  const getSpeechRecognition = () =>
    window.SpeechRecognition || window.webkitSpeechRecognition || null;

  const getSpeechLang = () => {
    const lang = i18n.language || "en";
    if (lang.startsWith("ar")) return "ar-SA";
    if (lang.startsWith("en")) return "en-US";
    return "en-US";
  };

  useEffect(() => {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition || null;
    if (!SR) return;
  
    let rec = recognitionRef.current;
  
    if (!rec) {
      rec = new SR();
      rec.continuous = false;
      rec.interimResults = false;
  
      rec.onstart = () => setListening(true);
      rec.onend = () => setListening(false);
      rec.onerror = (e) => {
        setListening(false);
        if (e?.error === "not-allowed" || e?.error === "service-not-allowed") {
          alert(t("chat.micBlocked") || "Microphone permission is blocked in your browser.");
        }
      };
      rec.onresult = (e) => {
        const transcript = e?.results?.[0]?.[0]?.transcript || "";
        if (transcript) setInput(transcript);
        // Optionally auto-send:
        // if (transcript) setTimeout(() => handleSend(), 0);
      };
  
      recognitionRef.current = rec;
    }
  
    // keep language in sync with i18n
    const lang = i18n.language?.startsWith("ar") ? "ar-SA" : "en-US";
    rec.lang = lang;
  
    // cleanup
    return () => {
      try { rec.stop(); } catch {}
    };
  }, [i18n.language, t]); // no eslint-disable needed
  

  const handleSend = async () => {
    const text = input.trim();
    if (!text) return;

    setMessages((prev) => [...prev, { id: Date.now(), text, sender: "user" }]);
    setInput("");

    const token = localStorage.getItem("token");
    if (!token) {
      alert("⚠️ You must be logged in to chat.");
      window.location.href = "/";
      return;
    }

    const typingId = Date.now() + 0.5;
    setMessages((prev) => [
      ...prev,
      { id: typingId, text: "typing", sender: "bot-typing" },
    ]);

    try {
      const resp = await fetch(API + "/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ text, generate_image: generateImage }),
      });

      if (!resp.ok) {
        const detail = (await extractErrorDetail(resp)) || "";
        const normalized = String(detail);

        if (
          normalized.includes("Invalid token subject") ||
          normalized.includes("⚠️ Invalid token subject")
        ) {
          logoutAndRedirect("Session expired. Please log in again.");
          return;
        }

        throw new Error(normalized);
      }

      const data = await resp.json();

      setMessages((prev) =>
        prev.map((m) =>
          m.id === typingId
            ? {
                id: Date.now() + 1,
                text: data.text,
                sender: "bot",
                image: data.image_url || null,
                audioBase64: data.audio_base64 || null,
              }
            : m
        )
      );
    } catch (e) {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === typingId
            ? {
                id: Date.now() + 2,
                text: "⚠️ " + (e.message || String(e)),
                sender: "bot",
              }
            : m
        )
      );
    }
  };

  const toggleListening = () => {
    const SR = getSpeechRecognition();
    if (!SR) {
      alert("⚠️ " + (t("chat.noSpeechAPI") || "Your browser does not support speech recognition."));
      return;
    }
    const rec = recognitionRef.current;
    if (!rec) return;

    try {
      if (listening) {
        rec.stop();
      } else {
        // must be HTTPS or localhost + user gesture
        rec.lang = getSpeechLang();
        rec.start();
      }
    } catch (err) {
      alert(
        t("chat.micStartFail") ||
          "Could not access the microphone. Ensure HTTPS/localhost and allow mic permissions."
      );
    }
  };

  const resolveImageSrc = (val) => {
    if (!val) return null;
    if (val.startsWith("data:")) return val;
    if (/^https?:\/\//i.test(val)) return val;
    return `data:image/png;base64,${val}`;
  };

  return (
    <div className={`chat-container ${darkMode ? "dark" : ""}`}>
      <div className="chat-box">
        {messages.map((msg) => {
          if (msg.sender === "bot-typing") {
            return (
              <div key={msg.id} className="chat-row bot">
                <div className="message-bubble bot typing">
                  <span className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </span>
                </div>
              </div>
            );
          }

          const isBot = msg.sender === "bot";
          const imgSrc = resolveImageSrc(msg.image);

          return (
            <div key={msg.id} className={`chat-row ${msg.sender}`}>
              {isBot && <img src="/robot.png" alt="bot" className="chat-avatar" />}

              <div className="chat-content">
                <div className={`message-bubble ${msg.sender}`}>
                  <div className="bubble-row">
                    <span>{msg.text}</span>
                    {isBot && msg.audioBase64 && (
                      <button
                        className="tts-btn"
                        title={t("chat.playAudio") || "Play audio"}
                        onClick={() => playTTS(msg.audioBase64)}
                      >
                        🔊
                      </button>
                    )}
                  </div>
                </div>

                {isBot && imgSrc && (
                  <img src={imgSrc} alt="generated" className="chat-generated-image" />
                )}
              </div>
            </div>
          );
        })}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          value={input}
          placeholder={t("chat.placeholder")}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button className={`mic-btn ${listening ? "active" : ""}`} onClick={toggleListening}>
          {listening ? t("chat.listening") : t("chat.mic")}
        </button>
        <button className="send-btn" onClick={handleSend}>
          {t("chat.send")}
        </button>
      </div>
    </div>
  );
}
