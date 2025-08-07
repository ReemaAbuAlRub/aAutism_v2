// import React, { useState, useEffect } from "react";
// import { useNavigate } from "react-router-dom";
// import { motion } from "framer-motion";
// import { useTranslation } from "react-i18next";
// import "./../styles/SignupPage.css";

// export default function SignupPage({ externalStep, setUsername, darkMode }) {
//     const [step, setStep] = useState("question");
//     const [showBreathing, setShowBreathing] = useState(false);
//     const [showNamePopup, setShowNamePopup] = useState(false);
//     const [tempName, setTempName] = useState("");
//     const [formData, setFormData] = useState({
//         name: "",
//         birthDate: "",
//         age: "",
//         autismLevel: "",
//         email: "",
//         password: "",
//     });

//     const { t } = useTranslation();
//     const navigate = useNavigate();

//     useEffect(() => {
//         // إذا المستخدم جاوب السؤال قبل هيك
//         if (localStorage.getItem("answeredQuestion")) {
//             setStep("signin");
//         }
//     }, []);

//     useEffect(() => {
//         if (externalStep && externalStep !== step) {
//             setStep(externalStep);
//         }
//     }, [externalStep, step]);

//     // حساب العمر تلقائياً
//     useEffect(() => {
//         if (formData.birthDate) {
//             const birth = new Date(formData.birthDate);
//             const today = new Date();
//             let age = today.getFullYear() - birth.getFullYear();
//             const m = today.getMonth() - birth.getMonth();
//             if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
//                 age--;
//             }
//             setFormData((prev) => ({ ...prev, age: age }));
//         }
//     }, [formData.birthDate]);

//     const handleChange = (e) => {
//         setFormData({ ...formData, [e.target.name]: e.target.value });
//     };

//     // تسجيل الدخول
//     const handleSignin = () => {
//         if (!formData.email || !formData.password) {
//             alert(t("alerts.fillEmailPassword"));
//             return;
//         }
//         const storedName = localStorage.getItem("username");
//         if (!storedName) {
//             setShowNamePopup(true);
//         } else {
//             localStorage.setItem("answeredQuestion", "true"); // حفظ إنو جاوب
//             setUsername(storedName);
//             navigate("/welcome");
//         }
//     };

//     // إنشاء حساب
//     const handleSignup = () => {
//         if (
//             !formData.name ||
//             !formData.email ||
//             !formData.password ||
//             !formData.birthDate ||
//             !formData.autismLevel
//         ) {
//             alert(t("alerts.fillAllFields"));
//             return;
//         }
//         localStorage.setItem("username", formData.name);
//         localStorage.setItem("birthDate", formData.birthDate);
//         localStorage.setItem("age", formData.age);
//         localStorage.setItem("autismLevel", formData.autismLevel);
//         localStorage.setItem("answeredQuestion", "true"); // حفظ إنو جاوب

//         setUsername(formData.name);
//         navigate("/welcome");
//     };

//     // حفظ الاسم من البوب أب
//     const handleSaveName = () => {
//         if (!tempName.trim()) {
//             alert(t("signupPage.popupEnterName"));
//             return;
//         }
//         localStorage.setItem("username", tempName);
//         localStorage.setItem("answeredQuestion", "true"); // حفظ إنو جاوب
//         setUsername(tempName);
//         setShowNamePopup(false);
//         navigate("/welcome");
//     };

//     // تحديد تاريخ اليوم كحد أقصى
//     const today = new Date().toISOString().split("T")[0];

//     return (
//         <div className={`signup-page ${darkMode ? "dark" : ""}`}>
//             <div className="page-layout">
//                 {/* يسار */}
//                 <div className="left-section">
//                     <motion.img
//                         src="/robot.png"
//                         alt="Robot"
//                         className="robot-animated-big"
//                         animate={{ rotate: [0, 5, -5, 0] }}
//                         transition={{ repeat: Infinity, duration: 3 }}
//                     />
//                     <h1 className="app-name">{t("appName")}</h1>
//                     <h3 className="page-title">
//                         {step === "signin"
//                             ? t("signupPage.signinTitle")
//                             : step === "signup"
//                                 ? t("signupPage.signupTitle")
//                                 : t("signupPage.questionTitle")}
//                     </h3>

//                     {/* زر تمرين التهدئة */}
//                     <button
//                         className="breathing-btn"
//                         onClick={() => setShowBreathing(true)}
//                     >
//                         {t("signupPage.breathingExerciseBtn")}
//                     </button>

