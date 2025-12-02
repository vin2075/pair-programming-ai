import React, { useEffect, useRef, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import CodeEditor from "./CodeEditor";
import { getRoom } from "../api/rooms";
import { useDispatch, useSelector } from "react-redux";
import { setCode, setRoomId, setSuggestion } from "../store/roomSlice";
import { RootState } from "../store";
import { fetchSuggestion } from "../api/autocomplete";


const WS_BASE = (process.env.REACT_APP_WS_URL || "ws://localhost:8000").replace(/\/$/, "");

function useDebounced<T extends (...args: any[]) => any>(fn: T, ms = 600) {
  const t = useRef<number | null>(null);
  return useCallback((...args: Parameters<T>) => {
    if (t.current) window.clearTimeout(t.current);
    // @ts-ignore
    t.current = window.setTimeout(() => fn(...args), ms);
  }, [fn, ms]);
}

const RoomPage: React.FC = () => {
  const { roomId } = useParams<{ roomId: string }>();
  const dispatch = useDispatch();
  const code = useSelector((s: RootState) => s.room.code);
  const suggestion = useSelector((s: RootState) => s.room.suggestion);
  const [ws, setWs] = useState<WebSocket | null>(null);
  const cursorPos = useRef<{ line: number; ch: number }>({ line: 0, ch: 0 });

  useEffect(() => {
    if (!roomId) return;
    dispatch(setRoomId(roomId));
    getRoom(roomId).then((r) => {
      dispatch(setCode(r.last_code || ""));
    });

    const socket = new WebSocket(`${WS_BASE}/ws/${roomId}`);
    socket.onmessage = (ev) => {
      try {
        const payload = JSON.parse(ev.data);
        if (payload.type === "initial" || payload.type === "code_update") {
          dispatch(setCode(payload.code || ""));
        }
      } catch {}
    };
    setWs(socket);

    return () => socket.close();
  }, [roomId, dispatch]);

  const sendCodeUpdate = useDebounced((nextCode: string) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    ws.send(JSON.stringify({ type: "code_update", code: nextCode }));
  }, 200);

  const callAutocomplete = useDebounced(async (codeText: string) => {
    try {
      const cursorFlat = getFlatCursorPosition(codeText, cursorPos.current);
      const s = await fetchSuggestion(codeText, cursorFlat);
      dispatch(setSuggestion(s));
    } catch {
      dispatch(setSuggestion(""));
    }
  }, 600);

  const handleCodeChange = (value: string) => {
    dispatch(setCode(value));
    sendCodeUpdate(value);
    callAutocomplete(value);
  };

  const handleCursorActivity = (pos: { line: number; ch: number }) =>
    (cursorPos.current = pos);

  return (
    <div style={{ height: "100vh", display: "flex", flexDirection: "column" }}>
  <div style={{ padding: 8, background: "#222", color: "#fff" }}>
    <strong>Room: </strong> {roomId}
  </div>

  <div style={{ flex: 1, display: "flex", height: "100%", overflow: "hidden" }}>
    
    {/* LEFT SIDE FULL HEIGHT EDITOR */}
    <div style={{ flex: 1, height: "100%", overflow: "hidden" }}>
      <CodeEditor
        value={code}
        onChange={handleCodeChange}
        onCursorActivity={handleCursorActivity}
      />
    </div>

    {/* RIGHT SIDE AI PANEL */}
    <div style={{ width: 320, borderLeft: "1px solid #eee", padding: 8, overflowY: "auto" }}>
      <h4>AI Suggestion</h4>
      <pre style={{ whiteSpace: "pre-wrap" }}>{suggestion}</pre>
    </div>

  </div>
</div>
  );
};

function getFlatCursorPosition(text: string, cursor: { line: number; ch: number }) {
  const lines = text.split("\n");
  let pos = 0;
  for (let i = 0; i < cursor.line; i++) pos += (lines[i] || "").length + 1;
  return pos + cursor.ch;
}

export default RoomPage;
