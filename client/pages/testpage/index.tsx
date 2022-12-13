import React, { useEffect, useState } from "react";
import axios from "axios";

interface userResponse {
  email: string;
}

function TestPage() {
  const [users, setUsers] = useState<userResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  let fetchUrl =
    process.env.NODE_ENV === "development"
      ? "http://127.0.0.1:8000/api/users/"
      : "<deployed url>";

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(fetchUrl);

        console.log(response);
        setUsers(response.data);
        setLoading(false);
      } catch (err) {
        let message;
        if (err instanceof Error) message = err.message;
        else message = String(err);
        setLoading(false);
        setError(message);
      }
    };

    fetchData();
  }, [fetchUrl]);

  return (
    <>
      {loading ? (
        <h1 style={{ textAlign: "center", width: "100%" }}>Loading...</h1>
      ) : (
        <>
          {error && <h1>{error}</h1>}
          {users.length && (
            <>
              <h1 style={{ textAlign: "center", width: "100%" }}>Users</h1>
              <ul style={{ listStyle: "none" }}>
                {users.map((user, index) => {
                  return <li key={index}>{user.email}</li>;
                })}
              </ul>
            </>
          )}
        </>
      )}
    </>
  );
}

export default TestPage;
