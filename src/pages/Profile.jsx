import React, { useState, useEffect } from "react";
import "./../styles/Profile.css";

export default function Profile({ setUsernameGlobal, setAvatarGlobal, darkMode }) {
    const [username, setUsername] = useState("");
    const [avatar, setAvatar] = useState(null);

    useEffect(() => {
        const storedName = localStorage.getItem("username");
        const storedAvatar = localStorage.getItem("avatar");
        if (storedName) setUsername(storedName);
        if (storedAvatar) setAvatar(storedAvatar);
    }, []);

    const handleSave = () => {
        if (!username) {
            alert("⚠️ الرجاء إدخال اسمك");
            return;
        }
        localStorage.setItem("username", username);
        setUsernameGlobal(username);

        if (avatar) {
            localStorage.setItem("avatar", avatar);
            setAvatarGlobal(avatar);
        }
        alert("✅ تم حفظ التغييرات بنجاح");
    };

    const handleAvatarChange = (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onloadend = () => {
                setAvatar(reader.result);
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <div className={`profile-page ${darkMode ? "dark" : ""}`}>
            <h2>✏️ تعديل الملف الشخصي</h2>

            <div className="avatar-box">
                {avatar ? (
                    <img src={avatar} alt="Avatar" className="avatar-preview" />
                ) : (
                    <div className="avatar-placeholder">👤</div>
                )}
                <input type="file" accept="image/*" onChange={handleAvatarChange} />
            </div>

            <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="اسمك"
                className="username-input"
            />

            <button onClick={handleSave} className="save-btn">
                💾 حفظ
            </button>
        </div>
    );
}
