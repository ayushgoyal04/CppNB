
"use client";
import Notebook from "@/components/Notebook";
import Toolbar from "@/components/Toolbar";

export default function HomePage() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-bold mb-6">CppNB</h1>
      <Toolbar onRunSelected={function (): void {
        throw new Error("Function not implemented.");
      }} onNew={function (): void {
        throw new Error("Function not implemented.");
      }} onSave={function (): void {
        throw new Error("Function not implemented.");
      }} onUpload={function (): void {
        throw new Error("Function not implemented.");
      }} onDownload={function (): void {
        throw new Error("Function not implemented.");
      }} />
      <Notebook />
    </div>
  );
}
