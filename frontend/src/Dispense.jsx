import { useEffect, useState } from "react";

function Dispense() {
  const [drugs, setDrugs] = useState([]);
  const [selectedDrug, setSelectedDrug] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    const fetchDrugs = async () => {
      const token = localStorage.getItem("access_token");

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/drugs/",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );

        const data = await response.json();

        if (!response.ok) {
          console.error("Failed to fetch drugs:", data);
          return;
        }

        setDrugs(data);
      } catch (error) {
        console.error("Error fetching drugs:", error);
      }
    };

    fetchDrugs();
  }, []);

  const handleAddToSale = () => {
    if (!selectedDrug) {
      alert("Please select a drug.");
      return;
    }

    if (quantity <= 0) {
      alert("Quantity must be greater than zero.");
      return;
    }

    const drug = drugs.find(
      (drug) => drug.id === Number(selectedDrug)
    );

    if (!drug) {
      alert("Drug not found.");
      return;
    }

    if (quantity > drug.stock_quantity) {
      alert("Not enough stock available.");
      return;
    }

    const existingItem = cart.find(
      (item) => item.drug_id === drug.id
    );

    if (existingItem) {
      const newQuantity =
        existingItem.quantity + Number(quantity);

      if (newQuantity > drug.stock_quantity) {
        alert("Not enough stock available.");
        return;
      }

      setCart(
        cart.map((item) =>
          item.drug_id === drug.id
            ? {
                ...item,
                quantity: newQuantity,
                total: newQuantity * drug.price,
              }
            : item
        )
      );
    } else {
      setCart([
        ...cart,
        {
          drug_id: drug.id,
          drug_name: drug.name,
          quantity: Number(quantity),
          unit_price: drug.price,
          total: Number(quantity) * drug.price,
        },
      ]);
    }

    setSelectedDrug("");
    setQuantity(1);
  };

  const handleSubmitSale = async () => {
    if (cart.length === 0) {
      alert("Please add at least one drug to the sale.");
      return;
    }

    const token = localStorage.getItem("access_token");

    const saleData = {
      patient_id: null,
      payment_method: "cash",
      items: cart.map((item) => ({
        drug_id: item.drug_id,
        quantity: item.quantity,
      })),
    };

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/sales/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify(saleData),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(data.detail || "Sale could not be completed.");
        return;
      }

      console.log("Sale created:", data);

      alert(
        `Sale #${data.id} completed successfully. Total: UGX ${data.total_amount}`
      );

      setCart([]);
    } catch (error) {
      console.error("Sale error:", error);
      alert("Could not connect to the server.");
    }
  };

  const totalAmount = cart.reduce(
    (sum, item) => sum + item.total,
    0
  );

  return (
    <div>
      <h2>Dispense Drugs</h2>

      <label>Select Drug</label>
      <br />

      <select
        value={selectedDrug}
        onChange={(event) =>
          setSelectedDrug(event.target.value)
        }
      >
        <option value="">-- Select a drug --</option>

        {drugs.map((drug) => (
          <option key={drug.id} value={drug.id}>
            {drug.name} - UGX {drug.price} - Stock:{" "}
            {drug.stock_quantity}
          </option>
        ))}
      </select>

      <br />
      <br />

      <label>Quantity</label>
      <br />

      <input
        type="number"
        min="1"
        value={quantity}
        onChange={(event) =>
          setQuantity(Number(event.target.value))
        }
      />

      <br />
      <br />

      <button onClick={handleAddToSale}>
        Add to Sale
      </button>

      <hr />

      <h3>Current Sale</h3>

      {cart.length === 0 ? (
        <p>No drugs added yet.</p>
      ) : (
        <div>
          {cart.map((item) => (
            <div key={item.drug_id}>
              <p>
                {item.drug_name} — {item.quantity} × UGX{" "}
                {item.unit_price} = UGX {item.total}
              </p>
            </div>
          ))}

          <h3>Total: UGX {totalAmount}</h3>

          <button onClick={handleSubmitSale}>
            Submit Sale
          </button>
        </div>
      )}
    </div>
  );
}

export default Dispense;