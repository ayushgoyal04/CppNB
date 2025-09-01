"use client";
import { useState } from "react";
import Cell from "./Cell";

export default function Notebook() {
    const [cells, setCells] = useState([
        { id: 1, code: "// Write your C++ code here" }
    ]);

    const handleCodeChange = (id: string | number, value: string) => {
        setCells(cells.map(c => c.id === id ? { ...c, code: value } : c));
    };

    const handleRun = (id: string | number) => {
        console.log("Run cell:", id);
        // TODO: send code to FastAPI backend
    };

    const handleAdd = (id: string | number) => {
        const newId = cells.length > 0 ? Math.max(...cells.map(c => Number(c.id))) + 1 : 1;
        setCells([
            ...cells,
            { id: newId, code: "// New cell" }
        ]);
    };

    const handleDelete = (id: string | number) => {
        setCells(cells.filter(c => c.id !== id));
    };

    return (
        <div>
            {cells.map(cell => (
                <Cell
                    key={cell.id}
                    id={cell.id}
                    code={cell.code}
                    onChange={handleCodeChange}
                    onRun={handleRun}
                    onAdd={handleAdd}
                    onDelete={handleDelete}
                />
            ))}
        </div>
    );
}
