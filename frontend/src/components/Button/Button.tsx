import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Loader } from "@/components/Loader/Loader";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  loading?: boolean;
  color?: string;
  children: ReactNode;
}

export function Button({
  onClick,
  disabled,
  loading = false,
  children,
  color = "#6366f1",
  ...rest
}: ButtonProps) {
  const isDisabled = disabled || loading;

  return (
    <button
      onClick={onClick}
      disabled={isDisabled}
      style={{
        background: isDisabled ? "#334155" : color,
        color: isDisabled ? "#64748b" : "#fff",
        border: "none",
        borderRadius: 10,
        padding: "10px 22px",
        fontWeight: 600,
        fontSize: 14,
        cursor: isDisabled ? "not-allowed" : "pointer",
        transition: "all .2s",
        display: "flex",
        alignItems: "center",
        gap: 8,
      }}
      {...rest}
    >
      {loading && <Loader size={14} />}
      {children}
    </button>
  );
}
