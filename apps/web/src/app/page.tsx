import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import { sessionCookieNames } from "@/lib/auth";

export default async function HomePage() {
  const cookieStore = await cookies();
  const hasSession =
    cookieStore.has(sessionCookieNames.access) || cookieStore.has(sessionCookieNames.refresh);

  redirect(hasSession ? "/dashboard" : "/auth");
}
