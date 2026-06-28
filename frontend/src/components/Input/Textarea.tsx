import type { TextareaHTMLAttributes } from "react";

interface TextareaProps extends Omit<TextareaHTMLAttributes<HTMLTextAreaElement>, "onChange"> {
  value: string;
  onChange: (value: string) => void;
}

export function Textarea({ value, onChange, placeholder, rows = 3, ...rest }: TextareaProps) {
  return (
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      rows={rows}
      style={{
        width: "100%",
        background: "#0f172a",
        border: "1px solid #334155",
        borderRadius: 10,
        color: "#e2e8f0",
        padding: "10px 14px",
        fontSize: 14,
        fontFamily: "inherit",
        resize: "vertical",
        outline: "none",
        boxSizing: "border-box",
        lineHeight: 1.6,
      }}
      {...rest}
    />
  );
}
