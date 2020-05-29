import React, { useState } from "react";
import Loading from "./Loading";
import "./App.scss";

const App = () => {
  const [imgColors, setImgColors] = useState({});
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  if (loading == true) {
    return <Loading />;
  }

  const getColors = (event) => {
    event.preventDefault();
    setError("");
    setLoading(true);
    fetch("/api/get_colors", {
      method: "POST",
      cache: "no-cache",
      headers: {
        content_type: "application/json",
      },
      body: JSON.stringify({
        query: query,
      }),
    })
      .then((res) => {
        // console.log(res);
        return res.json();
      })
      .then((data) => {
        // console.log(data);
        setImgColors(data.colors);
        setError(data.error);
        setLoading(false);
      });
  };

  const colorEls = Object.keys(imgColors).map(function (url) {
    let colors = imgColors[url]["colors"];
    let title = imgColors[url]["title"];
    let link = imgColors[url]["link"];
    return (
      <div className="colorContainer" key={url}>
        <a href={link} target="_blank">
          <img className="colorImg" src={url} />
        </a>
        <a href={link}>{title}</a>
        <div className="palette">
          {colors.map(function (color, index) {
            return (
              <div
                key={color}
                className="colorEl"
                style={{ background: color }}
              />
            );
          })}
        </div>
      </div>
    );
  });

  const errorEl = error ? <p>{error}</p> : null;

  return (
    <div className="App">
      <form className="colorsForm" onSubmit={getColors}>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          name="search"
          type="text"
          placeholder="what's the vibe?"
        />
        <button>get a palette</button>
      </form>
      {errorEl}
      {colorEls}
    </div>
  );
};

export default App;
