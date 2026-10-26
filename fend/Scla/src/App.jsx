import { useState } from "react";
import "./App.css";


const API = "https://smart-calculator-66h4.onrender.com";


function App() {

  const [expression, setExpression] = useState("");
  const [result, setResult] = useState("");
  const [history, setHistory] = useState([]);
  const [error, setError] = useState("");


  // Add calculator button value
  const addValue = (value) => {

    setError("");

    setExpression((previous) => previous + value);
  };


  // Clear calculator
  const clearCalculator = () => {

    setExpression("");
    setResult("");
    setError("");
  };


  // Delete last character
  const deleteLast = () => {

    setExpression((previous) =>
      previous.slice(0, -1)
    );
  };


  // Send expression to FastAPI
  const calculate = async () => {

    if (!expression.trim()) {
      setError("Enter a calculation first");
      return;
    }

    try {

      setError("");

      const response = await fetch(
        `${API}/calculate`,
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            expression: expression,
          }),
        }
      );


      const data = await response.json();


      if (!response.ok) {

        setError(
          data.detail || "Calculation failed"
        );

        return;
      }


      setResult(data.result);


      setHistory((previous) => [

        {
          expression: expression,
          result: data.result,
        },

        ...previous,

      ].slice(0, 8));


    } catch (error) {

      setError(
        "Cannot connect to FastAPI backend"
      );
    }
  };


  // Use keyboard Enter
  const handleKeyDown = (event) => {

    if (event.key === "Enter") {
      calculate();
    }
  };


  const buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "**", "+"
  ];


  return (

    <div className="app">

      <div className="calculator-container">

        <div className="calculator">

          <div className="title">

            <p>SMART</p>

            <h1>Calculator</h1>

          </div>


          <div className="display">

            <input
              type="text"
              value={expression}
              onChange={(event) =>
                setExpression(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Enter expression..."
            />

            <div className="answer">

              {error ? (
                <span className="error">
                  {error}
                </span>
              ) : (
                <span>
                  {result !== ""
                    ? `= ${result}`
                    : "Ready"}
                </span>
              )}

            </div>

          </div>


          <div className="special-buttons">

            <button
              className="clear"
              onClick={clearCalculator}
            >
              AC
            </button>


            <button
              onClick={() => addValue("(")}
            >
              (
            </button>


            <button
              onClick={() => addValue(")")}
            >
              )
            </button>


            <button
              onClick={deleteLast}
            >
              DEL
            </button>

          </div>


          <div className="buttons">

            {buttons.map((button) => (

              <button
                key={button}

                className={
                  ["+", "-", "*", "/", "**"]
                    .includes(button)
                    ? "operator"
                    : ""
                }

                onClick={() =>
                  addValue(button)
                }
              >

                {button === "*"
                  ? "×"
                  : button === "/"
                  ? "÷"
                  : button === "**"
                  ? "xʸ"
                  : button}

              </button>

            ))}

          </div>


          <button
            className="equals"
            onClick={calculate}
          >
            =
          </button>

        </div>


        <div className="history">

          <div className="history-header">

            <div>

              <p>RECENT</p>

              <h2>History</h2>

            </div>


            <button
              onClick={() =>
                setHistory([])
              }
            >
              Clear
            </button>

          </div>


          {history.length === 0 ? (

            <div className="empty-history">

              <span>⌁</span>

              <p>
                Your calculations will
                appear here.
              </p>

            </div>

          ) : (

            <div className="history-list">

              {history.map((item, index) => (

                <div
                  className="history-item"
                  key={index}
                  onClick={() =>
                    setExpression(
                      item.expression
                    )
                  }
                >

                  <p>
                    {item.expression}
                  </p>

                  <strong>
                    = {item.result}
                  </strong>

                </div>

              ))}

            </div>

          )}

        </div>

      </div>

    </div>
  );
}


export default App;