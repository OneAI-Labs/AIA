import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { FaPaperPlane, FaArrowLeft } from "react-icons/fa";
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";

const API_URL = "http://34.56.213.136:5000"; // ✅ Backend API URL

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [showChat, setShowChat] = useState(false);
  const [welcomeText, setWelcomeText] = useState("");
  const [promptText, setPromptText] = useState("");
  const messagesEndRef = useRef(null);
  const navigate = useNavigate();

  const fullText = "Welcome to the future of AI";
  const promptFullText = "Press enter to begin";

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

  useEffect(() => {
    fetchChatHistory();
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const fetchChatHistory = async () => {
    try {
      const response = await axios.get(`${API_URL}/chat-history`);
      setMessages(response.data.history || []);
    } catch (error) {
      console.error("Error fetching chat history:", error);
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInput("");

    try {
      const response = await axios.post(`${API_URL}/chat`, { message: input });
      const aiMessage = { sender: "ai", text: response.data.reply };
      setMessages((prevMessages) => [...prevMessages, aiMessage]);
    } catch (error) {
      console.error("Error fetching AI response:", error);
      const errorMessage = { sender: "ai", text: "⚠️ Unable to reach AI server. Please try again later." };
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
        <button
          className="absolute top-5 right-5 bg-blue-500 text-white px-4 py-2 rounded"
          onClick={() => navigate("/login")}
        >
          Login
        </button>
        <div className="absolute bottom-5 text-gray-500 text-xs">Developed by OneAI</div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen bg-black w-full px-4 py-6">
      <button onClick={() => setShowChat(false)} className="absolute top-5 left-5 text-white text-lg">
        <FaArrowLeft />
      </button>
      <button
        className="absolute top-5 right-5 bg-blue-500 text-white px-4 py-2 rounded"
        onClick={() => navigate("/login")}
      >
        Login
      </button>
      <div className="flex flex-col flex-1 overflow-y-auto space-y-4 pb-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-3 max-w-xs rounded-lg text-white ${msg.sender === "user" ? "bg-blue-500 self-end text-right" : "bg-gray-700 self-start text-left"}`}
          >
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="flex items-center border-t border-gray-700 p-4">
        <input
          type="text"
          className="flex-1 bg-gray-800 text-white p-2 rounded-l-lg outline-none"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={sendMessage} className="bg-blue-500 text-white p-2 rounded-r-lg">
          <FaPaperPlane />
        </button>
      </div>
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/login" element={<div className="flex items-center justify-center h-screen text-white">Login Page</div>} />
      </Routes>
    </Router>
  );
};

export default App;

