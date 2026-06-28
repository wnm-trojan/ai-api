import { useState } from "react";
import { ChatPanel } from "../features/chat";
import { StreamPanel } from "../features/stream";
import { JSONPanel } from "../features/json-mode";
import { FunctionPanel } from "../features/function-call";
import { MainLayout } from "../layouts/MainLayout";

export default function App() {
  const [tab, setTab] = useState("chat");

  return (
    <MainLayout activeTab={tab} onTabChange={setTab}>
      {tab === "chat" && <ChatPanel />}
      {tab === "stream" && <StreamPanel />}
      {tab === "json" && <JSONPanel />}
      {tab === "function" && <FunctionPanel />}
    </MainLayout>
  );
}
