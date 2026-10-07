import { useState } from "react";
import Dashboard from "./Dashboard";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);

  const handleLogin = async (event) => {
    event.preventDefault();

    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    try {
      const response = await fetch("http://127.0.0.1:8000/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Login failed");
        return;
      }

     console.log("Login successful:", data);

localStorage.setItem("access_token", data.access_token);

const drugsResponse = await fetch(
  "http://127.0.0.1:8000/drugs/",
  {
    method: "GET",
    headers: {
      Authorization: `Bearer ${data.access_token}`,
    },
  }
);

const drugsData = await drugsResponse.json();

console.log("Drugs response:", drugsData);

if (!drugsResponse.ok) {
  alert("Login worked, but accessing drugs failed.");
  return;
}

setLoggedIn(true);
    } catch (error) {
      console.error("Login error:", error);
      alert("Could not connect to the server.");
    }
  };

  if (loggedIn) {
  return <Dashboard />;
}

  return (
    <div>
      <h1>Docerejj Medical Centre</h1>
      <p>Login to your account</p>

      <form onSubmit={handleLogin}>
        <div>
          <label>Email</label>
          <br />
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            required
          />
        </div>

        <br />

        <div>
          <label>Password</label>
          <br />
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            required
          />
        </div>

        <br />

        <button type="submit">
          Login
        </button>
      </form>
    </div>
  );
}

export default App;