'use client';

import { useState, useRef, useEffect, FormEvent } from 'react';
import { parseMessage, generateResponse, getQuickActions, ParsedMessage } from '@/lib/chatbot-parser';
import { Card, CardHeader, CardTitle, CardContent, Button, Input } from './ui';

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatInterfaceProps {
  onDrinkAdded?: (drink: ParsedMessage['drinks'][0]) => void;
  onFoodAdded?: (food: ParsedMessage['foods'][0]) => void;
}

export function ChatInterface({ onDrinkAdded, onFoodAdded }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 'welcome',
      text: "Hi! I'm here to help track your drinks and food. Tell me what you're having, like '2 beers at 7pm' or 'had pizza for dinner'. You can also use the quick buttons below!",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const addMessage = (text: string, sender: 'user' | 'bot') => {
    const message: Message = {
      id: `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      text,
      sender,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, message]);
    return message;
  };

  const handleParsedMessage = (parsed: ParsedMessage) => {
    // Handle drinks
    for (const drink of parsed.drinks) {
      onDrinkAdded?.(drink);
    }

    // Handle foods
    for (const food of parsed.foods) {
      onFoodAdded?.(food);
    }

    // Generate and show response
    const response = generateResponse(parsed);
    setTimeout(() => {
      setIsTyping(false);
      addMessage(response, 'bot');
    }, 500);
  };

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userText = inputValue.trim();
    setInputValue('');

    // Add user message
    addMessage(userText, 'user');

    // Show typing indicator
    setIsTyping(true);

    // Parse the message
    const parsed = parseMessage(userText);
    handleParsedMessage(parsed);
  };

  const handleQuickAction = (action: ReturnType<typeof getQuickActions>[0]) => {
    const parsed = action.action();

    // Add a message showing what was added
    if (parsed.drinks.length > 0) {
      addMessage(`${action.emoji} ${action.label}`, 'user');
    } else if (parsed.foods.length > 0) {
      addMessage(`${action.emoji} ${action.label}`, 'user');
    }

    setIsTyping(true);
    handleParsedMessage(parsed);
  };

  const quickActions = getQuickActions();

  return (
    <Card className="flex flex-col h-[500px]">
      <CardHeader className="border-b border-neutral-200">
        <CardTitle>Chat</CardTitle>
        <p className="text-sm text-neutral-600">Tell me about your drinks and food</p>
      </CardHeader>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map(message => (
          <ChatMessage key={message.id} message={message} />
        ))}
        {isTyping && <TypingIndicator />}
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Actions */}
      <div className="px-4 py-2 border-t border-neutral-200 flex gap-2 flex-wrap">
        {quickActions.map(action => (
          <button
            key={action.label}
            onClick={() => handleQuickAction(action)}
            className="quick-action"
          >
            <span>{action.emoji}</span>
            <span>{action.label}</span>
          </button>
        ))}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-neutral-200">
        <div className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="e.g., '2 beers at 8pm' or 'ate pizza'"
            className="flex-1"
          />
          <Button type="submit" disabled={!inputValue.trim()}>
            Send
          </Button>
        </div>
      </form>
    </Card>
  );
}

function ChatMessage({ message }: { message: Message }) {
  const isBot = message.sender === 'bot';

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'}`}>
      <div
        className={`
          max-w-[80%] rounded-2xl px-4 py-3
          ${isBot
            ? 'bg-primary-100 text-primary-900 rounded-bl-sm'
            : 'bg-neutral-200 text-slate-800 rounded-br-sm'
          }
        `}
      >
        <p className="text-sm">{message.text}</p>
        <span className="text-xs opacity-60 mt-1 block">
          {message.timestamp.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true,
          })}
        </span>
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="flex justify-start">
      <div className="bg-primary-100 rounded-2xl rounded-bl-sm px-4 py-3">
        <div className="flex gap-1">
          <span className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
          <span className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
          <span className="w-2 h-2 bg-primary-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
        </div>
      </div>
    </div>
  );
}
