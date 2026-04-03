"use client";

import { useCallback, useRef, useState } from "react";

interface UploadProps {
  loading: boolean;
  onUpload: (file: File) => void;
}

export default function Upload({ loading, onUpload }: UploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFile = useCallback(
    (file: File | undefined) => {
      if (!file) return;
      if (
        !file.name.endsWith(".docx") &&
        !file.name.endsWith(".doc")
      ) {
        alert("Akceptowane sa tylko pliki .docx i .doc");
        return;
      }
      onUpload(file);
    },
    [onUpload]
  );

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDragOver(false);
      handleFile(e.dataTransfer.files[0]);
    },
    [handleFile]
  );

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center rounded-lg border-2 border-dashed border-blue-300 bg-blue-50 p-12">
        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-600 mb-4" />
        <p className="text-blue-700 font-medium">Analizuje dokument...</p>
        <p className="text-blue-500 text-sm mt-1">
          To moze potrwac kilka sekund
        </p>
      </div>
    );
  }

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragOver(true);
      }}
      onDragLeave={() => setDragOver(false)}
      onDrop={handleDrop}
      className={`flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 cursor-pointer transition-colors ${
        dragOver
          ? "border-blue-500 bg-blue-50"
          : "border-gray-300 bg-gray-50 hover:border-gray-400"
      }`}
      onClick={() => inputRef.current?.click()}
    >
      <svg
        className="w-12 h-12 text-gray-400 mb-3"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={1.5}
          d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
        />
      </svg>
      <p className="text-gray-600 font-medium">
        Przeciagnij plik DOC/DOCX lub kliknij
      </p>
      <p className="text-gray-400 text-sm mt-1">
        Formularz przetargowy (.doc, .docx)
      </p>
      <input
        ref={inputRef}
        type="file"
        accept=".docx,.doc,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword"
        className="hidden"
        onChange={(e) => handleFile(e.target.files?.[0])}
      />
    </div>
  );
}
