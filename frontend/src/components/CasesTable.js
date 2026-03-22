import React from "react";

function CasesTable({ cases }) {

  return (

    <table className="cases-table">

      <thead>
        <tr>
          <th>Entity</th>
          <th>Court</th>
          <th>Judge</th>
          <th>Status</th>
        </tr>
      </thead>

      <tbody>

        {cases.length === 0 && (
          <tr>
            <td colSpan="4">No cases found</td>
          </tr>
        )}

        {cases.map((c, i) => (

          <tr key={i}>

            <td>{c["Entity Name"]}</td>
            <td>{c.court}</td>
            <td>{c.judge}</td>
            <td>{c.case_status}</td>

          </tr>

        ))}

      </tbody>

    </table>

  );

}

export default CasesTable;