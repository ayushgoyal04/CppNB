
"use client"

import React, { useRef, useState } from "react";

export default function UploadPage() {
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [message, setMessage] = useState("");

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file && file.name.endsWith(".cppnb")) {
            setSelectedFile(file);
            setMessage("");
        } else {
            setSelectedFile(null);
            setMessage("Please select a valid .cppnb file.");
        }
    };

    const handleUpload = () => {
        if (!selectedFile) {
            setMessage("No file selected.");
            return;
        }
        // TODO: Implement actual upload logic here
        setMessage(`File '${selectedFile.name}' ready for upload.`);
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-purple-500 via-pink-400 to-yellow-300 animate-fade-in">
            <div className="bg-white bg-opacity-80 rounded-2xl shadow-2xl p-10 flex flex-col items-center w-full max-w-md border-2 border-purple-300 animate-pop-in">
                <h1 className="text-3xl font-extrabold mb-6 text-transparent bg-clip-text bg-gradient-to-r from-purple-600 via-pink-500 to-yellow-500 animate-gradient">Upload your <span className="underline decoration-pink-400">.cppnb</span> file</h1>
                <input
                    type="file"
                    accept=".cppnb"
                    ref={fileInputRef}
                    onChange={handleFileChange}
                    className="mb-6 border-2 border-pink-400 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition-all duration-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-gradient-to-r file:from-purple-400 file:to-pink-300 file:text-white hover:file:bg-gradient-to-r hover:file:from-pink-400 hover:file:to-yellow-300"
                />
                <button
                    onClick={handleUpload}
                    className="bg-gradient-to-r from-purple-500 via-pink-400 to-yellow-300 text-white px-6 py-3 rounded-xl font-bold shadow-lg hover:scale-105 hover:shadow-2xl transition-transform duration-300 animate-bounce"
                >
                    <span className="inline-block mr-2 animate-wiggle">🚀</span> Upload
                </button>
                {message && (
                    <p className="mt-6 text-pink-600 text-lg animate-fade-in">{message}</p>
                )}
            </div>
            <style jsx>{`
                @keyframes fade-in {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
                @keyframes pop-in {
                    0% { transform: scale(0.8); opacity: 0; }
                    80% { transform: scale(1.05); opacity: 1; }
                    100% { transform: scale(1); }
                }
                @keyframes gradient {
                    0% { background-position: 0% 50%; }
                    100% { background-position: 100% 50%; }
                }
                @keyframes bounce {
                    0%, 100% { transform: translateY(0); }
                    50% { transform: translateY(-8px); }
                }
                @keyframes wiggle {
                    0%, 100% { transform: rotate(-10deg); }
                    50% { transform: rotate(10deg); }
                }
                .animate-fade-in {
                    animation: fade-in 1s ease;
                }
                .animate-pop-in {
                    animation: pop-in 0.7s cubic-bezier(.68,-0.55,.27,1.55);
                }
                .animate-gradient {
                    background-size: 200% 200%;
                    animation: gradient 3s linear infinite alternate;
                }
                .animate-bounce {
                    animation: bounce 1.2s infinite;
                }
                .animate-wiggle {
                    animation: wiggle 1.2s infinite;
                }
            `}</style>
        </div>
    );
}
