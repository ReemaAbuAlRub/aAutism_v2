// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom";
// import { useTranslation } from "react-i18next";
// import LeftPanel from "../components/LeftPanel";
// import { LOGIN_URL } from "../config/api";
// import { afterAuthNavigate } from "../utils/user";
// import "../styles/SignupPage.css";

// export default function LoginPage({ setUsername, darkMode }) {
//   const { t } = useTranslation();
//   const navigate = useNavigate();
//   const [loading, setLoading] = useState(false);
//   const [email, setEmail] = useState("");
//   const [password, setPassword] = useState("");

//   const handleSignin = async () => {
//     if (!email || !password) {
//       alert(t("alerts.fillEmailPassword"));
//       return;
//     }
//     setLoading(true);
//     try {
//       const form = new URLSearchParams();
//       form.append("grant_type", "password");
//       form.append("username", email);
//       form.append("password", password);

//       const resp = await fetch(LOGIN_URL, {
//         method: "POST",
//         headers: { "Content-Type": "application/x-www-form-urlencoded" },
//         body: form.toString(),
//       });
//       if (!resp.ok) {
//         const err = await resp.json().catch(() => ({}));
//         throw new Error(err.detail || resp.statusText);
//       }
//       const { access_token } = await resp.json();
//       localStorage.setItem("token", access_token);

//       await afterAuthNavigate({ token: access_token, setUsername, navigate });
//     } catch (e) {
//       console.error("Login failed:", e);
//       alert(t("alerts.loginFailed") + ": " + e.message);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className={`signup-page ${darkMode ? "dark" : ""}`}>
//       <div className="page-layout">
//         <LeftPanel title={t("signupPage.signinTitle")} />
//         <div className="right-section">
//           <div className="form-box modern-form">
//             <h2 className="form-title">{t("signupPage.signinTitle")}</h2>
//             <input
//               type="email"
//               name="email"
//               placeholder={t("signupPage.signinEmailPlaceholder")}
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//             />
//             <input
//               type="password"
//               name="password"
//               placeholder={t("signupPage.signinPasswordPlaceholder")}
//               value={password}
//               onChange={(e) => setPassword(e.target.value)}
//             />
//             <button className="signin-btn" onClick={handleSignin} disabled={loading}>
//               {loading ? t("loading") : t("signupPage.signinBtn")}
//             </button>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }


import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
import LeftPanel from "../components/LeftPanel";
import "../styles/SignupPage.css";

const API_BASE = "http://localhost:8000/api/v1";
const LOGIN_URL = `${API_BASE}/user/login`;
const ME_URL = `${API_BASE}/user/me`;

export default function LoginPage({ setUsername, darkMode, onLogin }) {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const { t } = useTranslation();
  const navigate = useNavigate();

  const deriveDisplayName = (profile) => {
    const { username, first_name, last_name, full_name, email, name } = profile || {};
    return full_name || name || username || [first_name, last_name].filter(Boolean).join(" ") || (email ? email.split("@")[0] : "") || "User";
  };

  const handleChange = (e) => setFormData((p) => ({ ...p, [e.target.name]: e.target.value }));

  const fetchMeAndGoto = async () => {
    const token = localStorage.getItem("token");
    const meResp = await fetch(ME_URL, { headers: { Authorization: `Bearer ${token}` } });
    if (!meResp.ok) throw new Error((await meResp.json().catch(() => ({}))).detail || meResp.statusText);
    const me = await meResp.json();
    const displayName = deriveDisplayName(me);
    setUsername(displayName);
    localStorage.setItem("username", displayName);
    localStorage.setItem("answeredQuestion", "true");
    onLogin?.(displayName); // ✅ flips App.isLoggedIn true → Header shows Logout
    navigate("/welcome");
  };

  const handleSignin = async () => {
    if (!formData.email || !formData.password) return alert(t("alerts.fillEmailPassword"));
    setLoading(true);
    try {
      const form = new URLSearchParams();
      form.append("grant_type", "password");
      form.append("username", formData.email);
      form.append("password", formData.password);
      const resp = await fetch(LOGIN_URL, { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: form.toString() });
      if (!resp.ok) throw new Error((await resp.json().catch(() => ({}))).detail || resp.statusText);
      const { access_token } = await resp.json();
      localStorage.setItem("token", access_token); // <-- must happen BEFORE onLogin
      await fetchMeAndGoto();
    } catch (e) {
      console.error("Login failed:", e);
      alert(t("alerts.loginFailed") + ": " + e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`signup-page ${darkMode ? "dark" : ""}`}>
      <div className="page-layout">
        <LeftPanel title={t("signupPage.signinTitle")} />
        <div className="right-section">
          <div className="form-box modern-form">
            <h2 className="form-title">{t("signupPage.signinTitle")}</h2>
            <input type="email" name="email" placeholder={t("signupPage.signinEmailPlaceholder")} onChange={handleChange} />
            <input type="password" name="password" placeholder={t("signupPage.signinPasswordPlaceholder")} onChange={handleChange} />
            <button className="modern-btn signin-btn" onClick={handleSignin} disabled={loading}>
              {loading ? t("loading") : t("signupPage.signinBtn")}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}