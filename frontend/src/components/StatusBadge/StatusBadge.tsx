interface StatusBadgeProps {
  text: string;
  color: string;
}

export function StatusBadge({ text, color }: StatusBadgeProps) {
  return (
    <span
      style={{
        display: "inline-block",
        padding: "2px 10px",
        borderRadius: 999,
        background: color + "22",
        color,
        fontSize: 12,
        fontWeight: 600,
        border: `1px solid ${color}44`,
      }}
    >
      {text}
    </span>
  );
}
