import { useState } from "react";
import Drugs from "./Drugs";
import Dispense from "./Dispense";

function Dashboard() {
  const [activePage, setActivePage] = useState("dashboard");

  if (activePage === "drugs") {
    return (
      <div>
        <button onClick={() => setActivePage("dashboard")}>
          ← Back to Dashboard
        </button>

        <Drugs />
      </div>
    );
  }

if (activePage === "dispense") {
  return (
    <div>
      <button onClick={() => setActivePage("dashboard")}>
        ← Back to Dashboard
      </button>

      <Dispense />
    </div>
  );
}

  return (
    <div>
      <h1>Docerejj Medical Centre</h1>

      <h2>Dashboard</h2>

      <p>Welcome to the Docerejj Medical Centre system.</p>

      <div>
        <button onClick={() => setActivePage("drugs")}>
          Drugs
        </button>

       <button onClick={() => setActivePage("dispense")}>
          Dispense Drugs
        </button>

        <button>
          Patients
        </button>

        <button>
          My Sales
        </button>
      </div>
    </div>
  );
}

export default Dashboard;