import "./App.css";
import React, { useEffect, useState } from "react";
import { Container, Form, Button, ListGroup } from "react-bootstrap";
import ReactMarkdown from "react-markdown";
import "bootstrap/dist/css/bootstrap.min.css";

const WEBSOCKET_SERVER_URL = "ws://localhost:8765";

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState(
    "urllib.urlencode 를 이용하여 parameter를 쿼리 스트링으로 변환하는 코드를 작성해줘"
  );
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = new WebSocket(WEBSOCKET_SERVER_URL);
    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  useEffect(() => {
    if (socket) {
      socket.addEventListener("message", (event) => {
        setMessages((prevMessages) => [...prevMessages, event.data]);
      });
    }
  }, [socket]);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSendMessage = (event) => {
    event.preventDefault();
    setMessages((prevMessages) => [...prevMessages, `Input: ${inputValue}`]);
    if (inputValue.trim()) {
      socket.send(JSON.stringify({ message: inputValue.trim() }));
      setInputValue("");
    }
  };

  return (
    <Container>
      <Form onSubmit={handleSendMessage}>
        <Form.Group controlId="formInput">
          <Form.Label>Input Text</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter text"
            value={inputValue}
            onChange={handleInputChange}
          />
        </Form.Group>
        <Button variant="dark" type="submit">
          Submit
        </Button>
      </Form>
      <ListGroup className="mt-3">
        {messages.map((message, index) => (
          <ListGroup.Item key={index}>
            {" "}
            <ReactMarkdown>{message}</ReactMarkdown>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </Container>
  );
}

export default App;
