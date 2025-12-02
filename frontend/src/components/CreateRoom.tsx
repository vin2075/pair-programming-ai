// frontend/src/components/CreateRoom.tsx
import React from "react";
import { createRoom } from "../api/rooms";

const CreateRoom: React.FC = () => {
  const handleCreate = async () => {
    const roomId = await createRoom();
    window.location.href = `/room/${roomId}`;
  };

  return (
    <div style={{ padding: 24 }}>
      <h1>Pair Coding</h1>
      <p>Create or join a room for live pair programming.</p>
      <button onClick={handleCreate}>Create New Room</button>
    </div>
  );
};

export default CreateRoom;
