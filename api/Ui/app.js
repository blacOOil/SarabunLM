async function greet() {
  const name = document.getElementById("nameInput").value || "World";

  // Call your FastAPI backend
  const response = await fetch(`/api/hello?name=${encodeURIComponent(name)}`);
  const data = await response.json();

  document.getElementById("result").textContent = data.message;
  }