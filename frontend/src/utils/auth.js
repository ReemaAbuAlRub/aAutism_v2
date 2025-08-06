export function saveUserData(user) {
    localStorage.setItem("userData", JSON.stringify(user));
}

export function getUserData() {
    const data = localStorage.getItem("userData");
    return data ? JSON.parse(data) : null;
}
