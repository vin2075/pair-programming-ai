// frontend/src/api/rooms.ts
import axios from "axios";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const createRoom = async () => {
  const res = await axios.post(`${API}/rooms`);
  return res.data.roomId;
};

export const getRoom = async (roomId: string) => {
  const res = await axios.get(`${API}/rooms/${roomId}`);
  return res.data;
};
