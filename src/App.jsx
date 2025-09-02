import { useState, useEffect } from "react";
import { testAPI, getExpenses, addExpense } from "./api.js";
// 👈 make sure api.js is inside src/

function App() {
  const [backendMessage, setBackendMessage] = useState("Loading...");
  const [expenses, setExpenses] = useState([]);
  const [form, setForm] = useState({ title: "", amount: "" });

  // 🔹 Check backend on first load
  useEffect(() => {
    async function checkBackend() {
      const res = await testAPI();
      setBackendMessage(res.message || res.error);
    }
    checkBackend();
  }, []);

  // 🔹 Load all expenses
  async function loadExpenses() {
    const data = await getExpenses();
    setExpenses(data || []);
  }

  // 🔹 Add new expense
  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.title || !form.amount) return alert("Fill all fields");

    await addExpense(form);
    setForm({ title: "", amount: "" });
    loadExpenses(); // refresh list
  }

  return (
    <div style={{ maxWidth: "600px", margin: "auto", padding: "20px" }}>
      <h1>💸 BrokeMate</h1>
      <p>Backend says: <b>{backendMessage}</b></p>

      <hr />

      <h2>Add Expense</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Expense Title"
          value={form.title}
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />
        <input
          type="number"
          placeholder="Amount"
          value={form.amount}
          onChange={(e) => setForm({ ...form, amount: e.target.value })}
        />
        <button type="submit">Add</button>
      </form>

      <hr />

      <h2>Expenses</h2>
      <button onClick={loadExpenses}>Load Expenses</button>
      <ul>
        {expenses.length > 0 ? (
          expenses.map((exp, idx) => (
            <li key={idx}>
              {exp.title} - ₹{exp.amount}
            </li>
          ))
        ) : (
          <p>No expenses yet.</p>
        )}
      </ul>
    </div>
  );
}

export default App;
