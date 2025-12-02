// frontend/src/api/autocomplete.ts
import axios from "axios";

const API = process.env.REACT_APP_API_URL || "http://localhost:8000";

export const fetchSuggestion = async (code: string, cursorPosition: number) => {
  const res = await axios.post(`${API}/autocomplete`, {
    code,
    cursorPosition,
    language: "python",
  });
  return res.data.suggestion as string;
};
