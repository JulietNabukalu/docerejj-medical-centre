import { useEffect, useState } from "react";

function Drugs() {
  const [drugs, setDrugs] = useState([]);
  const [loading, setLoading] = useState(true);

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
      } finally {
        setLoading(false);
      }
    };

    fetchDrugs();
  }, []);

  if (loading) {
    return <p>Loading drugs...</p>;
  }

  return (
    <div>
      <h2>Drugs & Inventory</h2>

      {drugs.length === 0 ? (
        <p>No drugs found.</p>
      ) : (
        <table border="1" cellPadding="8">
          <thead>
            <tr>
              <th>ID</th>
              <th>Drug Name</th>
              <th>Price</th>
              <th>Stock</th>
            </tr>
          </thead>

          <tbody>
            {drugs.map((drug) => (
              <tr key={drug.id}>
                <td>{drug.id}</td>
                <td>{drug.name}</td>
                <td>{drug.price}</td>
                <td>{drug.stock_quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Drugs;