//                     {showBreathing && (
//                         <div className="breathing-modal">
//                             <div className="modal-content">
//                                 <h2>{t("signupPage.breathingExerciseTitle")}</h2>
//                                 <p>{t("signupPage.breathingExerciseText")}</p>
//                                 <motion.div
//                                     className="breathing-circle"
//                                     animate={{ scale: [1, 1.4, 1] }}
//                                     transition={{ repeat: Infinity, duration: 4 }}
//                                 />
//                                 <button
//                                     className="close-btn"
//                                     onClick={() => setShowBreathing(false)}
//                                 >
//                                     {t("signupPage.popupClose")}
//                                 </button>
//                             </div>
//                         </div>
//                     )}
//                 </div>

//                 {/* يمين */}
//                 <div className="right-section">
//                     {step === "question" && (
//                         <motion.div
//                             className="form-box modern-form no-bg"
//                             initial={{ opacity: 0, x: 50 }}
//                             animate={{ opacity: 1, x: 0 }}
//                             transition={{ duration: 0.8 }}
//                         >
//                             <h2 className="form-title">{t("signupPage.questionTitle")}</h2>
//                             <div className="question-buttons">
//                                 <button
//                                     onClick={() => {
//                                         setStep("signin");
//                                         localStorage.setItem("answeredQuestion", "true");
//                                     }}
//                                     className="modern-btn yes-btn"
//                                 >
//                                     {t("signupPage.yes")}
//                                 </button>
//                                 <button
//                                     onClick={() => {
//                                         setStep("signup");
//                                         localStorage.setItem("answeredQuestion", "true");
//                                     }}
//                                     className="modern-btn no-btn"
//                                 >
//                                     {t("signupPage.no")}
//                                 </button>
//                             </div>
//                         </motion.div>
//                     )}

//                     {step === "signin" && (
//                         <div className="form-box modern-form">
//                             <h2 className="form-title">{t("signupPage.signinTitle")}</h2>
//                             <input
//                                 type="email"
//                                 name="email"
//                                 placeholder={t("signupPage.signinEmailPlaceholder")}
//                                 onChange={handleChange}
//                             />
//                             <input
//                                 type="password"
//                                 name="password"
//                                 placeholder={t("signupPage.signinPasswordPlaceholder")}
//                                 onChange={handleChange}
//                             />
//                             <button className="modern-btn signin-btn" onClick={handleSignin}>
//                                 {t("signupPage.signinBtn")}
//                             </button>
//                         </div>
//                     )}

//                     {step === "signup" && (
//                         <div className="form-box modern-form">
//                             <h2 className="form-title">{t("signupPage.signupTitle")}</h2>
//                             <input
//                                 type="text"
//                                 name="name"
//                                 placeholder={t("signupPage.signupNamePlaceholder")}
//                                 onChange={handleChange}
//                             />
//                             <input
//                                 type="date"
//                                 name="birthDate"
//                                 max={today}
//                                 onChange={handleChange}
//                             />
//                             {formData.age && (
//                                 <p className="age-display">
//                                     {t("signupPage.ageDisplay", { age: formData.age })}
//                                 </p>
//                             )}
//                             <select
//                                 name="autismLevel"
//                                 onChange={handleChange}
//                                 defaultValue=""
//                             >
//                                 <option value="" disabled>
//                                     {t("signupPage.signupAutismLevel")}
//                                 </option>
//                                 <option value="1">{t("signupPage.signupAutismLevel1")}</option>
//                                 <option value="2">{t("signupPage.signupAutismLevel2")}</option>
//                                 <option value="3">{t("signupPage.signupAutismLevel3")}</option>
//                             </select>
//                             <input
//                                 type="email"
//                                 name="email"
//                                 placeholder={t("signupPage.signupEmailPlaceholder")}
//                                 onChange={handleChange}
//                             />
//                             <input
//                                 type="password"
//                                 name="password"
//                                 placeholder={t("signupPage.signupPasswordPlaceholder")}
//                                 onChange={handleChange}
//                             />
//                             <button className="modern-btn signup-btn" onClick={handleSignup}>
//                                 {t("signupPage.signupBtn")}
//                             </button>
//                         </div>
//                     )}
//                 </div>
//             </div>

//             {/* Popup إدخال الاسم */}
//             {showNamePopup && (
//                 <div className="breathing-modal">
//                     <div className="modal-content">
//                         <h2>{t("signupPage.popupEnterName")}</h2>
//                         <p className="support-msg">{t("signupPage.popupSupportMsg")}</p>
//                         <input
//                             type="text"
//                             placeholder={t("signupPage.signupNamePlaceholder")}
//                             value={tempName}
//                             onChange={(e) => setTempName(e.target.value)}
//                             className="username-input"
//                         />
//                         <button className="modern-btn signup-btn" onClick={handleSaveName}>
//                             {t("signupPage.popupSaveName")}
//                         </button>
//                         <button
//                             className="close-btn"
//                             onClick={() => setShowNamePopup(false)}
//                         >
//                             {t("signupPage.popupClose")}
//                         </button>
//                     </div>
//                 </div>
//             )}
//         </div>
//     );
// }


