import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [type, setType] = useState('topic');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [darkMode, setDarkMode] = useState(
    window.matchMedia('(prefers-color-scheme: dark)').matches
  );

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/generate-notes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, type }),
      });

      if (!response.ok) throw new Error('Failed to fetch');
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark-mode', !darkMode);
  };

  const qaItems = result?.qa
    ? result.qa
        .split('**\n')
        .filter((item) => item.trim())
        .map((item) => {
          const [question, answer] = item.split('\nA: ').map((s) => s.trim());
          return { question: question.replace('Q: ', ''), answer };
        })
    : [];

  const parseConceptMap = (text) => {
    const lines = text.split('\n');
    let nodes = [];
    let currentNode = null;

    lines.forEach((line) => {
      line = line.trim();
      if (line.startsWith('**')) {
        currentNode = { title: line.replace('**', '').trim(), children: [] };
        nodes.push(currentNode);
      } else if (line && currentNode) {
        currentNode.children.push(line.trim());
      }
    });

    return nodes;
  };

  const conceptNodes = result ? parseConceptMap(result.concept_map) : [];

  return (
    <div className="container">
      <div className="header">
        <h1>Study Notes Generator</h1>
        <button className="toggle-dark-mode" onClick={toggleDarkMode}>
          {darkMode ? 'Light Mode' : 'Dark Mode'}
        </button>
      </div>

      <form onSubmit={handleSubmit} className="form-group">
        <label>
          Enter Text:
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Type your textbook paragraph or chapter here..."
            required
          />
        </label>
        <label>
          Type:
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="topic">Topic</option>
            <option value="chapter">Chapter</option>
          </select>
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Generating...' : 'Generate Notes'}
        </button>
      </form>

      {loading && <div className="loading">Loading...</div>}
      {error && <div className="error">Error: {error}</div>}
      {result && (
        <>
          <div className="card">
            <h2>Summary</h2>
            <div
              className="summary"
              dangerouslySetInnerHTML={{ __html: result.summary.replace(/\n/g, '<br/>') }}
            />
          </div>
          <div className="card">
            <h2>Question & Answers</h2>
            <div className="qa">
              {qaItems.map((item, index) => (
                <div
                  key={index}
                  className={`qa-item ${index < 5 ? 'active' : ''}`}
                  onClick={() => {
                    const qaElements = document.querySelectorAll('.qa-item');
                    qaElements.forEach((el, i) =>
                      el.classList.toggle('active', i === index)
                    );
                  }}
                >
                  <div>{item.question}</div>
                  <div className="answer">{item.answer}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="card">
            <h2>Concept Map</h2>
            <div className="concept-map">
              {conceptNodes.map((node, index) => (
                <div key={index} className="node">
                  <h3>{node.title}</h3>
                  {node.children.map((child, i) => (
                    <div key={i} className="subnode">
                      {child}
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
          <div className="card">
            <h2>Mnemonics</h2>
            <div
              className="mnemonics"
              dangerouslySetInnerHTML={{ __html: result.mnemonics.replace(/\n/g, '<br/>') }}
            />
          </div>
        </>
      )}
    </div>
  );
}

export default App;