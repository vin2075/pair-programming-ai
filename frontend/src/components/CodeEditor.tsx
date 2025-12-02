//CodeEditor.tsx
import React from "react";
import { Controlled as ControlledEditor } from "react-codemirror2";
import "codemirror/lib/codemirror.css";
import "codemirror/theme/dracula.css";
import "codemirror/mode/python/python";
import "codemirror/addon/edit/closebrackets";
import "codemirror/addon/edit/closetag";

interface Props {
  value: string;
  onChange: (value: string) => void;
  onCursorActivity?: (pos: { line: number; ch: number }) => void;
}

const CodeEditor: React.FC<Props> = ({ value, onChange, onCursorActivity }) => {
  return (
    <div className="code-editor-wrapper">
      <ControlledEditor
        value={value}
        options={{
          lineNumbers: true,
          mode: "python",
          theme: "dracula",
          lineWrapping: true,
          autoCloseBrackets: true,
        }}
        onBeforeChange={(_editor, _data, val) => onChange(val)}
        onCursorActivity={(editor) => {
          const cursor = editor.getCursor();
          onCursorActivity && onCursorActivity(cursor);
        }}
      />
    </div>
  );
};

export default CodeEditor;
