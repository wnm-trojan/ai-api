interface ErrorBoxProps {
  msg: string;
}

export function ErrorBox({ msg }: ErrorBoxProps) {
  if (!msg) return null;

  return (
    <div
      style={{
        background: "#450a0a",
        border: "1px solid #7f1d1d",
        borderRadius: 10,
        padding: "10px 14px",
        color: "#fca5a5",
        fontSize: 13,
      }}
    >
      ⚠️ {msg}
    </div>
  );
}
