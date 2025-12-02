// frontend/src/App.tsx
import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import CreateRoom from "./components/CreateRoom";
import RoomPage from "./components/RoomPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CreateRoom />} />
        <Route path="/room/:roomId" element={<RoomPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
