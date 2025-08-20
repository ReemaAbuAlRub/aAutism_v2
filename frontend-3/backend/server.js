// server.js
const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const app = express();
const PORT = 3000; // ✅ تم تغيير البورت ليتطابق مع الواجهة

// Middleware
app.use(cors());
app.use(bodyParser.json());

// قاعدة بيانات وهمية (مؤقتة داخل الذاكرة)
const users = [];

// ✅ Endpoint إنشاء حساب (Signup)
app.post("/api/v1/user/register", (req, res) => {
    const { name, birthDate, age, autismLevel, email, password } = req.body;
    const existingUser = users.find((user) => user.email === email);

    if (existingUser) {
        return res.status(400).json({ message: "البريد الإلكتروني مستخدم مسبقًا." });
    }

    const newUser = { name, birthDate, age, autismLevel, email, password };
    users.push(newUser);
    return res.status(201).json({ message: "تم إنشاء الحساب بنجاح", name });
});

// ✅ Endpoint تسجيل الدخول (Login)
app.post("/api/v1/user/login", (req, res) => {
    const { email, password } = req.body;
    const user = users.find((u) => u.email === email && u.password === password);

    if (!user) {
        return res.status(401).json({ message: "البريد الإلكتروني أو كلمة المرور خاطئة." });
    }

    return res.status(200).json({ message: "تم تسجيل الدخول بنجاح", name: user.name });
});

// ✅ تشغيل الخادم
app.listen(PORT, () => {
    console.log(`✅ السيرفر شغّال على http://localhost:${PORT}`);
});
