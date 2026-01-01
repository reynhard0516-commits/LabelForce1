import { useEffect, useState } from "react";
import { getMe } from "../services/auth";
import { getToken } from "../authStorage";

export default function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    async function load() {
      const token = getToken();
      if (!token) return;

      const me = await getMe(token);
      setUser(me);
    }

    load();
  }, []);

  if (!user) return <p>Not logged in</p>;

  return <pre>{JSON.stringify(user, null, 2)}</pre>;
}
