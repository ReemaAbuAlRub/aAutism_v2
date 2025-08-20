import { ME_URL } from "../config/api";

export function deriveDisplayName(profile) {
  const { username, first_name, last_name, full_name, email, name } = profile || {};
  const display =
    full_name ||
    name ||
    username ||
    [first_name, last_name].filter(Boolean).join(" ") ||
    (email ? email.split("@")[0] : "");
  return display || "User";
}

export async function fetchMe(token) {
  const res = await fetch(ME_URL, {
    method: "GET",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || res.statusText);
  }
  return res.json();
}

export async function afterAuthNavigate({ token, setUsername, navigate }) {
  // WHY: centralize post-login/signup flow; avoids divergence between pages.
  if (!token) throw new Error("Missing token after login/signup");
  const me = await fetchMe(token);
  const displayName = deriveDisplayName(me);
  setUsername(displayName);
  localStorage.setItem("answeredQuestion", "true");
  navigate("/welcome");
}
