"use client";

"use client";

type ToolbarProps = {
    onRunSelected: () => void;
    onNew: () => void;
    onSave: () => void;
    onUpload: () => void;
    onDownload: () => void;
};

export default function Toolbar({
    onRunSelected,
    onNew,
    onSave,
    onUpload,
    onDownload,
}: ToolbarProps) {
    return (
        <div className="flex gap-2 p-2 bg-gray-50 border-b mb-4">
            <button
                onClick={onRunSelected}
                className="px-3 py-1 bg-green-500 text-white rounded"
            >
                Run Selected
            </button>
            <button
                onClick={onNew}
                className="px-3 py-1 bg-blue-500 text-white rounded"
            >
                New
            </button>
            <button
                onClick={onSave}
                className="px-3 py-1 bg-gray-700 text-white rounded"
            >
                Save
            </button>
            <button
                onClick={onUpload}
                className="px-3 py-1 bg-purple-500 text-white rounded"
            >
                Upload
            </button>
            <button
                onClick={onDownload}
                className="px-3 py-1 bg-orange-500 text-white rounded"
            >
                Download
            </button>
        </div>
    );
}
