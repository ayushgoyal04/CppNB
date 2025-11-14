"use client";
import { useState } from "react";
import Editor from "@monaco-editor/react";

type CellProps = {
    id: string | number;
    code: string;
    onChange: (id: string | number, value: string) => void;
    onRun: (id: string | number) => void;
    onAdd: (id: string | number) => void;
    onDelete: (id: string | number) => void;
};

export default function Cell({ id, code, onChange, onRun, onAdd, onDelete }: CellProps) {
    const [checked, setChecked] = useState(false);

    return (
        <div className="border rounded-2xl p-4 my-4 shadow-sm bg-white">
            <div className="flex items-center justify-between mb-2">
                <input
                    type="checkbox"
                    checked={checked}
                    onChange={() => setChecked(!checked)}
                />
                <div className="flex gap-2">
                    <button
                        onClick={() => onRun(id)}
                        className="px-3 py-1 rounded bg-green-500 text-white"
                    >
                        Run
                    </button>
                    <button
                        onClick={() => onAdd(id)}
                        className="px-3 py-1 rounded bg-blue-500 text-white"
                    >
                        + Add
                    </button>
                    <button
                        onClick={() => onDelete(id)}
                        className="px-3 py-1 rounded bg-red-500 text-white"
                    >
                        Delete
                    </button>
                </div>
            </div>

            <Editor
                height="200px"
                defaultLanguage="cpp"
                value={code}
                onChange={(value) => onChange(id, value || "")}
            />

            <div className="mt-2 p-2 bg-gray-100 rounded">
                <p className="text-sm text-gray-700">Output will show here...</p>
            </div>
        </div>
    );
}
