// frontend/src/store/roomSlice.ts
import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface RoomState {
  roomId: string | null;
  code: string;
  suggestion: string;
}

const initialState: RoomState = {
  roomId: null,
  code: "",
  suggestion: "",
};

const roomSlice = createSlice({
  name: "room",
  initialState,
  reducers: {
    setRoomId(state, action: PayloadAction<string>) {
      state.roomId = action.payload;
    },
    setCode(state, action: PayloadAction<string>) {
      state.code = action.payload;
    },
    setSuggestion(state, action: PayloadAction<string>) {
      state.suggestion = action.payload;
    },
  },
});

export const { setRoomId, setCode, setSuggestion } = roomSlice.actions;
export default roomSlice.reducer;
