
import React from "react";
import ReactDOM from "react-dom/client";
import Login from "./pages/Login";
import Profile from "./pages/Profile";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <>
      <Login />
      <Profile />
    </>
  </React.StrictMode>
);
