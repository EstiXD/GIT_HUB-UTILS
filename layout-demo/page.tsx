"use client";

import React, { useState, useRef } from "react";

export default function LayoutDemo() {
  const [menuOpen, setMenuOpen] = useState(false);
  // Anchos en px de los 3 paneles (sidebar, chat, panel derecho)
  const [widths, setWidths] = useState({
    sidebar: 320,
    chat: 600,
    panel: 350,
  });
  const dragging = useRef<{
    type: "sidebar" | "chat";
    startX: number;
    startWidths: { sidebar: number; chat: number; panel: number };
  } | null>(null); // { type: 'sidebar' | 'chat', startX, startWidths }

  // Manejador de mouse para arrastrar divisores
  const onMouseDown = (type) => (e) => {
    dragging.current = {
      type,
      startX: e.clientX,
      startWidths: { ...widths },
    };
    document.addEventListener("mousemove", onMouseMove);
    document.addEventListener("mouseup", onMouseUp);
  };

  const onMouseMove = (e) => {
    if (!dragging.current) return;
    const dx = e.clientX - dragging.current.startX;
    let newWidths = { ...dragging.current.startWidths };
    if (dragging.current.type === "sidebar") {
      // Sidebar y chat
      newWidths.sidebar = Math.max(
        20,
        dragging.current.startWidths.sidebar + dx
      );
      newWidths.chat = Math.max(20, dragging.current.startWidths.chat - dx);
    } else if (dragging.current.type === "chat") {
      // Chat y panel derecho
      newWidths.chat = Math.max(20, dragging.current.startWidths.chat + dx);
      newWidths.panel = Math.max(20, dragging.current.startWidths.panel - dx);
    }
    setWidths(newWidths);
  };

  const onMouseUp = () => {
    dragging.current = null;
    document.removeEventListener("mousemove", onMouseMove);
    document.removeEventListener("mouseup", onMouseUp);
  };

  return (
    <div className="flex min-h-screen w-full transition-all duration-300">
      {/* =====================================================
          Columna 1 - Barra lateral de iconos
      ====================================================== */}
      <div
        id="opciones"
        className="bg-gray-900 flex flex-col justify-between items-start py-4 pl-2"
      >
        <div className="flex flex-col gap-1">
          {/* Menú hamburguesa (arriba) */}
          <div
            onClick={() => setMenuOpen(!menuOpen)}
            className="w-8 h-8 flex flex-col justify-between cursor-pointer"
          >
            <span className="block h-1 bg-white rounded"></span>
            <span className="block h-1 bg-white rounded"></span>
            <span className="block h-1 bg-white rounded"></span>
          </div>

          {/* Íconos debajo del menú */}
          <div className="flex flex-col gap-4 mt-4">
            <div className="w-8 h-8 bg-gray-700 rounded"></div>
            <div className="w-8 h-8 bg-gray-700 rounded"></div>
            <div className="w-8 h-8 bg-gray-700 rounded"></div>
          </div>
        </div>

        {/* Bolita verde (abajo) */}
        <div className="w-10 h-10 rounded-full bg-green-500"></div>
      </div>

      {/* =====================================================
          Columna 2 - Sidebar de chats (resizable con splitter)
      ====================================================== */}
      <div
        style={{ width: widths.sidebar }}
        className="overflow-auto min-w-[0px] max-w-full transition-all duration-100"
      >
        <div
          id="sidebar"
          className="bg-gray-800 flex flex-col relative z-0 h-full "
        >
          <div className="p-4 border-b border-gray-700 text-white font-bold">
            WhatsApp
          </div>
          <div className="p-2">
            <input
              type="text"
              placeholder="Buscar o iniciar chat nuevo"
              className="w-full rounded-lg p-2 text-sm bg-gray-700 text-white placeholder-gray-400"
            />
          </div>
          <div className="flex justify-around text-gray-400 text-sm border-b border-gray-700">
            <button className="p-2 hover:text-white">Todos</button>
            <button className="p-2 hover:text-white">No leídos</button>
            <button className="p-2 hover:text-white">Favoritos</button>
            <button className="p-2 hover:text-white">Grupos</button>
          </div>
          <div className="flex-1 overflow-y-auto">
            <div className="p-3 hover:bg-gray-700 cursor-pointer text-white border-b border-gray-700">
              <span className="font-semibold">Deisy</span>
              <p className="text-sm text-gray-400">
                Hola Deisy buenas noches...
              </p>
            </div>
            <div className="p-3 hover:bg-gray-700 cursor-pointer text-white border-b border-gray-700">
              <span className="font-semibold">Kevin Rincon</span>
              <p className="text-sm text-gray-400">¿Cómo has estado?</p>
            </div>
            <div className="p-3 hover:bg-gray-700 cursor-pointer text-white border-b border-gray-700">
              <span className="font-semibold">Guiovani Andrés</span>
              <p className="text-sm text-gray-400">😊</p>
            </div>
          </div>
        </div>
      </div>
      {/* Splitter entre sidebar y chat */}
      <div
        onMouseDown={onMouseDown("sidebar")}
        className="cursor-col-resize w-2 bg-gray-700 hover:bg-green-600 transition-colors duration-100 z-10"
        style={{ userSelect: "none" }}
        title="Ajustar ancho"
      />

      {/* =====================================================
          Columna 3 - Área del chat (resizable con splitter)
      ====================================================== */}
      <div
        style={{ width: widths.chat }}
        className="overflow-auto min-w-[0px] max-w-full transition-all duration-100"
      >
        <div
          id="contenido1"
          className="bg-gray-900 flex flex-col h-full w-full"
          style={{ height: "100vh", minHeight: 0 }}
        >
          <div className="p-4 border-b border-gray-700 text-white flex justify-between">
            <span>Deisy</span>
            <div className="flex gap-3">
              <div className="w-6 h-6 bg-gray-600 rounded"></div>
              <div className="w-6 h-6 bg-gray-600 rounded"></div>
            </div>
          </div>
          <div className="flex-1 p-4 text-white overflow-y-auto min-h-0">
            <div className="bg-green-600 p-2 rounded-lg mb-2 w-fit">
              Hola Deisy buenas noches 🌙
            </div>
            <div className="bg-gray-700 p-2 rounded-lg mb-2 w-fit ml-auto">
              Hola! ¿Cómo estás?
            </div>
          </div>
          <div className="p-4 border-t border-gray-700 flex gap-2 sticky bottom-0 bg-gray-900 z-20">
            <input
              type="text"
              placeholder="Escribe un mensaje"
              className="flex-1 rounded-lg p-2 text-sm bg-gray-700 text-white placeholder-gray-400"
            />
            <button className="px-4 py-2 bg-green-600 rounded-lg text-white">
              Enviar
            </button>
          </div>
        </div>
      </div>
      {/* Splitter entre chat y panel derecho */}
      <div
        onMouseDown={onMouseDown("chat")}
        className="cursor-col-resize w-2 bg-gray-700 hover:bg-green-600 transition-colors duration-100 z-10"
        style={{ userSelect: "none" }}
        title="Ajustar ancho"
      />

      {/* =====================================================
          Columna 4 - Panel derecho (resizable con splitter)
      ====================================================== */}
      <div className="overflow-auto min-w-[0px] max-w-full transition-all duration-100">
        <div
          id="contenido2"
          className="bg-gray-950 flex flex-col items-center justify-center text-center text-white p-8 h-full w-full "
        >
          <div className="bg-gray-800 rounded-lg p-6 shadow-lg">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg"
              alt="WhatsApp"
              className="w-16 h-16 mx-auto mb-4"
            />
            <h2 className="text-2xl font-bold mb-2">
              Descarga WhatsApp para Windows
            </h2>
            <p className="text-gray-400 mb-4">
              Descarga la aplicación para Windows y haz llamadas, comparte
              pantalla y disfruta de una experiencia más rápida.
            </p>
            <button className="px-6 py-2 bg-green-600 rounded-lg text-white">
              Descargar
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-4">
            Tus mensajes personales están cifrados de extremo a extremo.
          </p>
        </div>
      </div>
    </div>
  );
}
