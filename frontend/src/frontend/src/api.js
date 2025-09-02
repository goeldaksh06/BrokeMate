const API_BASE_URL = "https://brokemate-1.onrender.com"; // 👈 your backend URL

// Test backend connection
export async function testAPI() {
  try {
    const response = await fetch(`${API_BASE_URL}/test`);
    return await response.json();
  } catch (error) {
    return { error: "Failed to connect to backend" };
  }
}

// Get all expenses
export async function getExpenses() {
  try {
    const response = await fetch(`${API_BASE_URL}/expenses`);
    return await response.json();
  } catch (error) {
    return [];
  }
}

// Add a new expense
export async function addExpense(expense) {
  try {
    const response = await fetch(`${API_BASE_URL}/expenses`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(expense),
    });
    return await response.json();
  } catch (error) {
    return { error: "Failed to add expense" };
  }
}
