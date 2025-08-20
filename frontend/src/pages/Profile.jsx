// import React, { useState, useEffect } from "react";
// import "./../styles/Profile.css";
// import { useTranslation } from "react-i18next";
// import "../styles/Header.css";



// export default function Profile({ setUsernameGlobal, setAvatarGlobal, darkMode }) {
//     const [username, setUsername] = useState("");
//     const [avatar, setAvatar] = useState(null);
//     const { t, i18n } = useTranslation();

//     useEffect(() => {
//         const storedName = localStorage.getItem("username");
//         const storedAvatar = localStorage.getItem("avatar");
//         if (storedName) setUsername(storedName);
//         if (storedAvatar) setAvatar(storedAvatar);
//     }, []);

//     const handleSave = () => {
//         if (!username) {
//             alert("⚠️ الرجاء إدخال اسمك");
//             return;
//         }
//         localStorage.setItem("username", username);
//         setUsernameGlobal(username);

//         if (avatar) {
//             localStorage.setItem("avatar", avatar);
//             setAvatarGlobal(avatar);
//         }
//         alert("✅ تم حفظ التغييرات بنجاح");
//     };

//     const handleAvatarChange = (e) => {
//         const file = e.target.files[0];
//         if (file) {
//             const reader = new FileReader();
//             reader.onloadend = () => {
//                 setAvatar(reader.result);
//             };
//             reader.readAsDataURL(file);
//         }
//     };

//     return (
//         <div className={`profile-page ${darkMode ? "dark" : ""}`}>
//             <h2>{t("Profile_Title")}</h2>

//             <div className="avatar-box">
//                 {avatar ? (
//                     <img src={avatar} alt="Avatar" className="avatar-preview" />
//                 ) : (
//                     <div className="avatar-placeholder">👤</div>
//                 )}
//                 <input type="file" accept="image/*" onChange={handleAvatarChange} />
//             </div>

//             <input
//                 type="text"
//                 value={username}
//                 onChange={(e) => setUsername(e.target.value)}
//                 placeholder="اسمك"
//                 className="username-input"
//             />

//             <button onClick={handleSave} className="save-btn">
//                 💾 حفظ
//             </button>
//         </div>
//     );
// }


import React, { useState, useEffect } from "react";
import "./../styles/Profile.css";
import { useTranslation } from "react-i18next";

const API_ME = "http://localhost:8000/api/v1/users/me";

export default function Profile({ setUsernameGlobal, setAvatarGlobal, darkMode }) {
  const { t } = useTranslation();

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [autismLevel, setAutismLevel] = useState("");
  const [disorderType, setDisorderType] = useState("");
  const [avatar, setAvatar] = useState(null);

  const logoutAndRedirect = (msg = "Session expired. Please log in again.") => {
    try {
      localStorage.removeItem("token");
    } catch {}
    alert(msg);
    window.location.href = "/";
  };

  const fetchJSON = async (url, options = {}) => {
    const resp = await fetch(url, options);
    if (!resp.ok) {
      let detail = "";
      try {
        const j = await resp.clone().json();
        detail =
          (typeof j?.detail === "string" && j.detail) ||
          (Array.isArray(j?.detail) ? j.detail.map((d) => d?.msg || d).join("; ") : "") ||
          JSON.stringify(j);
      } catch {
        try {
          detail = await resp.text();
        } catch {
          detail = resp.statusText;
        }
      }

      if (String(detail).includes("Invalid token subject")) {
        logoutAndRedirect();
        throw new Error(detail);
      }
      if (resp.status === 401 || resp.status === 403) {
        logoutAndRedirect();
        throw new Error(detail || "Unauthorized");
      }

      throw new Error(detail || resp.statusText);
    }
    return resp.json();
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      logoutAndRedirect("Please log in to view your profile.");
      return;
    }

    const fetchUser = async () => {
      try {
        setLoading(true);
        const data = await fetchJSON(API_ME, {
          headers: { Authorization: `Bearer ${token}` },
        });

        setUsername(data?.username || data?.name || "");
        setEmail(data?.email || "");
        setAutismLevel(data?.autism_level || "");
        setDisorderType(data?.disorder_type || "");
        setAvatar(
          data?.avatar_url || data?.avatar || localStorage.getItem("avatar") || null
        );
        setError("");
      } catch (e) {
        setError(e.message || String(e));
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, []); // runs once on mount

  const handleAvatarChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onloadend = () => setAvatar(reader.result);
    reader.readAsDataURL(file);
  };

  const handleSave = async () => {
    const token = localStorage.getItem("token");
    if (!token) {
      logoutAndRedirect("Please log in to update your profile.");
      return;
    }
    if (!username) {
      alert(t("profile.missingName") || "⚠️ Please enter your name");
      return;
    }

    try {
      setSaving(true);
      setError("");

      const payload = {
        username,
        email,
        autism_level: autismLevel,
        disorder_type: disorderType,
        avatar: avatar,
      };

      await fetchJSON(API_ME, {
        method: "PUT", // or PATCH
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      localStorage.setItem("username", username);
      if (avatar) localStorage.setItem("avatar", avatar);

      setUsernameGlobal?.(username);
      setAvatarGlobal?.(avatar || null);

      alert(t("profile.saved") || "✅ Changes saved successfully");
    } catch (e) {
      setError(e.message || String(e));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className={`profile-page ${darkMode ? "dark" : ""}`}>
      <h2>{t("Profile_Title") || "Profile"}</h2>

      {loading ? (
        <div className="profile-loading">{t("loading") || "Loading..."}</div>
      ) : (
        <>
          {error && <div className="profile-error">⚠️ {error}</div>}

          <div className="avatar-box">
            {avatar ? (
              <img src={avatar} alt="Avatar" className="avatar-preview" />
            ) : (
              <div className="avatar-placeholder">👤</div>
            )}
            <input type="file" accept="image/*" onChange={handleAvatarChange} />
          </div>

          <label className="profile-label">
            {t("profile.name") || "Name"}
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder={t("profile.namePH") || "Your name"}
              className="username-input"
            />
          </label>

          <label className="profile-label">
            {t("profile.email") || "Email"}
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={t("profile.emailPH") || "your@email.com"}
              className="email-input"
            />
          </label>

          <label className="profile-label">
            {t("profile.autismLevel") || "Autism level"}
            <select
              className="select-input"
              value={autismLevel}
              onChange={(e) => setAutismLevel(e.target.value)}
            >
              <option value="">{t("profile.select") || "Select..."}</option>
              <option value="level_1">{t("profile.level1") || "Level 1"}</option>
              <option value="level_2">{t("profile.level2") || "Level 2"}</option>
              <option value="level_3">{t("profile.level3") || "Level 3"}</option>
            </select>
          </label>

          <label className="profile-label">
            {t("profile.disorderType") || "Disorder type"}
            <input
              type="text"
              value={disorderType}
              onChange={(e) => setDisorderType(e.target.value)}
              placeholder={t("profile.disorderPH") || "e.g., ASD"}
              className="disorder-input"
            />
          </label>

          <button onClick={handleSave} className="save-btn" disabled={saving}>
            {saving ? (t("saving") || "Saving...") : "💾 " + (t("save") || "Save")}
          </button>
        </>
      )}
    </div>
  );
}
