import "./App.css";
import React, { useEffect, useState } from "react";
import { Container, Form, Button, ListGroup, Navbar } from "react-bootstrap";
import ReactMarkdown from "react-markdown";
import "bootstrap/dist/css/bootstrap.min.css";

const WEBSOCKET_SERVER_URL = "ws://localhost:8765";

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState(
    "안녕! python에서 Hello World를 출력하는 코드를 알려 줘"
  );
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const newSocket = new WebSocket(WEBSOCKET_SERVER_URL);
    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  useEffect(() => {
    if (socket) {
      socket.addEventListener("open", (event) => {
        socket.send(JSON.stringify({ method: "get_function_list" }));
      });
      socket.addEventListener("message", (event) => {
        const recv = JSON.parse(event.data);

        if (recv.response_type === "prompt_result") {
          setMessages((prevMessages) => [
            ...prevMessages,
            { message: recv.message, type: "ai" },
          ]);
        }
        if (recv.response_type === "pre_result") {
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              message: `${recv.name}: ${recv.error ? "Not valid" : "Valid"}`,
              type: "pre_result",
              error: recv.error,
            },
          ]);
        }
        if (recv.response_type === "post_result") {
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              message: `${recv.name}: ${recv.error ? "Not valid" : "Valid"}`,
              type: "post_result",
              error: recv.error,
            },
          ]);
        }
      });
    }
  }, [socket]);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSendMessage = (event) => {
    event.preventDefault();
    setMessages((prevMessages) => [
      ...prevMessages,
      { message: inputValue, type: "user" },
    ]);
    if (inputValue.trim()) {
      socket.send(JSON.stringify({ message: inputValue.trim() }));
      setInputValue("");
    }
  };

  return (
    <Container>
      <Navbar
        style={{
          position: "sticky",
          justifyContent: "space-around",
          backgroundColor: "white",
        }}
        variant="dark"
        fixed="top"
      >
        <Form
          onSubmit={handleSendMessage}
          style={{
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
            width: "90%",
          }}
        >
          <Form.Label>Input Text</Form.Label>
          <Form.Group
            controlId="formInput"
            style={{
              flex: "20",
              marginLeft: "10px",
              marginRight: "10px",
            }}
          >
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
      </Navbar>

      <ListGroup className="mt-3">
        {messages.map((item, index) => (
          <ListGroup.Item
            key={index}
            style={{
              textAlign: item.type !== "ai" ? "right" : "left",
              backgroundColor:
                (item.type === "pre_result" || item.type === "post_result") &&
                item.error === true
                  ? "#ffc9c9"
                  : item.type === "pre_result" || item.type === "post_result"
                  ? "#e8ffe8"
                  : "white",
            }}
          >
            {" "}
            <ReactMarkdown>{item.message}</ReactMarkdown>
          </ListGroup.Item>
        ))}
      </ListGroup>
    </Container>
  );
}

export default App;
