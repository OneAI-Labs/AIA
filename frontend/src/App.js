import React, { useState, useEffect } from "react";
import axios from "axios";
import { FaPaperPlane, FaArrowLeft } from "react-icons/fa";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [showChat, setShowChat] = useState(false);
  const [welcomeText, setWelcomeText] = useState("");
  const [promptText, setPromptText] = useState("");

  const fullText = "Welcome to the future of AI";
  const promptFullText = "Press enter to begin";
  const API_URL = "http://34.56.213.136:5000/chat"; // ✅ Updated API URL

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setWelcomeText(fullText.slice(0, i));
      i++;
      if (i > fullText.length) {
        clearInterval(interval);
        setTimeout(() => {
          let j = 0;
          const promptInterval = setInterval(() => {
            setPromptText(promptFullText.slice(0, j));
            j++;
            if (j > promptFullText.length) clearInterval(promptInterval);
          }, 100);
        }, 1000);
      }
    }, 100);
    return () => clearInterval(interval);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");

    try {
      const response = await axios.post(API_URL, { message: input });
      const aiMessage = { sender: "ai", text: response.data.reply };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error("Error:", error);
      const errorMessage = {
        sender: "ai",
        text: "⚠️ Unable to reach AI server. Please try again later.",
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      if (!showChat) {
        setShowChat(true);
      } else {
        sendMessage();
      }
    }
  };

  if (!showChat) {
    return (
      <div
        className="flex flex-col h-screen bg-black items-center justify-center relative w-full text-center"
        onKeyDown={handleKeyDown}
        tabIndex={0}
      >
        <div className="text-blue-400 text-5xl mb-4 font-bold">AI-A</div>
        <div className="bg-gradient-to-b from-blue-400 to-black w-60 h-60 rounded-full shadow-lg mb-4"></div>
        <div className="text-white text-lg">{welcomeText}</div>
        <div className="text-gray-400 text-sm mt-2">{promptText}</div>
        <div className="absolute bottom-5 text-gray-500 text-xs">
          Developed by OneAI
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-black items-center justify-center relative w-full">
      <button onClick={() => setShowChat(false)} className="absolute top-5 left-5 text-white text-lg">
        <FaArrowLeft />
      </button>
      <div className="bg-gradient-to-b from-blue-400 to-black w-40 h-40 rounded-full shadow-lg mb-10"></div>

      <div className="absolute top-24 w-full max-w-2xl px-4 space-y-2 overflow-y-auto max-h-80 flex flex-col items-end">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 max-w-xs rounded-lg text-white mb-2 ${
              msg.sender === "user" ? "bg-blue-500 self-end text-right" : "bg-gray-700 self-start text-left"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="absolute bottom-10 w-full px-4 flex justify-center">
        <div className="flex w-full max-w-2xl border border-gray-400 rounded-lg p-3 bg-gray-900 shadow-lg">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1 p-2 border-none outline-none bg-transparent text-white"
            placeholder="Type a message..."
          />
          <button
            onClick={sendMessage}
            className="ml-2 p-2 rounded-full bg-gray-700 text-white hover:bg-gray-800 transition"
          >
            <FaPaperPlane />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
