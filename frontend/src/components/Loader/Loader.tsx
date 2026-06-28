interface LoaderProps {
  size?: number;
}

export function Loader({ size = 14 }: LoaderProps) {
  return (
    <span
      style={{
        width: size,
        height: size,
        border: "2px solid #ffffff44",
        borderTopColor: "#fff",
        borderRadius: "50%",
        animation: "spin 0.7s linear infinite",
        display: "inline-block",
      }}
    />
  );
}