import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useTranslation } from "react-i18next";
import "./../styles/SignupPage.css";

const API = "http://localhost:8000/api/v1/user";

export default function SignupPage({ externalStep, setUsername, darkMode }) {
  const [step, setStep] = useState("question");
  const [showBreathing, setShowBreathing] = useState(false);
  const [showNamePopup, setShowNamePopup] = useState(false);

  // Split signup fields
  const [formData, setFormData] = useState({
    firstName: "",
    lastName:  "",
    birthDate: "",
    age:       "",
    autismLevel: "",
    email:    "",
    password: ""
  });

  // Temp fields for popup
  const [tempFirst, setTempFirst] = useState("");
  const [tempLast,  setTempLast]  = useState("");

  const { t } = useTranslation();
  const navigate = useNavigate();

  useEffect(() => {
    // إذا المستخدم جاوب السؤال قبل هيك
    if (localStorage.getItem("answeredQuestion")) {
      setStep("signin");
    }
  }, []);

  useEffect(() => {
    if (externalStep && externalStep !== step) {
      setStep(externalStep);
    }
  }, [externalStep, step]);

  // حساب العمر تلقائياً
  useEffect(() => {
    if (formData.birthDate) {
      const birth = new Date(formData.birthDate);
      const today = new Date();
      let age = today.getFullYear() - birth.getFullYear();
      const m = today.getMonth() - birth.getMonth();
      if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) {
        age--;
      }
      setFormData(prev => ({ ...prev, age }));
    }
  }, [formData.birthDate]);

  const handleChange = e => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  // تسجيل الدخول
  const handleSignin = async () => {
    if (!formData.email || !formData.password) {
      alert(t("alerts.fillEmailPassword"));
      return;
    }
    const data = new URLSearchParams();
    data.append("username", formData.email);
    data.append("password", formData.password);
    data.append("grant_type", "password");

    const storedFirst = localStorage.getItem("firstName");
    const storedLast  = localStorage.getItem("lastName");
    const storedFull  = localStorage.getItem("username");

    const resp = await fetch(`${API}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: data.toString(),
    });


    const { access_token, token_type } = await resp.json();
    console.log("🏷️ login success:", { access_token, token_type });

    // **STORE** the JWT for future calls
    localStorage.setItem("token", access_token);
    
    if (storedFirst && storedLast) {
      // We have both parts already
      const full = `${storedFirst} ${storedLast}`;
      localStorage.setItem("answeredQuestion", "true");
      setUsername(full);
      navigate("/welcome");
    } else if (storedFull) {
      // Legacy full username → split
      const parts = storedFull.trim().split(" ");
      const first = parts[0];
      const last  = parts.slice(1).join(" ") || "";
      localStorage.setItem("firstName", first);
      localStorage.setItem("lastName", last);
      localStorage.setItem("answeredQuestion", "true");
      setUsername(storedFull);
      navigate("/welcome");
    } else {
      // No name at all → popup
      setShowNamePopup(true);
    }
  };

  // إنشاء حساب
  const handleSignup = () => {
    const { firstName, lastName, email, password, birthDate, autismLevel } = formData;
    if (
      !firstName.trim() ||
      !lastName.trim()  ||
      !email ||
      !password ||
      !birthDate ||
      !autismLevel
    ) {
      alert(t("alerts.fillAllFields"));
      return;
    }

    // Persist split and legacy
    localStorage.setItem("firstName", firstName);
    localStorage.setItem("lastName", lastName);
    localStorage.setItem("username", `${firstName} ${lastName}`);
    localStorage.setItem("birthDate", formData.birthDate);
    localStorage.setItem("age", formData.age);
    localStorage.setItem("autismLevel", autismLevel);
    localStorage.setItem("answeredQuestion", "true");

    setUsername(`${firstName} ${lastName}`);
    navigate("/welcome");
  };

  // حفظ الاسم من البوب أب
  const handleSaveName = () => {
    if (!tempFirst.trim() || !tempLast.trim()) {
      alert(t("signupPage.popupEnterName"));
      return;
    }
    localStorage.setItem("firstName", tempFirst);
    localStorage.setItem("lastName", tempLast);
    localStorage.setItem("username", `${tempFirst} ${tempLast}`);
    localStorage.setItem("answeredQuestion", "true");
    setUsername(`${tempFirst} ${tempLast}`);
    setShowNamePopup(false);
    navigate("/welcome");
  };

  // تحديد تاريخ اليوم كحد أقصى
  const today = new Date().toISOString().split("T")[0];

  return (
    <div className={`signup-page ${darkMode ? "dark" : ""}`}>
      <div className="page-layout">
        {/* يسار */}
        <div className="left-section">
          <motion.img
            src="/robot.png"
            alt="Robot"
            className="robot-animated-big"
            animate={{ rotate: [0, 5, -5, 0] }}
            transition={{ repeat: Infinity, duration: 3 }}
          />
          <h1 className="app-name">{t("appName")}</h1>
          <h3 className="page-title">
            {step === "signin"
              ? t("signupPage.signinTitle")
              : step === "signup"
                ? t("signupPage.signupTitle")
                : t("signupPage.questionTitle")}
          </h3>
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

        {/* يمين */}
        <div className="right-section">
          {step === "question" && (
            <motion.div
              className="form-box modern-form no-bg"
              initial={{ opacity: 0, x: 50 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="form-title">{t("signupPage.questionTitle")}</h2>
              <div className="question-buttons">
                <button
                  onClick={() => {
                    setStep("signin");
                    localStorage.setItem("answeredQuestion", "true");
                  }}
                  className="modern-btn yes-btn"
                >
                  {t("signupPage.yes")}
                </button>
                <button
                  onClick={() => {
                    setStep("signup");
                    localStorage.setItem("answeredQuestion", "true");
                  }}
                  className="modern-btn no-btn"
                >
                  {t("signupPage.no")}
                </button>
              </div>
            </motion.div>
          )}

          {step === "signin" && (
            <div className="form-box modern-form">
              <h2 className="form-title">{t("signupPage.signinTitle")}</h2>
              <input
                type="email"
                name="email"
                placeholder={t("signupPage.signinEmailPlaceholder")}
                onChange={handleChange}
              />
              <input
                type="password"
                name="password"
                placeholder={t("signupPage.signinPasswordPlaceholder")}
                onChange={handleChange}
              />
              <button className="modern-btn signin-btn" onClick={handleSignin}>
                {t("signupPage.signinBtn")}
              </button>
            </div>
          )}

          {step === "signup" && (
            <div className="form-box modern-form">
              <h2 className="form-title">{t("signupPage.signupTitle")}</h2>
              <input
                type="text"
                name="firstName"
                placeholder={t("signupPage.signupFirstNamePlaceholder") || "الاسم الأول"}
                onChange={handleChange}
              />
              <input
                type="text"
                name="lastName"
                placeholder={t("signupPage.signupLastNamePlaceholder") || "اسم العائلة"}
                onChange={handleChange}
              />
              <input
                type="date"
                name="birthDate"
                max={today}
                onChange={handleChange}
              />
              {formData.age && (
                <p className="age-display">
                  {t("signupPage.ageDisplay", { age: formData.age })}
                </p>
              )}
              <select
                name="autismLevel"
                onChange={handleChange}
                defaultValue=""
              >
                <option value="" disabled>
                  {t("signupPage.signupAutismLevel")}
                </option>
                <option value="1">{t("signupPage.signupAutismLevel1")}</option>
                <option value="2">{t("signupPage.signupAutismLevel2")}</option>
                <option value="3">{t("signupPage.signupAutismLevel3")}</option>
              </select>
              <input
                type="email"
                name="email"
                placeholder={t("signupPage.signupEmailPlaceholder")}
                onChange={handleChange}
              />
              <input
                type="password"
                name="password"
                placeholder={t("signupPage.signupPasswordPlaceholder")}
                onChange={handleChange}
              />
              <button className="modern-btn signup-btn" onClick={handleSignup}>
                {t("signupPage.signupBtn")}
              </button>
            </div>
          )}
        </div>
      </div>

      {/* Popup إدخال الاسم */}
      {showNamePopup && (
        <div className="breathing-modal">
          <div className="modal-content">
            <h2>{t("signupPage.popupEnterName")}</h2>
            <p className="support-msg">{t("signupPage.popupSupportMsg")}</p>
            <input
              type="text"
              placeholder={t("signupPage.signupFirstNamePlaceholder") || "الاسم الأول"}
              value={tempFirst}
              onChange={e => setTempFirst(e.target.value)}
              className="username-input"
            />
            <input
              type="text"
              placeholder={t("signupPage.signupLastNamePlaceholder") || "اسم العائلة"}
              value={tempLast}
              onChange={e => setTempLast(e.target.value)}
              className="username-input"
            />
            <button className="modern-btn signup-btn" onClick={handleSaveName}>
              {t("signupPage.popupSaveName")}
            </button>
            <button className="close-btn" onClick={() => setShowNamePopup(false)}>
              {t("signupPage.popupClose")}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
