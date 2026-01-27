// test-gemini.js

const API_KEY = "AIzaSyDNe69LoZHdW19n71JIi2y0-dtFJ6Y3imE"; // <-- put your key here
const MODEL = "gemini-2.5-flash"; // or gemini-pro, gemini-1.5-pro etc.

async function testGemini() {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${MODEL}:generateContent?key=${API_KEY}`;

  const payload = {
    contents: [
      {
        parts: [{ text: "Hello! Just testing if Gemini API works." }]
      }
    ]
  };

  try {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!res.ok) {
      console.error("HTTP Error:", res.status, await res.text());
      return;
    }

    const data = await res.json();
    console.log("Gemini Response:");
    console.log(JSON.stringify(data, null, 2));
  } catch (err) {
    console.error("Request Failed:", err);
  }
}

testGemini();
