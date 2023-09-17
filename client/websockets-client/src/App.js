import "./App.css";
import React, { useEffect, useState, useRef } from "react";
import {
  Container,
  Form,
  Button,
  ListGroup,
  Navbar,
  FormLabel,
} from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCircle } from "@fortawesome/free-solid-svg-icons";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import Tooltip from "react-bootstrap/Tooltip";
import { v4 as uuidv4 } from "uuid";
import ReactMarkdown from "react-markdown";
import "bootstrap/dist/css/bootstrap.min.css";

const WEBSOCKET_SERVER_URL = "ws://localhost:8765";

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState(
    "안녕! python에서 Hello World를 출력하는 코드를 알려 줘"
  );
  const [socket, setSocket] = useState(null);
  const [checked, setChecked] = useState(false); // 체크 여부 판단
  const [checkPreMWs, setCheckPreMWs] = useState(new Set());
  const [checkPostMWs, setCheckPostMWs] = useState(new Set());
  const messageEndRef = useRef(null);
  useEffect(() => {
    const newSocket = new WebSocket(WEBSOCKET_SERVER_URL);
    setSocket(newSocket);

    return () => newSocket.close();
  }, []);

  const checkPreMWHandler = (id, isChecked) => {
    if (isChecked) {
      checkPreMWs.add(id);
      setCheckPreMWs(checkPreMWs);
    } else if (!isChecked) {
      checkPreMWs.delete(id);
      setCheckPreMWs(checkPreMWs);
    }
    console.log(checkPreMWs);
  };
  const checkPostMWHandler = (id, isChecked) => {
    if (isChecked) {
      checkPostMWs.add(id);
      setCheckPostMWs(checkPostMWs);
    } else if (!isChecked) {
      checkPostMWs.delete(id);
      setCheckPostMWs(checkPostMWs);
    }
    console.log(checkPostMWs);
  };

  const checkHandled = ({ target }) => {
    setChecked(!checked);
    if (target.name === "pre-middlewares")
      checkPreMWHandler(target.id, target.checked);
    if (target.name === "post-middlewares")
      checkPostMWHandler(target.id, target.checked);
  };

  useEffect(() => {
    if (socket) {
      socket.addEventListener("message", (event) => {
        const recv = JSON.parse(event.data);

        if (recv.response_type === "prompt_result") {
          if (!recv.error) {
            setMessages((prevMessages) =>
              prevMessages.map((msg) => {
                if (msg.uuid === recv.uuid && msg.type === "user")
                  msg.indicators = msg.indicators.map((indicator) => {
                    if (indicator.state === "pending") {
                      indicator.state = "valid";
                    }
                    return indicator;
                  });
                return msg;
              })
            );
          }
          console.log(recv);
          setMessages((prevMessages) => [
            ...prevMessages,
            {
              message: recv.message,
              type: "ai",
              uuid: recv.uuid,
              indicators: [...recv.post_middlewares].map((mw) => {
                return { name: mw, type: "post", state: "pending", msg: "" };
              }),
            },
          ]);
        }
        if (recv.response_type === "pre_result") {
          console.log(recv);
          setMessages((prevMessages) =>
            prevMessages.map((msg) => {
              if (msg.uuid === recv.uuid && msg.type === "user")
                msg.indicators = msg.indicators.map((indicator) => {
                  if (indicator.name === recv.name) {
                    indicator.state = recv.error ? "invalid" : "valid";
                    indicator.msg = recv.error ? recv.stderr : recv.stdout;
                  }
                  return indicator;
                });
              return msg;
            })
          );
        }
        if (recv.response_type === "post_result") {
          console.log(recv);
          setMessages((prevMessages) =>
            prevMessages.map((msg) => {
              if (msg.uuid === recv.uuid && msg.type === "ai")
                msg.indicators = msg.indicators.map((indicator) => {
                  if (indicator.name === recv.name) {
                    indicator.state = recv.error ? "invalid" : "valid";
                    indicator.msg = recv.error ? recv.stderr : recv.stdout;
                  }
                  return indicator;
                });
              return msg;
            })
          );
        }
      });
    }
  }, [socket]);
  useEffect(() => {
    messageEndRef.current.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleInputChange = (event) => {
    setInputValue(event.target.value);
  };

  const handleSendMessage = (event) => {
    event.preventDefault();
    let msgid = uuidv4();
    setMessages((prevMessages) => [
      ...prevMessages,
      {
        message: inputValue,
        type: "user",
        uuid: msgid,
        indicators: [...checkPreMWs].map((mw) => {
          return { name: mw, type: "pre", state: "pending", msg: "pending" };
        }),
      },
    ]);
    const sendMessage = {
      message: inputValue.trim(),
      uuid: msgid,
      pre_middlewares: [...checkPreMWs],
      post_middlewares: [...checkPostMWs],
    };
    // console.log(JSON.stringify(sendMessage));
    if (inputValue.trim()) {
      socket.send(JSON.stringify(sendMessage));
      setInputValue("");
    }
  };

  return (
    <Container>
      <Navbar
        style={{
          position: "fixed",
          left: "0",
          top: "0",
          width: "250px",
          height: "90%",
          justifyContent: "space-around",
          padding: "20px",
          alignItems: "start",
          backgroundColor: "#e6e6e6",
          borderRadius: "30px",
          display: "flex",
          margin: "10px",
          flexDirection: "column",
        }}
        variant="dark"
        fixed="left"
      >
        <Form style={{ flex: 1 }}>
          <FormLabel>
            <h5>Pre Middlewares</h5>
          </FormLabel>
          <Form.Check
            type="switch"
            name="pre-middlewares"
            id="private-info"
            label="개인정보 검출"
            onChange={(e) => checkHandled(e)}
          />
          <Form.Check
            type="switch"
            name="pre-middlewares"
            id="forbidden-words"
            label="금칙어 여부"
            onChange={(e) => checkHandled(e)}
          />
        </Form>
        <Form style={{ flex: 1 }}>
          <FormLabel>
            <h5>Post Middlewares</h5>
          </FormLabel>
          <Form.Check
            type="switch"
            name="post-middlewares"
            id="python310"
            label="Python 3.10 동작 검증"
            onChange={(e) => checkHandled(e)}
          />
          <Form.Check
            type="switch"
            name="post-middlewares"
            id="python36"
            label="Python 3.6 동작 검증"
            onChange={(e) => checkHandled(e)}
          />
          <Form.Check
            type="switch"
            name="post-middlewares"
            id="wikipedia"
            label="Wikipedia 관련도 검증"
            onChange={(e) => checkHandled(e)}
          />
        </Form>
      </Navbar>
      <Navbar
        style={{
          position: "fixed",
          bottom: "0",
          left: "100px",
          height: "20px",
          justifyContent: "space-around",
          backgroundColor: "transparent",
        }}
        variant="dark"
        fixed="bottom"
      >
        <Form
          onSubmit={handleSendMessage}
          style={{
            display: "flex",
            justifyContent: "space-around",
            alignItems: "center",
            width: "70%",
          }}
        >
          <Form.Group
            controlId="formInput"
            style={{
              flex: "20",
              display: "flex",
              justifyContent: "space-around",
              alignItems: "center",
              flexWrap: "nowrap",
              marginLeft: "10px",
              marginRight: "10px",
            }}
            className={"shadow p-3 mb-5 bg-white rounded"}
          >
            <Form.Control
              type="text"
              placeholder="Enter text"
              value={inputValue}
              onChange={handleInputChange}
            />
            <Button
              variant="dark"
              type="submit"
              style={{ flex: "1", marginLeft: "10px" }}
            >
              Submit
            </Button>
          </Form.Group>
        </Form>
      </Navbar>

      <ListGroup
        className="mt-3"
        style={{ marginBottom: "100px", marginLeft: "250px" }}
      >
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
            <ReactMarkdown>{item.message}</ReactMarkdown>
            {item.indicators.map((indicator, index) => (
              <OverlayTrigger
                placement="bottom"
                overlay={
                  <Tooltip id={`button-tooltip-${index}`}>
                    {indicator.name}
                  </Tooltip>
                }
              >
                <FontAwesomeIcon
                  key={index}
                  icon={faCircle}
                  size="sm"
                  style={{
                    color:
                      indicator.state === "pending"
                        ? "gray"
                        : indicator.state === "valid"
                        ? "#5CCD5C"
                        : "#CD5C5C",
                    marginLeft: "0.3rem",
                  }}
                  onClick={(event) => {
                    // console.log(item.uuid);
                    // console.log(index);
                    setMessages(
                      messages.map((msg) => {
                        if (msg.uuid === item.uuid)
                          msg.indicators[index].state = "valid";
                        return msg;
                      })
                    );
                  }}
                />
              </OverlayTrigger>
            ))}
          </ListGroup.Item>
        ))}
      </ListGroup>
      <div ref={messageEndRef}></div>
    </Container>
  );
}

export default App;
